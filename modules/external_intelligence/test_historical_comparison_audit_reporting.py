"""No-network validation for opt-in historical comparison audit output."""

import json
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)
from modules.external_intelligence.research_runtime_bootstrap import (
    ResearchRuntimeBootstrap,
    ResearchRuntimeBootstrapConfig,
)
from modules.observation.observation import (
    Observation,
    ObservationProvenance,
)
from modules.observation.observation_persistence import (
    ObservationPersistence,
)


RUN_TIME = datetime(2026, 8, 20, 12, 0, 0)


def make_observation(
    title: str,
    age_hours: int,
    *,
    entity: str = "Example Limited",
    job_id: str | None = "JOB-ORDERS",
    intent: str | None = "ORDER_AND_CAPACITY",
) -> Observation:
    fingerprint = sha256(title.encode("utf-8")).hexdigest()

    return Observation(
        title=title,
        description=title,
        source="https://research.example.com/report",
        category="External Web",
        entity=entity,
        confidence=80.0,
        timestamp=RUN_TIME - timedelta(hours=age_hours),
        provenance=ObservationProvenance(
            cycle_id="audit-validation",
            job_id=job_id,
            research_intent=intent,
            retrieved_at=RUN_TIME - timedelta(hours=age_hours),
            source_url="https://research.example.com/report",
            source_domain="research.example.com",
            source_type="text/html",
            content_fingerprint=fingerprint,
        ),
    )


class FakeController:
    def __init__(self, runtime, observations):
        self.runtime = runtime
        self.observations = observations

    def run_once(self, now):
        for observation in self.observations:
            self.runtime.observation_registry.add(observation)

        return SimpleNamespace(
            due_jobs=[],
            executed_jobs=[],
            results=[
                SimpleNamespace(
                    observations=list(self.observations),
                    status="SUCCESS",
                )
            ],
        )


def validate_runtime_reporting(root: Path) -> None:
    observation_path = root / "state" / "observations.json"
    audit_path = root / "audit" / "historical.jsonl"
    historical = make_observation("Historical orders", 24)
    current = make_observation("Current orders", 0)
    unrelated = make_observation(
        "Unrelated current",
        0,
        entity="Different Limited",
        job_id="JOB-OTHER",
        intent="OTHER_INTENT",
    )
    tie_a = make_observation(
        "Ambiguous history A",
        12,
        entity="Ambiguous Limited",
    )
    tie_b = make_observation(
        "Ambiguous history B",
        12,
        entity="Ambiguous Limited",
    )
    ambiguous_current = make_observation(
        "Ambiguous current",
        0,
        entity="Ambiguous Limited",
    )
    ObservationPersistence(observation_path).save(
        [historical, tie_a, tie_b]
    )

    runtime = ResearchRuntime(
        observation_path=observation_path,
        tavily_api_key="test-key",
        enable_historical_comparison=True,
        historical_comparison_audit_path=audit_path,
    )
    runtime.controller = FakeController(
        runtime,
        [current, unrelated, ambiguous_current],
    )
    runtime.run_once(RUN_TIME)

    assert audit_path.exists()
    lines = audit_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    selected = json.loads(lines[0])
    no_match = json.loads(lines[1])
    ambiguous = json.loads(lines[2])

    assert selected["schema_version"] == 1
    assert selected["recorded_at"] == RUN_TIME.isoformat()
    assert selected["selection"]["basis"] == "JOB_ID"
    assert selected["selection"]["eligible_count"] == 1
    assert selected["current_observation"]["job_id"] == "JOB-ORDERS"
    assert selected["historical_observation"]["title"] == (
        "Historical orders"
    )
    assert selected["comparison"]["type"] == "INFORMATION_CHANGE"
    assert selected["comparison"]["change_direction"] == "UNKNOWN"
    assert selected["comparison"]["materiality"] == "UNKNOWN"

    assert no_match["selection"]["basis"] is None
    assert no_match["historical_observation"] is None
    assert no_match["comparison"] is None

    assert ambiguous["selection"]["basis"] == "JOB_ID"
    assert "ambiguous" in ambiguous["selection"]["reason"].casefold()
    assert ambiguous["historical_observation"] is None
    assert ambiguous["comparison"] is None

    persisted = ObservationPersistence(observation_path).load()
    assert len(persisted) == 6
    assert {item.title for item in persisted} == {
        "Historical orders",
        "Ambiguous history A",
        "Ambiguous history B",
        "Current orders",
        "Unrelated current",
        "Ambiguous current",
    }
    assert runtime.context.get_evidence() == []
    assert runtime.context.get_assumptions() == []
    assert runtime.context.get_knowledge() == []
    assert runtime.context.intelligence_mesh.count() == 3


def validate_disabled_and_path_safety(root: Path) -> None:
    observation_path = root / "disabled-observations.json"
    disabled_audit = root / "disabled-audit.jsonl"

    runtime = ResearchRuntime(
        observation_path=observation_path,
        tavily_api_key="test-key",
    )
    runtime.controller = FakeController(
        runtime,
        [make_observation("Disabled current", 0)],
    )
    runtime.run_once(RUN_TIME)
    assert not disabled_audit.exists()

    try:
        ResearchRuntime(
            observation_path=observation_path,
            tavily_api_key="test-key",
            historical_comparison_audit_path=disabled_audit,
        )
        raise AssertionError("Disabled comparison accepted an audit path")
    except ValueError:
        pass

    try:
        ResearchRuntime(
            observation_path=observation_path,
            tavily_api_key="test-key",
            enable_historical_comparison=True,
            historical_comparison_audit_path=observation_path,
        )
        raise AssertionError("Observation path accepted as audit path")
    except ValueError:
        pass


def validate_bootstrap_configuration(root: Path) -> None:
    observation_path = root / "bootstrap-observations.json"
    audit_path = root / "bootstrap-audit.jsonl"
    config = ResearchRuntimeBootstrapConfig.from_environment(
        {
            "TAVILY_API_KEY": "test-key",
            "EIOS_OBSERVATION_PATH": str(observation_path),
            "EIOS_ENABLE_HISTORICAL_COMPARISON": "true",
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH": str(audit_path),
        }
    )
    assert config.historical_comparison_audit_path == audit_path

    bootstrap = ResearchRuntimeBootstrap(
        config,
        job_provider=lambda: [],
        dependency_checker=lambda name: True,
    )
    validation = bootstrap.validate()
    assert validation.ready is True
    assert validation.historical_comparison_audit_enabled is True
    assert validation.historical_comparison_audit_path == audit_path
    assert not audit_path.exists()

    runtime_options = {}

    def runtime_factory(**kwargs):
        runtime_options.update(kwargs)
        return SimpleNamespace(register_job=lambda job: None)

    built = ResearchRuntimeBootstrap(
        config,
        runtime_factory=runtime_factory,
        job_provider=lambda: [],
        dependency_checker=lambda name: True,
    ).build()
    assert built is not None
    assert runtime_options[
        "historical_comparison_audit_path"
    ] == audit_path

    disabled = ResearchRuntimeBootstrap(
        ResearchRuntimeBootstrapConfig(
            tavily_api_key="test-key",
            observation_path=observation_path,
            historical_comparison_audit_path=audit_path,
        ),
        job_provider=lambda: [],
        dependency_checker=lambda name: True,
    ).validate()
    assert disabled.ready is False
    assert any(
        "requires" in error.casefold()
        for error in disabled.errors
    )

    shared_path = ResearchRuntimeBootstrap(
        ResearchRuntimeBootstrapConfig(
            tavily_api_key="test-key",
            observation_path=observation_path,
            enable_historical_comparison=True,
            historical_comparison_audit_path=observation_path,
        ),
        job_provider=lambda: [],
        dependency_checker=lambda name: True,
    ).validate()
    assert shared_path.ready is False
    assert any(
        "separate" in error.casefold()
        for error in shared_path.errors
    )


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        with patch(
            "requests.sessions.Session.request",
            side_effect=AssertionError(
                "Audit validation must not perform HTTP requests"
            ),
        ):
            validate_runtime_reporting(root)
            validate_disabled_and_path_safety(root)
            validate_bootstrap_configuration(root)

    print(
        "HISTORICAL COMPARISON AUDIT REPORTING: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
