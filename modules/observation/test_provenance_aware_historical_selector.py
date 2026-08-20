"""Provenance-aware historical candidate selection validation."""

from datetime import datetime, timedelta

from modules.observation.historical_observation_selector import (
    HistoricalObservationSelector,
    HistoricalSelectionBasis,
)
from modules.observation.observation import (
    Observation,
    ObservationProvenance,
)


CURRENT_TIME = datetime(2026, 8, 20, 12, 0, 0)


def make_observation(
    title,
    age_hours,
    *,
    job_id=None,
    intent=None,
    provenance=True,
):
    lineage = None

    if provenance:
        lineage = ObservationProvenance(
            job_id=job_id,
            research_intent=intent,
        )

    return Observation(
        title=title,
        description=title,
        source="https://example.com/report",
        category="External Web",
        entity="Example Limited",
        confidence=75.0,
        timestamp=(
            CURRENT_TIME - timedelta(hours=age_hours)
        ),
        provenance=lineage,
    )


def main() -> None:
    selector = HistoricalObservationSelector()
    current = make_observation(
        "Current",
        0,
        job_id="JOB-ORDERS",
        intent="ORDER_AND_CAPACITY",
    )

    exact_job = make_observation(
        "Exact job",
        24,
        job_id=" job-orders ",
        intent="ORDER_AND_CAPACITY",
    )
    newer_intent = make_observation(
        "Newer intent only",
        1,
        job_id=None,
        intent=" order_and_capacity ",
    )
    newest_legacy = make_observation(
        "Newest legacy",
        0.5,
        provenance=False,
    )

    job_selection = selector.select(
        current,
        [newest_legacy, newer_intent, exact_job],
    )
    assert job_selection.selected_observation is exact_job
    assert job_selection.eligible_count == 1
    assert job_selection.selection_basis == (
        HistoricalSelectionBasis.JOB_ID
    )

    conflicting_job = make_observation(
        "Conflicting job",
        1,
        job_id="JOB-RESULTS",
        intent="ORDER_AND_CAPACITY",
    )
    conflict_selection = selector.select(
        current,
        [conflicting_job],
    )
    assert conflict_selection.selected_observation is None
    assert conflict_selection.eligible_count == 0

    intent_selection = selector.select(
        current,
        [newest_legacy, newer_intent, conflicting_job],
    )
    assert intent_selection.selected_observation is newer_intent
    assert intent_selection.selection_basis == (
        HistoricalSelectionBasis.RESEARCH_INTENT
    )

    legacy_selection = selector.select(
        current,
        [newest_legacy, conflicting_job],
    )
    assert legacy_selection.selected_observation is newest_legacy
    assert legacy_selection.selection_basis == (
        HistoricalSelectionBasis.LEGACY_ENTITY_CATEGORY
    )

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
    legacy_compatibility = selector.select(
        legacy_current,
        [older_legacy, exact_job],
    )
    assert legacy_compatibility.selected_observation is older_legacy
    assert legacy_compatibility.selection_basis == (
        HistoricalSelectionBasis.LEGACY_ENTITY_CATEGORY
    )

    tied_time = 12
    tie_a = make_observation(
        "Tie A",
        tied_time,
        job_id="JOB-ORDERS",
        intent="ORDER_AND_CAPACITY",
    )
    tie_b = make_observation(
        "Tie B",
        tied_time,
        job_id="JOB-ORDERS",
        intent="ORDER_AND_CAPACITY",
    )
    ambiguous = selector.select(current, [tie_a, tie_b])
    assert ambiguous.selected_observation is None
    assert ambiguous.selection_basis == HistoricalSelectionBasis.JOB_ID

    print(
        "PROVENANCE-AWARE HISTORICAL SELECTOR: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
