"""
EIOS
Everest Investment Operating System

Catalyst Coverage Priority Engine Test

Current architecture:
    30 Catalyst Families
    30 Covered
     0 Uncovered
    Priority Queue = 0

The priority engine must therefore return an empty queue.
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


# ==========================================================
# CURRENT COVERED FAMILY SET
# ==========================================================

EXPECTED_COVERED_FAMILIES = {
    CatalystFamily.CAPACITY_EXPANSION,
    CatalystFamily.CAPACITY_UTILISATION,
    CatalystFamily.ORDER_CONTRACT,
    CatalystFamily.CUSTOMER_ADDITION,
    CatalystFamily.MARKET_SHARE,
    CatalystFamily.INDUSTRY_CAPITAL_CYCLE,
    CatalystFamily.SUPPLY_CONSTRAINT,
    CatalystFamily.COMPETITIVE_EXIT,
    CatalystFamily.NEW_PRODUCT_PLATFORM,
    CatalystFamily.TAM_EXPANSION,
    CatalystFamily.REGULATORY_CHANGE,
    CatalystFamily.GOVERNMENT_POLICY,
    CatalystFamily.FISCAL_TAX,
    CatalystFamily.MONETARY_LIQUIDITY,
    CatalystFamily.COMMODITY,
    CatalystFamily.CURRENCY,
    CatalystFamily.TRADE_IMPORT_SUBSTITUTION,
    CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN,
    CatalystFamily.CORPORATE_ACTION_MA,
    CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION,
    CatalystFamily.BALANCE_SHEET_CASH_FLOW,
    CatalystFamily.REVENUE_GROWTH,
    CatalystFamily.VOLUME_GROWTH,
    CatalystFamily.PRICING,
    CatalystFamily.MARGIN_EXPANSION,
    CatalystFamily.TECHNOLOGY_ADOPTION,
    CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
    CatalystFamily.PRODUCT_MIX,
    CatalystFamily.COST_REDUCTION,
    CatalystFamily.OPERATING_LEVERAGE,
}


def main() -> None:

    # ======================================================
    # PRIORITY THRESHOLD TESTS
    # ======================================================

    low = CatalystCoveragePriorityEngine._priority_from_evidence(
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

    assert low == CoveragePriority.LOW

    medium = CatalystCoveragePriorityEngine._priority_from_evidence(
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

    assert medium == CoveragePriority.MEDIUM

    high = CatalystCoveragePriorityEngine._priority_from_evidence(
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

    assert high == CoveragePriority.HIGH

    critical = CatalystCoveragePriorityEngine._priority_from_evidence(
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

    assert critical == CoveragePriority.CRITICAL

    print("Priority Thresholds              : PASS")

    # ======================================================
    # FAMILY / COVERAGE STATE
    # ======================================================

    assert len(CatalystFamily) == 30
    print("Canonical Family Count            : PASS")

    assert len(EXPECTED_COVERED_FAMILIES) == 30
    print("Covered Family Count              : PASS")

    assert EXPECTED_COVERED_FAMILIES == set(CatalystFamily)
    print("Coverage Consistency              : PASS")

    # ======================================================
    # PRIORITY QUEUE
    # ======================================================

    queue = CatalystCoveragePriorityEngine.build_queue()

    assert isinstance(queue, list)
    print("Priority Queue Type               : PASS")

    assert len(queue) == 0
    print("Priority Queue Empty              : PASS")

    assert CatalystCoveragePriorityEngine.uncovered_count() == 0
    print("Uncovered Family Count            : PASS")

    # ======================================================
    # EMPTY QUEUE INTEGRITY
    # ======================================================

    assert queue == []
    print("Empty Queue Integrity             : PASS")

    queue_families = {
        item.family
        for item in queue
    }

    assert queue_families == set()
    print("Queue Family Set Empty            : PASS")

    assert (
        len(queue)
        + len(EXPECTED_COVERED_FAMILIES)
        == len(CatalystFamily)
    )
    print("Coverage / Queue Reconciliation   : PASS")

    # ======================================================
    # COVERED FAMILY EXCLUSION
    # ======================================================

    for family in EXPECTED_COVERED_FAMILIES:
        assert family not in queue_families

    print("Covered Family Exclusion           : PASS")

    # ======================================================
    # FINAL FAMILIES
    # ======================================================

    assert CatalystFamily.CORPORATE_ACTION_MA in EXPECTED_COVERED_FAMILIES
    assert CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION in EXPECTED_COVERED_FAMILIES
    assert CatalystFamily.BALANCE_SHEET_CASH_FLOW in EXPECTED_COVERED_FAMILIES

    assert CatalystFamily.CORPORATE_ACTION_MA not in queue_families
    assert CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION not in queue_families
    assert CatalystFamily.BALANCE_SHEET_CASH_FLOW not in queue_families

    print("Corporate Action / M&A Exclusion  : PASS")
    print("Management Capital Allocation Exclusion : PASS")
    print("Balance Sheet / Cash Flow Exclusion : PASS")

    # ======================================================
    # NO UNINITIALIZED DEVELOPMENT PRIORITY
    # ======================================================

    assert not queue
    print("No Uncovered Priority Records      : PASS")

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()
    print("EIOS CATALYST COVERAGE PRIORITY : PASS")


if __name__ == "__main__":
    main()