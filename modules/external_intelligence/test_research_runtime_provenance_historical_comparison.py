"""No-network runtime validation for provenance-aware history selection."""

from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
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
    age_hours: float,
    *,
    job_id: str | None = None,
    intent: str | None = None,
    provenance: bool = True,
) -> Observation:
    lineage = None

    if provenance:
        lineage = ObservationProvenance(
            cycle_id="cycle-validation",
            job_id=job_id,
            research_intent=intent,
            retrieved_at=RUN_TIME - timedelta(hours=age_hours),
            source_url="https://research.example.com/report",
            source_domain="research.example.com",
            source_type="text/html",
            content_fingerprint=sha256(title.encode("utf-8")).hexdigest(),
        )

    return Observation(
        title=title,
        description=title,
        source="https://research.example.com/report",
        category="External Web",
        entity="Example Limited",
        confidence=80.0,
        timestamp=RUN_TIME - timedelta(hours=age_hours),
        provenance=lineage,
    )


class FakeController:
    """Deterministic controller that performs no external retrieval."""

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


def execute_scenario(history, current_observations):
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "observations.json"
        ObservationPersistence(path).save(list(history))

        runtime = ResearchRuntime(
            observation_path=path,
            tavily_api_key="test-key",
            enable_historical_comparison=True,
        )
        runtime.controller = FakeController(
            runtime,
            current_observations,
        )
        runtime.run_once(RUN_TIME)

        assert runtime.context.get_evidence() == []
        assert runtime.context.get_assumptions() == []
        assert runtime.context.get_knowledge() == []
        assert runtime.context.intelligence_mesh.count() == len(
            current_observations
        )

        return runtime.historical_comparisons()


def validate_provenance_policy() -> None:
    current = make_observation(
        "Current",
        0,
        job_id="JOB-ORDERS",
        intent="ORDER_AND_CAPACITY",
    )
    exact_job = make_observation(
        "Exact job",
        48,
        job_id=" job-orders ",
        intent="ORDER_AND_CAPACITY",
    )
    newer_intent = make_observation(
        "Newer intent",
        2,
        intent=" order_and_capacity ",
    )
    newest_legacy = make_observation(
        "Newest legacy",
        1,
        provenance=False,
    )

    records = execute_scenario(
        [newest_legacy, newer_intent, exact_job],
        [current],
    )
    selection = records[0].selection
    assert selection.selected_observation == exact_job
    assert selection.selection_basis == HistoricalSelectionBasis.JOB_ID
    assert records[0].comparison is not None

    conflicting_job = make_observation(
        "Conflicting job",
        1,
        job_id="JOB-RESULTS",
        intent="ORDER_AND_CAPACITY",
    )
    records = execute_scenario(
        [newest_legacy, newer_intent, conflicting_job],
        [current],
    )
    selection = records[0].selection
    assert selection.selected_observation == newer_intent
    assert selection.selection_basis == (
        HistoricalSelectionBasis.RESEARCH_INTENT
    )

    records = execute_scenario(
        [newest_legacy, conflicting_job],
        [current],
    )
    selection = records[0].selection
    assert selection.selected_observation == newest_legacy
    assert selection.selection_basis == (
        HistoricalSelectionBasis.LEGACY_ENTITY_CATEGORY
    )


def validate_legacy_and_same_cycle_isolation() -> None:
    legacy_current = make_observation(
        "Legacy current",
        0,
        provenance=False,
    )
    older_legacy = make_observation(
        "Older legacy",
        48,
        provenance=False,
    )
    populated_provenance = make_observation(
        "Populated provenance",
        1,
        job_id="JOB-OTHER",
        intent="OTHER_INTENT",
    )

    records = execute_scenario(
        [populated_provenance, older_legacy],
        [legacy_current],
    )
    selection = records[0].selection
    assert selection.selected_observation == older_legacy
    assert selection.selection_basis == (
        HistoricalSelectionBasis.LEGACY_ENTITY_CATEGORY
    )

    first = make_observation(
        "First same-cycle observation",
        1,
        job_id="JOB-ORDERS",
        intent="ORDER_AND_CAPACITY",
    )
    second = make_observation(
        "Second same-cycle observation",
        0,
        job_id="JOB-ORDERS",
        intent="ORDER_AND_CAPACITY",
    )
    records = execute_scenario([], [first, second])
    assert len(records) == 2
    assert all(
        record.selection.selected_observation is None
        and record.comparison is None
        for record in records
    )


def main() -> None:
    with patch(
        "requests.sessions.Session.request",
        side_effect=AssertionError(
            "Runtime validation must not perform HTTP requests"
        ),
    ):
        validate_provenance_policy()
        validate_legacy_and_same_cycle_isolation()

    print(
        "RESEARCH RUNTIME PROVENANCE HISTORICAL COMPARISON: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
