"""
EIOS
Everest Investment Operating System

Catalyst Coverage Priority Engine Test
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CatalystCoverageEvidence,
    CoveragePriority,
    CatalystCoveragePriority,
)

from modules.opportunity.catalyst.catalyst_coverage_priority_engine import (
    CatalystCoveragePriorityEngine,
)


def main() -> None:

    # ======================================================
    # PRIORITY THRESHOLD TESTS
    # ======================================================

    low = (
        CatalystCoveragePriorityEngine
        ._priority_from_evidence(
            CatalystCoverageEvidence(
                earnings_impact=1,
                detection_lead_time=1,
                cross_sector_applicability=1,
                observability=1,
                persistence=1,
                evidence_availability=1,
                second_order_potential=1,
                market_mispricing_potential=1,
            )
        )
    )

    assert low == CoveragePriority.LOW

    medium = (
        CatalystCoveragePriorityEngine
        ._priority_from_evidence(
            CatalystCoverageEvidence(
                earnings_impact=2,
                detection_lead_time=2,
                cross_sector_applicability=2,
                observability=2,
                persistence=1,
                evidence_availability=1,
                second_order_potential=1,
                market_mispricing_potential=1,
            )
        )
    )

    assert medium == CoveragePriority.MEDIUM

    high = (
        CatalystCoveragePriorityEngine
        ._priority_from_evidence(
            CatalystCoverageEvidence(
                earnings_impact=3,
                detection_lead_time=3,
                cross_sector_applicability=3,
                observability=3,
                persistence=3,
                evidence_availability=3,
                second_order_potential=3,
                market_mispricing_potential=3,
            )
        )
    )

    assert high == CoveragePriority.HIGH

    critical = (
        CatalystCoveragePriorityEngine
        ._priority_from_evidence(
            CatalystCoverageEvidence(
                earnings_impact=5,
                detection_lead_time=5,
                cross_sector_applicability=5,
                observability=5,
                persistence=5,
                evidence_availability=5,
                second_order_potential=5,
                market_mispricing_potential=5,
            )
        )
    )

    assert critical == CoveragePriority.CRITICAL

    # ======================================================
    # QUEUE SIZE
    # ======================================================

    queue = (
        CatalystCoveragePriorityEngine.build_queue()
    )

    assert len(queue) == 27

    assert (
        CatalystCoveragePriorityEngine.uncovered_count()
        == 27
    )

    # ======================================================
    # ONLY UNCOVERED FAMILIES
    # ======================================================

    for item in queue:

        assert (
            item.family
            in CatalystFamily
        )

        assert (
            CatalystCoveragePriorityEngine.contains(
                item.family
            )
        )

    # ======================================================
    # NO COVERED FAMILIES
    # ======================================================

    covered_families = {
        CatalystFamily.CAPACITY_EXPANSION,
        CatalystFamily.ORDER_CONTRACT,
        CatalystFamily.REGULATORY_CHANGE,
    }

    for item in queue:

        assert (
            item.family
            not in covered_families
        )

    # ======================================================
    # EVIDENCE-DRIVEN PRIORITY
    # ======================================================

    profiled_families = {
        CatalystFamily.REVENUE_GROWTH,
        CatalystFamily.VOLUME_GROWTH,
        CatalystFamily.PRICING,
        CatalystFamily.MARGIN_EXPANSION,
        CatalystFamily.TECHNOLOGY_ADOPTION,
        CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
    }

    for item in queue:

        if item.family in profiled_families:

            assert (
                item.priority
                == CoveragePriority.CRITICAL
            )

        else:

            assert (
                item.priority
                == CoveragePriority.LOW
            )

    # ======================================================
    # EVIDENCE PROFILE
    # ======================================================

    for item in queue:

        assert isinstance(
            item.evidence,
            CatalystCoverageEvidence,
        )

        values = [
            item.evidence.earnings_impact,
            item.evidence.detection_lead_time,
            item.evidence.cross_sector_applicability,
            item.evidence.observability,
            item.evidence.persistence,
            item.evidence.evidence_availability,
            item.evidence.second_order_potential,
            item.evidence.market_mispricing_potential,
        ]

        for value in values:

            assert 0 <= value <= 5

    # ======================================================
    # EXPLICIT PROFILE VALIDATION
    # ======================================================

    revenue = next(
        item
        for item in queue
        if item.family
        == CatalystFamily.REVENUE_GROWTH
    )

    assert (
        revenue.evidence.earnings_impact
        == 5
    )

    assert (
        revenue.evidence.detection_lead_time
        == 4
    )

    assert (
        revenue.priority
        == CoveragePriority.CRITICAL
    )

    product_mix = next(
        item
        for item in queue
        if item.family
        == CatalystFamily.PRODUCT_MIX
    )

    assert (
        product_mix.evidence
        == CatalystCoverageEvidence()
    )

    assert (
        product_mix.priority
        == CoveragePriority.LOW
    )

    # ======================================================
    # RATIONALE
    # ======================================================

    for item in queue:

        assert item.rationale

        if item.family in profiled_families:

            assert (
                "canonical evidence profile"
                in item.rationale.lower()
            )

        else:

            assert (
                "neutral"
                in item.rationale.lower()
            )

    # ======================================================
    # IMMUTABLE RECORD
    # ======================================================

    record = queue[0]

    assert isinstance(
        record,
        CatalystCoveragePriority,
    )

    # ======================================================
    # UNIQUE FAMILIES
    # ======================================================

    families = [
        item.family
        for item in queue
    ]

    assert (
        len(families)
        == len(set(families))
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Priority Thresholds            : PASS"
    )

    print(
        "Priority Queue Size            : PASS"
    )

    print(
        "Uncovered Family Selection     : PASS"
    )

    print(
        "Covered Family Exclusion       : PASS"
    )

    print(
        "Evidence-Driven Priority       : PASS"
    )

    print(
        "Evidence Profile Integrity     : PASS"
    )

    print(
        "Explicit Profile Validation    : PASS"
    )

    print(
        "Priority Rationale             : PASS"
    )

    print(
        "Immutable Priority Record      : PASS"
    )

    print(
        "Unique Family Queue             : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST COVERAGE PRIORITY : PASS"
    )


if __name__ == "__main__":
    main()