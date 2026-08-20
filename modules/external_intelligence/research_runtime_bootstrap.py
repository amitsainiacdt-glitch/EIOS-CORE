"""
EIOS ResearchRuntime operational bootstrap.

Configuration validation is separate from runtime construction and
never performs HTTP requests. The network-capable ResearchRuntime is
imported lazily only when a validated bootstrap is built.
"""

from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Mapping

from modules.external_intelligence.research_job_configuration import (
    ResearchJobConfiguration,
)


@dataclass(frozen=True)
class ResearchRuntimeBootstrapConfig:
    """Environment-derived runtime configuration without side effects."""

    tavily_api_key: str
    observation_path: Path
    enable_historical_comparison: bool = False

    @classmethod
    def from_environment(
        cls,
        environment: Mapping[str, str] | None = None,
    ) -> "ResearchRuntimeBootstrapConfig":
        values = os.environ if environment is None else environment

        historical_value = values.get(
            "EIOS_ENABLE_HISTORICAL_COMPARISON",
            "false",
        )

        return cls(
            tavily_api_key=values.get(
                "TAVILY_API_KEY",
                "",
            ).strip(),
            observation_path=Path(
                values.get(
                    "EIOS_OBSERVATION_PATH",
                    "data/observations.json",
                ).strip()
            ),
            enable_historical_comparison=(
                cls._parse_boolean(
                    historical_value,
                    name=(
                        "EIOS_ENABLE_HISTORICAL_COMPARISON"
                    ),
                )
            ),
        )

    @staticmethod
    def _parse_boolean(
        value: str,
        *,
        name: str,
    ) -> bool:
        normalized = str(value).strip().casefold()

        if normalized in {"1", "true", "yes", "on"}:
            return True

        if normalized in {"0", "false", "no", "off", ""}:
            return False

        raise ValueError(
            f"{name} must be true or false"
        )


@dataclass(frozen=True)
class ResearchRuntimeBootstrapValidation:
    """Safe configuration-readiness result."""

    ready: bool
    errors: tuple[str, ...]
    job_count: int
    observation_path: Path
    historical_comparison_enabled: bool


class ResearchRuntimeBootstrap:
    """Validate, build, and explicitly execute one runtime cycle."""

    def __init__(
        self,
        config: ResearchRuntimeBootstrapConfig,
        *,
        runtime_factory: Callable | None = None,
        job_provider: Callable = (
            ResearchJobConfiguration.all_jobs
        ),
        dependency_checker: Callable[[str], bool] | None = None,
    ) -> None:
        if not isinstance(
            config,
            ResearchRuntimeBootstrapConfig,
        ):
            raise ValueError(
                "config must be ResearchRuntimeBootstrapConfig"
            )

        self.config = config
        self.runtime_factory = runtime_factory
        self.job_provider = job_provider
        self.dependency_checker = (
            dependency_checker
            if dependency_checker is not None
            else self._dependency_available
        )

    def validate(self) -> ResearchRuntimeBootstrapValidation:
        """Validate readiness without constructing or running the runtime."""

        validation, _ = self._validation_snapshot()
        return validation

    def _validation_snapshot(
        self,
    ) -> tuple[ResearchRuntimeBootstrapValidation, tuple]:
        """Return one validated, immutable view of configured jobs."""

        errors = []

        if not self.config.tavily_api_key:
            errors.append(
                "TAVILY_API_KEY is not configured."
            )

        self._validate_observation_path(errors)

        if not self.dependency_checker("requests"):
            errors.append(
                "Python dependency 'requests' is not installed."
            )

        jobs = tuple(self._jobs(errors))

        job_ids = [
            getattr(job, "job_id", "")
            for job in jobs
        ]

        for job in jobs:
            try:
                job.validate()
            except Exception as exc:
                errors.append(
                    "Research job validation failed: "
                    f"{type(exc).__name__}."
                )

        if any(not job_id for job_id in job_ids):
            errors.append(
                "Every research job must have a job_id."
            )

        if len(job_ids) != len(set(job_ids)):
            errors.append(
                "Research job IDs must be unique."
            )

        validation = ResearchRuntimeBootstrapValidation(
            ready=not errors,
            errors=tuple(errors),
            job_count=len(jobs),
            observation_path=self.config.observation_path,
            historical_comparison_enabled=(
                self.config.enable_historical_comparison
            ),
        )
        return validation, jobs

    def build(self):
        """Construct a validated runtime and register production jobs."""

        validation, jobs = self._validation_snapshot()

        if not validation.ready:
            raise RuntimeError(
                "Runtime configuration is not ready: "
                + " ".join(validation.errors)
            )

        runtime_factory = self.runtime_factory

        if runtime_factory is None:
            from modules.external_intelligence.research_runtime import (
                ResearchRuntime,
            )

            runtime_factory = ResearchRuntime

        runtime = runtime_factory(
            observation_path=self.config.observation_path,
            tavily_api_key=self.config.tavily_api_key,
            enable_historical_comparison=(
                self.config.enable_historical_comparison
            ),
        )

        for job in jobs:
            runtime.register_job(job)

        return runtime

    def run_once(
        self,
        now: datetime | None = None,
    ):
        """Explicitly construct and execute one live runtime cycle."""

        runtime = self.build()
        result = runtime.run_once(
            datetime.now() if now is None else now
        )

        return runtime, result

    def _jobs(self, errors: list[str]) -> list:
        try:
            return list(self.job_provider())
        except Exception as exc:
            errors.append(
                "Research job configuration failed: "
                f"{type(exc).__name__}."
            )
            return []

    def _validate_observation_path(
        self,
        errors: list[str],
    ) -> None:
        """Check storage safety without creating or modifying any path."""

        path = self.config.observation_path

        if str(path).strip() in {"", "."}:
            errors.append(
                "EIOS_OBSERVATION_PATH must identify a file."
            )
            return

        if path.exists():
            if not path.is_file():
                errors.append(
                    "EIOS_OBSERVATION_PATH must identify a file, not a directory."
                )
            elif not os.access(path, os.R_OK | os.W_OK):
                errors.append(
                    "EIOS_OBSERVATION_PATH must be readable and writable."
                )
            return

        ancestor = path.parent
        while not ancestor.exists() and ancestor != ancestor.parent:
            ancestor = ancestor.parent

        if not ancestor.is_dir():
            errors.append(
                "EIOS_OBSERVATION_PATH parent must be a directory."
            )
        elif not os.access(ancestor, os.W_OK):
            errors.append(
                "EIOS_OBSERVATION_PATH parent must be writable."
            )

    @staticmethod
    def _dependency_available(name: str) -> bool:
        return importlib.util.find_spec(name) is not None


__all__ = [
    "ResearchRuntimeBootstrap",
    "ResearchRuntimeBootstrapConfig",
    "ResearchRuntimeBootstrapValidation",
]
