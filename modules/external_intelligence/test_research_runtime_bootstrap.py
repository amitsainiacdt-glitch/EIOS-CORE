"""No-network validation for the ResearchRuntime bootstrap."""

from datetime import datetime
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from modules.external_intelligence.research_job import ResearchJob
from modules.external_intelligence.research_runtime_bootstrap import (
    ResearchRuntimeBootstrap,
    ResearchRuntimeBootstrapConfig,
)
from scripts.run_external_research_once import main as launcher_main


def make_job(job_id="JOB-1"):
    return ResearchJob(
        job_id=job_id,
        company="Test Company",
        ticker="TEST",
        question="Check developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=60,
        enabled=True,
        priority=100,
        max_sources=1,
        observation_category="External Web",
        observation_confidence=70.0,
    )


class FakeRuntime:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.jobs = []
        self.run_times = []

    def register_job(self, job):
        self.jobs.append(job)

    def run_once(self, now):
        self.run_times.append(now)
        return SimpleNamespace(executed_jobs=self.jobs)


class FakeBootstrap:
    def __init__(self, config):
        self.config = config
        self.run_count = 0

    def validate(self):
        return SimpleNamespace(
            ready=True,
            errors=(),
            job_count=1,
            observation_path=self.config.observation_path,
            historical_comparison_enabled=(
                self.config.enable_historical_comparison
            ),
        )

    def run_once(self):
        self.run_count += 1
        runtime = SimpleNamespace(
            observation_count=lambda: 0,
        )
        result = SimpleNamespace(executed_jobs=[])
        return runtime, result


def main() -> None:
    config = ResearchRuntimeBootstrapConfig.from_environment(
        {
            "TAVILY_API_KEY": "test-key",
            "EIOS_OBSERVATION_PATH": "data/test.json",
            "EIOS_ENABLE_HISTORICAL_COMPARISON": "true",
        }
    )

    assert config.tavily_api_key == "test-key"
    assert config.observation_path == Path("data/test.json")
    assert config.enable_historical_comparison is True

    bootstrap = ResearchRuntimeBootstrap(
        config,
        runtime_factory=FakeRuntime,
        job_provider=lambda: [make_job()],
        dependency_checker=lambda name: name == "requests",
    )

    validation = bootstrap.validate()
    assert validation.ready is True
    assert validation.errors == ()
    assert validation.job_count == 1

    runtime = bootstrap.build()
    assert runtime.kwargs == {
        "observation_path": Path("data/test.json"),
        "tavily_api_key": "test-key",
        "enable_historical_comparison": True,
    }
    assert len(runtime.jobs) == 1

    run_time = datetime(2026, 8, 20, 12, 0, 0)
    runtime, result = bootstrap.run_once(run_time)
    assert runtime.run_times == [run_time]
    assert result.executed_jobs == runtime.jobs

    missing = ResearchRuntimeBootstrap(
        ResearchRuntimeBootstrapConfig(
            tavily_api_key="",
            observation_path=Path("data/test.json"),
        ),
        runtime_factory=FakeRuntime,
        job_provider=lambda: [make_job()],
        dependency_checker=lambda name: False,
    ).validate()
    assert missing.ready is False
    assert len(missing.errors) == 2

    duplicate_jobs = ResearchRuntimeBootstrap(
        config,
        runtime_factory=FakeRuntime,
        job_provider=lambda: [make_job(), make_job()],
        dependency_checker=lambda name: True,
    ).validate()
    assert duplicate_jobs.ready is False
    assert any(
        "unique" in error.casefold()
        for error in duplicate_jobs.errors
    )

    def reject_invalid_job():
        raise ValueError("invalid job")

    invalid_job = SimpleNamespace(
        job_id="INVALID",
        validate=reject_invalid_job,
    )
    invalid_jobs = ResearchRuntimeBootstrap(
        config,
        job_provider=lambda: [invalid_job],
        dependency_checker=lambda name: True,
    ).validate()
    assert invalid_jobs.ready is False
    assert any(
        "job validation" in error.casefold()
        for error in invalid_jobs.errors
    )

    provider_calls = []

    def changing_job_provider():
        provider_calls.append(len(provider_calls))
        return [make_job(f"JOB-{len(provider_calls)}")]

    snapshot_runtime = ResearchRuntimeBootstrap(
        config,
        runtime_factory=FakeRuntime,
        job_provider=changing_job_provider,
        dependency_checker=lambda name: True,
    ).build()
    assert provider_calls == [0]
    assert [job.job_id for job in snapshot_runtime.jobs] == ["JOB-1"]

    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        directory_target = root / "observations"
        directory_target.mkdir()
        missing_target = root / "new" / "observations.json"

        invalid_path = ResearchRuntimeBootstrap(
            ResearchRuntimeBootstrapConfig(
                tavily_api_key="test-key",
                observation_path=directory_target,
            ),
            job_provider=lambda: [make_job()],
            dependency_checker=lambda name: True,
        ).validate()
        assert invalid_path.ready is False
        assert any("directory" in error for error in invalid_path.errors)

        safe_path = ResearchRuntimeBootstrap(
            ResearchRuntimeBootstrapConfig(
                tavily_api_key="test-key",
                observation_path=missing_target,
            ),
            job_provider=lambda: [make_job()],
            dependency_checker=lambda name: True,
        ).validate()
        assert safe_path.ready is True
        assert not missing_target.exists()
        assert not missing_target.parent.exists()

        construction = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys, types; "
                    "sys.modules['requests'] = types.ModuleType('requests'); "
                    "from pathlib import Path; "
                    "from modules.external_intelligence.research_runtime_bootstrap "
                    "import ResearchRuntimeBootstrap, ResearchRuntimeBootstrapConfig; "
                    f"path = Path({str(missing_target)!r}); "
                    "runtime = ResearchRuntimeBootstrap("
                    "ResearchRuntimeBootstrapConfig('test-key', path), "
                    "dependency_checker=lambda name: True).build(); "
                    "assert runtime.observation_count() == 0; "
                    "assert len(runtime.registry.all()) == 6; "
                    "assert not path.exists()"
                ),
            ],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=False,
        )
        assert construction.returncode == 0, construction.stderr

    fake_bootstrap = FakeBootstrap(config)

    def bootstrap_factory(supplied):
        assert supplied is config
        return fake_bootstrap

    def config_factory():
        return config

    assert launcher_main(
        [],
        bootstrap_factory=bootstrap_factory,
        config_factory=config_factory,
    ) == 0
    assert fake_bootstrap.run_count == 0

    assert launcher_main(
        ["--execute"],
        bootstrap_factory=bootstrap_factory,
        config_factory=config_factory,
    ) == 0
    assert fake_bootstrap.run_count == 1

    try:
        ResearchRuntimeBootstrapConfig.from_environment(
            {
                "TAVILY_API_KEY": "test-key",
                "EIOS_ENABLE_HISTORICAL_COMPARISON": "sometimes",
            }
        )
        raise AssertionError("Invalid boolean was accepted")
    except ValueError:
        pass

    print("RESEARCH RUNTIME BOOTSTRAP: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
