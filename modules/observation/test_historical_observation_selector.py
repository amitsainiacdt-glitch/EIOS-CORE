"""Historical Observation Selector validation."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.observation.historical_observation_selector import (
    HistoricalObservationSelector,
)
from modules.observation.observation import Observation
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import (
    ObservationPersistence,
)
from modules.observation.observation_registry import ObservationRegistry


BASE_TIME = datetime(2026, 8, 20, 12, 0, 0)


def make_observation(
    *,
    title: str,
    timestamp: datetime,
    entity: str = "ANUP",
    category: str = "Financial Results",
    source: str = "Company filing",
) -> Observation:
    return Observation(
        title=title,
        description=title,
        source=source,
        category=category,
        entity=entity,
        confidence=90.0,
        timestamp=timestamp,
    )


def main() -> None:
    selector = HistoricalObservationSelector()
    current = make_observation(
        title="Current",
        timestamp=BASE_TIME,
    )
    older = make_observation(
        title="Older",
        timestamp=BASE_TIME - timedelta(days=2),
    )
    latest = make_observation(
        title="Latest historical",
        timestamp=BASE_TIME - timedelta(days=1),
    )

    selection = selector.select(
        current,
        [older, latest],
    )
    assert selection.selected_observation is latest
    assert selection.eligible_count == 2

    normalized = selector.select(
        current,
        [
            make_observation(
                title="Normalized",
                timestamp=BASE_TIME - timedelta(hours=1),
                entity=" anup ",
                category=" financial   results ",
            )
        ],
    )
    assert normalized.selected_observation is not None

    excluded = selector.select(
        current,
        [
            make_observation(
                title="Wrong entity",
                timestamp=BASE_TIME - timedelta(hours=1),
                entity="KPIT",
            ),
            make_observation(
                title="Wrong category",
                timestamp=BASE_TIME - timedelta(hours=1),
                category="Management",
            ),
            make_observation(
                title="Same time",
                timestamp=BASE_TIME,
            ),
            make_observation(
                title="Future",
                timestamp=BASE_TIME + timedelta(hours=1),
            ),
        ],
    )
    assert excluded.selected_observation is None
    assert excluded.eligible_count == 0

    legacy_naive = make_observation(
        title="Legacy naive",
        timestamp=BASE_TIME - timedelta(hours=2),
    )
    aware_current = make_observation(
        title="Aware current",
        timestamp=BASE_TIME.replace(tzinfo=timezone.utc),
    )
    mixed = selector.select(aware_current, [legacy_naive])
    assert mixed.selected_observation is legacy_naive
    assert legacy_naive.timestamp == BASE_TIME - timedelta(hours=2)
    assert legacy_naive.timestamp.tzinfo is None

    tied_time = BASE_TIME - timedelta(hours=1)
    ambiguous = selector.select(
        current,
        [
            make_observation(
                title="Tie A",
                timestamp=tied_time,
                source="Source A",
            ),
            make_observation(
                title="Tie B",
                timestamp=tied_time,
                source="Source B",
            ),
        ],
    )
    assert ambiguous.selected_observation is None
    assert ambiguous.eligible_count == 2
    assert "ambiguous" in ambiguous.reason.casefold()

    empty = selector.select(current, [])
    assert empty.selected_observation is None

    with TemporaryDirectory() as temp_dir:
        registry = ObservationRegistry()
        registry.add(older)
        registry.add(latest)
        engine = ObservationEngine(
            registry=registry,
            persistence=ObservationPersistence(
                Path(temp_dir) / "observations.json"
            ),
        )
        engine_selection = engine.select_historical(current)
        assert engine_selection.selected_observation is latest
        assert registry.count() == 2

    try:
        selector.select(None, [])
        raise AssertionError("None current observation was accepted")
    except ValueError:
        pass

    print(
        "HISTORICAL OBSERVATION SELECTOR: ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
