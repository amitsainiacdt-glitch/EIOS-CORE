"""
EIOS
Everest Investment Operating System

Catalyst Development Queue Engine Test
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CoveragePriority,
)

from modules.opportunity.catalyst.catalyst_development_queue import (
    CatalystDevelopmentItem,
)

from modules.opportunity.catalyst.catalyst_development_queue_engine import (
    CatalystDevelopmentQueueEngine,
)

from modules.opportunity.catalyst.catalyst_development_selector import (
    CatalystDevelopmentSelector,
)


def main() -> None:

    # ======================================================
    # BUILD QUEUE
    # ======================================================

    queue = (
        CatalystDevelopmentQueueEngine.build_queue()
    )

    assert queue == []

    # ======================================================
    # QUEUE COUNT
    # ======================================================

    assert (
        CatalystDevelopmentQueueEngine.count()
        == len(queue)
    )

    assert (
        len(queue)
        == 0
    )

    # ======================================================
    # RECORD TYPE
    # ======================================================

    for item in queue:

        assert isinstance(
            item,
            CatalystDevelopmentItem,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for item in queue:

        assert (
            item.family
            in CatalystFamily
        )

    # ======================================================
    # PRIORITY INTEGRITY
    # ======================================================

    for item in queue:

        assert (
            item.priority
            in CoveragePriority
        )

    # ======================================================
    # RATIONALE INTEGRITY
    # ======================================================

    for item in queue:

        assert item.rationale

    # ======================================================
    # UNIQUE DEVELOPMENT FAMILIES
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
    # COVERED FAMILIES
    # ======================================================

    covered_families = {

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

    # ======================================================
    # COVERED FAMILY COUNT
    # ======================================================

    assert (
        len(covered_families)
        == 30
    )

    # ======================================================
    # COVERED FAMILIES MUST NOT BE IN QUEUE
    # ======================================================

    assert (
        set(families).isdisjoint(
            covered_families
        )
    )

    # ======================================================
    # QUEUE MUST REPRESENT ALL UNCOVERED FAMILIES
    # ======================================================

    uncovered_families = (
        set(CatalystFamily)
        - covered_families
    )

    assert (
        len(uncovered_families)
        == 0
    )

    assert (
        set(families)
        == uncovered_families
    )

    # ======================================================
    # QUEUE / TAXONOMY CONSISTENCY
    # ======================================================

    assert (
        len(families)
        + len(covered_families)
        == len(CatalystFamily)
    )

    assert (
        len(CatalystFamily)
        == 30
    )

    # ======================================================
    # NEW PRODUCT / PLATFORM MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.NEW_PRODUCT_PLATFORM
        in covered_families
    )

    assert (
        CatalystFamily.NEW_PRODUCT_PLATFORM
        not in set(families)
    )

    # ======================================================
    # TAM EXPANSION MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.TAM_EXPANSION
        in covered_families
    )

    assert (
        CatalystFamily.TAM_EXPANSION
        not in set(families)
    )

    # ======================================================
    # GOVERNMENT POLICY MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.GOVERNMENT_POLICY
        in covered_families
    )

    assert (
        CatalystFamily.GOVERNMENT_POLICY
        not in set(families)
    )

    # ======================================================
    # FISCAL / TAX MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.FISCAL_TAX
        in covered_families
    )

    assert (
        CatalystFamily.FISCAL_TAX
        not in set(families)
    )

    # ======================================================
    # MONETARY / LIQUIDITY MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.MONETARY_LIQUIDITY
        in covered_families
    )

    assert (
        CatalystFamily.MONETARY_LIQUIDITY
        not in set(families)
    )

    # ======================================================
    # COMMODITY MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.COMMODITY
        in covered_families
    )

    assert (
        CatalystFamily.COMMODITY
        not in set(families)
    )

    # ======================================================
    # CURRENCY MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.CURRENCY
        in covered_families
    )

    assert (
        CatalystFamily.CURRENCY
        not in set(families)
    )

    # ======================================================
    # TRADE / IMPORT SUBSTITUTION MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.TRADE_IMPORT_SUBSTITUTION
        in covered_families
    )

    assert (
        CatalystFamily.TRADE_IMPORT_SUBSTITUTION
        not in set(families)
    )

    # ======================================================
    # GEOPOLITICAL SUPPLY CHAIN MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
        in covered_families
    )

    assert (
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
        not in set(families)
    )

    # ======================================================
    # CORPORATE ACTION / M&A MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.CORPORATE_ACTION_MA
        in covered_families
    )

    assert (
        CatalystFamily.CORPORATE_ACTION_MA
        not in set(families)
    )

    # ======================================================
    # MANAGEMENT CAPITAL ALLOCATION MUST BE COVERED
    # ======================================================

    assert (
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
        in covered_families
    )

    assert (
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
        not in set(families)
    )

    # ======================================================
    # FINAL FAMILY COVERAGE
    # ======================================================

    assert (
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
        in covered_families
    )

    assert (
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
        not in set(families)
    )

    # ======================================================
    # EMPTY DEVELOPMENT QUEUE
    # ======================================================

    assert (
        queue
        == []
    )

    assert (
        uncovered_families
        == set()
    )

    assert (
        set(families)
        == set()
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Development Queue Exists        : PASS"
    )

    print(
        "Development Queue Count         : PASS"
    )

    print(
        "Development Record Type         : PASS"
    )

    print(
        "Family Integrity                : PASS"
    )

    print(
        "Priority Integrity              : PASS"
    )

    print(
        "Rationale Integrity              : PASS"
    )

    print(
        "Unique Development Families     : PASS"
    )

    print(
        "Covered Family Exclusion         : PASS"
    )

    print(
        "Uncovered Development Queue      : PASS"
    )

    print(
        "New Product / Platform Coverage : PASS"
    )

    print(
        "TAM Expansion Coverage           : PASS"
    )

    print(
        "Government Policy Coverage       : PASS"
    )

    print(
        "Fiscal / Tax Coverage            : PASS"
    )

    print(
        "Monetary / Liquidity Coverage    : PASS"
    )

    print(
        "Commodity Coverage               : PASS"
    )

    print(
        "Currency Coverage                : PASS"
    )

    print(
        "Trade / Import Substitution Coverage : PASS"
    )

    print(
        "Geopolitical Supply Chain Coverage   : PASS"
    )

    print(
        "Corporate Action / M&A Coverage      : PASS"
    )

    print(
        "Management Capital Allocation Coverage : PASS"
    )

    print(
        "Balance Sheet / Cash Flow Coverage : PASS"
    )

    print(
        "Empty Development Queue          : PASS"
    )

    print(
        "Zero Uncovered Families          : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST DEVELOPMENT QUEUE : PASS"
    )


if __name__ == "__main__":
    main()