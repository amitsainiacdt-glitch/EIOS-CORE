"""
EIOS
Everest Investment Operating System

Observation Historical Comparison Integration Test
===================================================

Validates the opt-in boundary between ObservationEngine and
HistoricalComparisonEngine without changing ingestion behavior.
"""

from datetime import datetime
from tempfile import TemporaryDirectory
from pathlib import Path

from modules.observation.historical_comparison import (
    ComparisonType,
)
from modules.observation.observation import Observation
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import (
    ObservationPersistence,
)
from modules.observation.observation_registry import ObservationRegistry


def make_observation(description: str) -> Observation:
    return Observation(
        title="Quarterly update",
        description=description,
        source="Company filing",
        category="Financial Results",
        entity="ANUP",
        confidence=90.0,
        timestamp=datetime.now(),
    )


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        persistence = ObservationPersistence(
            Path(temp_dir) / "observations.json"
        )
        registry = ObservationRegistry()
        engine = ObservationEngine(
            registry=registry,
            persistence=persistence,
        )

        historical = make_observation("Revenue was 100")
        current = make_observation("Revenue was 120")

        comparison = engine.compare_historical(
            current_observation=current,
            historical_observation=historical,
        )

        assert comparison.comparison_type == (
            ComparisonType.INFORMATION_CHANGE
        )
        assert comparison.change_detected is True
        assert comparison.current_observation is current
        assert comparison.historical_observation is historical

        # Comparison is analytical and must not mutate ingestion state.
        assert registry.count() == 0
        assert persistence.load() == []

        duplicate = engine.compare_historical(
            current_observation=historical,
            historical_observation=historical,
        )

        assert duplicate.comparison_type == ComparisonType.NO_CHANGE
        assert duplicate.change_detected is False
        assert registry.count() == 0

    print(
        "OBSERVATION HISTORICAL COMPARISON INTEGRATION: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
