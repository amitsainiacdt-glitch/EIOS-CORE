"""
EIOS
Everest Investment Operating System

Historical Comparison Engine Test
==================================

Validates the historical comparison boundary without involving
Evidence, Signals, Catalysts, or Opportunity analysis.
"""

from datetime import datetime, timedelta

from modules.observation.historical_comparison import (
    ChangeDirection,
    ComparisonType,
    Materiality,
)

from modules.observation.historical_comparison_engine import (
    HistoricalComparisonEngine,
)

from modules.observation.observation import (
    Observation,
)


def make_observation(
    *,
    title="Industrial Capex Accelerates",
    description="Industrial investment is increasing.",
    source="https://example.com/article",
    category="External Web",
    entity="The Anup Engineering Limited",
    confidence=90.0,
    timestamp=None,
):
    if timestamp is None:
        timestamp = datetime(2026, 8, 20, 10, 0, 0)

    return Observation(
        title=title,
        description=description,
        source=source,
        category=category,
        entity=entity,
        confidence=confidence,
        timestamp=timestamp,
    )


def main():

    print("=" * 60)
    print("EIOS HISTORICAL COMPARISON ENGINE TEST")
    print("=" * 60)

    engine = HistoricalComparisonEngine()

    # ======================================================
    # TEST 1 — IDENTICAL OBSERVATIONS
    # ======================================================

    historical = make_observation()

    current = make_observation()

    result = engine.compare(
        current,
        historical,
    )

    assert result.comparison_type == (
        ComparisonType.NO_CHANGE
    )

    assert result.change_detected is False

    print(
        "Test 1 — Identical Observations       : PASS"
    )

    # ======================================================
    # TEST 2 — TIMESTAMP ONLY
    # ======================================================

    historical = make_observation(
        timestamp=datetime(
            2026,
            8,
            19,
            10,
            0,
            0,
        )
    )

    current = make_observation(
        timestamp=datetime(
            2026,
            8,
            20,
            10,
            0,
            0,
        )
    )

    result = engine.compare(
        current,
        historical,
    )

    assert result.comparison_type == (
        ComparisonType.NO_CHANGE
    )

    assert result.change_detected is False

    print(
        "Test 2 — Timestamp Only              : PASS"
    )

    # ======================================================
    # TEST 3 — CHANGED DESCRIPTION
    # ======================================================

    historical = make_observation(
        description=(
            "Industrial investment is increasing."
        )
    )

    current = make_observation(
        description=(
            "Industrial investment is accelerating "
            "significantly."
        )
    )

    result = engine.compare(
        current,
        historical,
    )

    assert result.comparison_type == (
        ComparisonType.INFORMATION_CHANGE
    )

    assert result.change_detected is True

    print(
        "Test 3 — Changed Information          : PASS"
    )

    # ======================================================
    # TEST 4 — DIFFERENT SOURCE
    # ======================================================

    historical = make_observation(
        source="https://example.com/article"
    )

    current = make_observation(
        source="https://another.example/article"
    )

    result = engine.compare(
        current,
        historical,
    )

    assert result.comparison_type == (
        ComparisonType.SOURCE_CHANGE
    )

    assert result.change_detected is False

    assert (
        result.current_observation.source
        == "https://another.example/article"
    )

    assert (
        result.historical_observation.source
        == "https://example.com/article"
    )

    print(
        "Test 4 — Independent Source            : PASS"
    )

    # ======================================================
    # TEST 5 — NO FABRICATED DIRECTION
    # ======================================================

    historical = make_observation(
        description="Capacity was 100 units."
    )

    current = make_observation(
        description="Capacity is now 150 units."
    )

    result = engine.compare(
        current,
        historical,
    )

    assert result.change_detected is True

    assert result.change_direction == (
        ChangeDirection.UNKNOWN
    )

    assert result.delta is None

    print(
        "Test 5 — No Fabricated Direction       : PASS"
    )

    # ======================================================
    # TEST 6 — HISTORICAL PRESERVATION
    # ======================================================

    historical = make_observation(
        description="Original information."
    )

    current = make_observation(
        description="Updated information."
    )

    result = engine.compare(
        current,
        historical,
    )

    assert result.historical_observation is historical

    print(
        "Test 6 — Historical Preservation       : PASS"
    )

    # ======================================================
    # TEST 7 — CURRENT PRESERVATION
    # ======================================================

    assert result.current_observation is current

    print(
        "Test 7 — Current Preservation           : PASS"
    )

    # ======================================================
    # TEST 8 — OBSERVATION IMMUTABILITY
    # ======================================================

    original_current = (
        current.title,
        current.description,
        current.source,
        current.category,
        current.entity,
        current.confidence,
        current.timestamp,
    )

    original_historical = (
        historical.title,
        historical.description,
        historical.source,
        historical.category,
        historical.entity,
        historical.confidence,
        historical.timestamp,
    )

    engine.compare(
        current,
        historical,
    )

    assert (
        current.title,
        current.description,
        current.source,
        current.category,
        current.entity,
        current.confidence,
        current.timestamp,
    ) == original_current

    assert (
        historical.title,
        historical.description,
        historical.source,
        historical.category,
        historical.entity,
        historical.confidence,
        historical.timestamp,
    ) == original_historical

    print(
        "Test 8 — Observation Immutability      : PASS"
    )

    # ======================================================
    # TEST 9 — DETERMINISTIC COMPARISON
    # ======================================================

    first_result = engine.compare(
        current,
        historical,
    )

    second_result = engine.compare(
        current,
        historical,
    )

    assert (
        first_result.comparison_type
        == second_result.comparison_type
    )

    assert (
        first_result.change_detected
        == second_result.change_detected
    )

    assert (
        first_result.change_direction
        == second_result.change_direction
    )

    assert (
        first_result.materiality
        == second_result.materiality
    )

    assert (
        first_result.delta
        == second_result.delta
    )

    print(
        "Test 9 — Deterministic Comparison      : PASS"
    )

    # ======================================================
    # TEST 10 — INVALID INPUT
    # ======================================================

    try:

        engine.compare(
            None,
            historical,
        )

        assert False

    except ValueError:

        pass

    try:

        engine.compare(
            current,
            None,
        )

        assert False

    except ValueError:

        pass

    print(
        "Test 10 — Invalid Input Protection      : PASS"
    )

    # ======================================================
    # TEST 11 — PROVENANCE
    # ======================================================

    result = engine.compare(
        current,
        historical,
    )

    assert result.provenance

    assert (
        result.current_observation is current
    )

    assert (
        result.historical_observation
        is historical
    )

    print(
        "Test 11 — Provenance Preservation        : PASS"
    )

    # ======================================================
    # TEST 12 — MATERIALITY NOT FABRICATED
    # ======================================================

    assert result.materiality == (
        Materiality.UNKNOWN
    )

    print(
        "Test 12 — Materiality Not Fabricated     : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "HISTORICAL COMPARISON ENGINE : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()