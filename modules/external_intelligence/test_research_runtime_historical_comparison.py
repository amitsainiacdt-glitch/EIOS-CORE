"""Opt-in ResearchRuntime historical comparison validation."""

from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)
from modules.observation.historical_comparison import (
    ComparisonType,
)
from modules.observation.observation import Observation
from modules.observation.observation_persistence import (
    ObservationPersistence,
)


RUN_TIME = datetime(2026, 8, 20, 12, 0, 0)


def make_observation(
    title: str,
    timestamp: datetime,
    *,
    source: str = "Company filing",
) -> Observation:
    return Observation(
        title=title,
        description=title,
        source=source,
        category="Financial Results",
        entity="ANUP",
        confidence=90.0,
        timestamp=timestamp,
    )


class FakeController:
    def __init__(self, runtime, observations):
        self.runtime = runtime
        self.observations = observations

    def run_once(self, now):
        for observation in self.observations:
            self.runtime.observation_registry.add(observation)

        execution_result = SimpleNamespace(
            observations=list(self.observations),
            status="SUCCESS",
        )

        return SimpleNamespace(
            due_jobs=[],
            executed_jobs=[],
            results=[execution_result],
        )


def make_runtime(path, *, enabled, history=()):
    ObservationPersistence(path).save(list(history))

    return ResearchRuntime(
        observation_path=path,
        tavily_api_key="test-key",
        enable_historical_comparison=enabled,
    )


def execute(runtime, observations):
    runtime.controller = FakeController(
        runtime,
        observations,
    )
    return runtime.run_once(RUN_TIME)


def main() -> None:
    historical = make_observation(
        "Historical revenue 100",
        RUN_TIME - timedelta(days=1),
    )
    current = make_observation(
        "Current revenue 120",
        RUN_TIME,
    )

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "selected.json"
        runtime = make_runtime(
            path,
            enabled=True,
            history=[historical],
        )
        result = execute(runtime, [current])

        assert result is not None
        assert runtime.historical_comparison_count() == 1
        record = runtime.historical_comparisons()[0]
        assert record.current_observation is current
        assert record.selection.selected_observation == historical
        assert record.comparison is not None
        assert record.comparison.comparison_type == (
            ComparisonType.INFORMATION_CHANGE
        )

        returned_records = runtime.historical_comparisons()
        returned_records.clear()
        assert runtime.historical_comparison_count() == 1

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "no_history.json"
        runtime = make_runtime(path, enabled=True)
        execute(runtime, [current])

        record = runtime.historical_comparisons()[0]
        assert record.selection.selected_observation is None
        assert record.comparison is None

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "ambiguous.json"
        tied_time = RUN_TIME - timedelta(days=1)
        runtime = make_runtime(
            path,
            enabled=True,
            history=[
                make_observation("Tie A", tied_time, source="A"),
                make_observation("Tie B", tied_time, source="B"),
            ],
        )
        execute(runtime, [current])

        record = runtime.historical_comparisons()[0]
        assert record.selection.selected_observation is None
        assert "ambiguous" in record.selection.reason.casefold()
        assert record.comparison is None

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "disabled.json"
        runtime = make_runtime(
            path,
            enabled=False,
            history=[historical],
        )
        execute(runtime, [current])

        assert runtime.historical_comparison_count() == 0

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "same_cycle.json"
        runtime = make_runtime(path, enabled=True)
        first = make_observation(
            "First same-cycle observation",
            RUN_TIME - timedelta(minutes=1),
        )
        second = make_observation(
            "Second same-cycle observation",
            RUN_TIME,
        )
        execute(runtime, [first, second])

        records = runtime.historical_comparisons()
        assert len(records) == 2
        assert all(
            record.selection.selected_observation is None
            for record in records
        )

    print(
        "RESEARCH RUNTIME HISTORICAL COMPARISON: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
