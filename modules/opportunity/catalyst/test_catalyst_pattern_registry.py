"""
EIOS
Everest Investment Operating System

Catalyst Pattern Registry Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_pattern_registry import (
    CatalystPatternRegistry,
)


def main() -> None:

    # ======================================================
    # REGISTRY COUNT
    # ======================================================

    assert (
        CatalystPatternRegistry.count()
        == 98
    )

    # ======================================================
    # REGISTRY CONTENT
    # ======================================================

    patterns = (
        CatalystPatternRegistry.all()
    )

    assert (
        len(patterns)
        == 98
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in patterns:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # PATTERN NAME INTEGRITY
    # ======================================================

    for pattern in patterns:

        assert pattern.name

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in patterns:

        assert (
            pattern.family
            in CatalystFamily
        )

    # ======================================================
    # PATTERN RETRIEVAL
    # ======================================================

    for pattern in patterns:

        retrieved = (
            CatalystPatternRegistry.get(
                pattern.pattern_id
            )
        )

        assert (
            retrieved
            is pattern
        )

    # ======================================================
    # FAMILY LOOKUP
    # ======================================================

    family_counts = {}

    for family in CatalystFamily:

        family_counts[family] = len(
            CatalystPatternRegistry.get_by_family(
                family
            )
        )

    # ======================================================
    # COMPLETED FAMILY COUNTS
    # ======================================================

    assert (
        family_counts[
            CatalystFamily.CAPACITY_EXPANSION
        ]
        == 2
    )

    assert (
        family_counts[
            CatalystFamily.CAPACITY_UTILISATION
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.ORDER_CONTRACT
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.CUSTOMER_ADDITION
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.MARKET_SHARE
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.SUPPLY_CONSTRAINT
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.REGULATORY_CHANGE
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.REVENUE_GROWTH
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.VOLUME_GROWTH
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.PRICING
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.MARGIN_EXPANSION
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.TECHNOLOGY_ADOPTION
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.PRODUCT_MIX
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.COST_REDUCTION
        ]
        == 6
    )

    assert (
        family_counts[
            CatalystFamily.OPERATING_LEVERAGE
        ]
        == 6
    )

    # ======================================================
    # TOTAL FAMILY COUNT CONSISTENCY
    # ======================================================

    assert (
        sum(
            family_counts.values()
        )
        == CatalystPatternRegistry.count()
    )

    # ======================================================
    # CAPACITY UTILISATION FAMILY
    # ======================================================

    capacity_utilisation_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.CAPACITY_UTILISATION
        )
    )

    assert (
        len(capacity_utilisation_patterns)
        == 6
    )

    expected_capacity_utilisation_ids = {
        "PAT-CAPACITY-UTILISATION-UTILISATION-INFLECTION",
        "PAT-CAPACITY-UTILISATION-FIXED-COST-ABSORPTION",
        "PAT-CAPACITY-UTILISATION-MARGIN-INFLECTION",
        "PAT-CAPACITY-UTILISATION-UNDERUTILISED-ASSET-REACTIVATION",
        "PAT-CAPACITY-UTILISATION-CONSTRAINT-RELEASE",
        "PAT-CAPACITY-UTILISATION-CAPITAL-EFFICIENCY-INFLECTION",
    }

    actual_capacity_utilisation_ids = {
        pattern.pattern_id
        for pattern in capacity_utilisation_patterns
    }

    assert (
        actual_capacity_utilisation_ids
        == expected_capacity_utilisation_ids
    )

    # ======================================================
    # CUSTOMER ADDITION FAMILY
    # ======================================================

    customer_addition_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.CUSTOMER_ADDITION
        )
    )

    assert (
        len(customer_addition_patterns)
        == 6
    )

    expected_customer_addition_ids = {
        "PAT-CUSTOMER-ADDITION-STRATEGIC-CUSTOMER-WIN",
        "PAT-CUSTOMER-ADDITION-CUSTOMER-QUALIFICATION-INFLECTION",
        "PAT-CUSTOMER-ADDITION-CONCENTRATION-DILUTION",
        "PAT-CUSTOMER-ADDITION-REPEAT-ORDER-INFLECTION",
        "PAT-CUSTOMER-ADDITION-CUSTOMER-LIFETIME-VALUE-INFLECTION",
        "PAT-CUSTOMER-ADDITION-CUSTOMER-BASE-SCALE-INFLECTION",
    }

    actual_customer_addition_ids = {
        pattern.pattern_id
        for pattern in customer_addition_patterns
    }

    assert (
        actual_customer_addition_ids
        == expected_customer_addition_ids
    )

    # ======================================================
    # MARKET SHARE FAMILY
    # ======================================================

    market_share_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.MARKET_SHARE
        )
    )

    assert (
        len(market_share_patterns)
        == 6
    )

    expected_market_share_ids = {
        "PAT-MARKET-SHARE-ORGANIC-SHARE-GAIN",
        "PAT-MARKET-SHARE-COMPETITOR-SHARE-CAPTURE",
        "PAT-MARKET-SHARE-DISTRIBUTION-LED-GAIN",
        "PAT-MARKET-SHARE-PRODUCT-LED-GAIN",
        "PAT-MARKET-SHARE-CAPACITY-CONSTRAINED-GAIN",
        "PAT-MARKET-SHARE-SHARE-GAIN-COMPOUNDING",
    }

    actual_market_share_ids = {
        pattern.pattern_id
        for pattern in market_share_patterns
    }

    assert (
        actual_market_share_ids
        == expected_market_share_ids
    )

    # ======================================================
    # INDUSTRY CAPITAL CYCLE FAMILY
    # ======================================================

    industry_capital_cycle_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        )
    )

    assert (
        len(industry_capital_cycle_patterns)
        == 6
    )

    expected_industry_capital_cycle_ids = {
        "PAT-CAPITAL-CYCLE-CAPACITY-DISCIPLINE-INFLECTION",
        "PAT-CAPITAL-CYCLE-DEMAND-LED-CAPACITY-ABSORPTION",
        "PAT-CAPITAL-CYCLE-CAPEX-CYCLE-TURN",
        "PAT-CAPITAL-CYCLE-UNDERINVESTMENT-SUPPLY-TIGHTENING",
        "PAT-CAPITAL-CYCLE-PEAK-CAPACITY-UTILISATION",
        "PAT-CAPITAL-CYCLE-CAPITAL-RETURNS-INFLECTION",
    }

    actual_industry_capital_cycle_ids = {
        pattern.pattern_id
        for pattern in industry_capital_cycle_patterns
    }

    assert (
        actual_industry_capital_cycle_ids
        == expected_industry_capital_cycle_ids
    )

    # ======================================================
    # SUPPLY CONSTRAINT FAMILY
    # ======================================================

    supply_constraint_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.SUPPLY_CONSTRAINT
        )
    )

    assert (
        len(supply_constraint_patterns)
        == 6
    )

    expected_supply_constraint_ids = {
        "PAT-SUPPLY-CONSTRAINT-CAPACITY-SHORTAGE",
        "PAT-SUPPLY-CONSTRAINT-LEAD-TIME-EXTENSION",
        "PAT-SUPPLY-CONSTRAINT-INVENTORY-DEPLETION",
        "PAT-SUPPLY-CONSTRAINT-SUPPLIER-CONSOLIDATION",
        "PAT-SUPPLY-CONSTRAINT-RAW-MATERIAL-SCARCITY",
        "PAT-SUPPLY-CONSTRAINT-PRICING-POWER-INFLECTION",
    }

    actual_supply_constraint_ids = {
        pattern.pattern_id
        for pattern in supply_constraint_patterns
    }

    assert (
        actual_supply_constraint_ids
        == expected_supply_constraint_ids
    )

    # ======================================================
    # PRODUCT MIX FAMILY
    # ======================================================

    product_mix_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.PRODUCT_MIX
        )
    )

    assert (
        len(product_mix_patterns)
        == 6
    )

    expected_product_mix_ids = {
        "PAT-PRODUCT-MIX-PREMIUM-TIER-MIGRATION",
        "PAT-PRODUCT-MIX-CATEGORY-MIGRATION",
        "PAT-PRODUCT-MIX-NEW-PRODUCT-INFLECTION",
        "PAT-PRODUCT-MIX-PRODUCT-RATIONALISATION",
        "PAT-PRODUCT-MIX-SOLUTION-BUNDLE-MIGRATION",
        "PAT-PRODUCT-MIX-WINNER-CONCENTRATION",
    }

    actual_product_mix_ids = {
        pattern.pattern_id
        for pattern in product_mix_patterns
    }

    assert (
        actual_product_mix_ids
        == expected_product_mix_ids
    )

    # ======================================================
    # COST REDUCTION FAMILY
    # ======================================================

    cost_reduction_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.COST_REDUCTION
        )
    )

    assert (
        len(cost_reduction_patterns)
        == 6
    )

    expected_cost_reduction_ids = {
        "PAT-COST-REDUCTION-INPUT-COST-DECLINE",
        "PAT-COST-REDUCTION-PROCUREMENT-EFFICIENCY",
        "PAT-COST-REDUCTION-AUTOMATION",
        "PAT-COST-REDUCTION-OPERATING-EFFICIENCY",
        "PAT-COST-REDUCTION-MIX-AND-SOURCING",
        "PAT-COST-REDUCTION-HEADCOUNT-PRODUCTIVITY",
    }

    actual_cost_reduction_ids = {
        pattern.pattern_id
        for pattern in cost_reduction_patterns
    }

    assert (
        actual_cost_reduction_ids
        == expected_cost_reduction_ids
    )

    # ======================================================
    # OPERATING LEVERAGE FAMILY
    # ======================================================

    operating_leverage_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.OPERATING_LEVERAGE
        )
    )

    assert (
        len(operating_leverage_patterns)
        == 6
    )

    expected_operating_leverage_ids = {
        "PAT-OPERATING-LEVERAGE-FIXED-COST-ABSORPTION",
        "PAT-OPERATING-LEVERAGE-INCREMENTAL-MARGIN-INFLECTION",
        "PAT-OPERATING-LEVERAGE-UTILISATION-TO-LEVERAGE",
        "PAT-OPERATING-LEVERAGE-REVENUE-THRESHOLD-CROSSING",
        "PAT-OPERATING-LEVERAGE-VOLUME-TO-EARNINGS-AMPLIFICATION",
        "PAT-OPERATING-LEVERAGE-EPS-INFLECTION",
    }

    actual_operating_leverage_ids = {
        pattern.pattern_id
        for pattern in operating_leverage_patterns
    }

    assert (
        actual_operating_leverage_ids
        == expected_operating_leverage_ids
    )

    # ======================================================
    # MARKET RECOGNITION FAMILY
    # ======================================================

    market_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET
        )
    )

    assert (
        len(market_patterns)
        == 6
    )

    expected_market_ids = {
        "PAT-MARKET-EXPECTATION-EARNINGS-RESET",
        "PAT-MARKET-EXPECTATION-GROWTH-REACCELERATION",
        "PAT-MARKET-EXPECTATION-DURABILITY-RESET",
        "PAT-MARKET-EXPECTATION-RUNWAY-EXTENSION",
        "PAT-MARKET-EXPECTATION-CONSENSUS-CONVERGENCE",
        "PAT-MARKET-EXPECTATION-THESIS-VALIDATION",
    }

    actual_market_ids = {
        pattern.pattern_id
        for pattern in market_patterns
    }

    assert (
        actual_market_ids
        == expected_market_ids
    )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in patterns
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Registry Count                    : PASS"
    )

    print(
        "Pattern Retrieval                 : PASS"
    )

    print(
        "Pattern Name Integrity            : PASS"
    )

    print(
        "Family Integrity                  : PASS"
    )

    print(
        "Family Lookup                     : PASS"
    )

    print(
        "Capacity Utilisation Coverage     : PASS"
    )

    print(
        "Capacity Utilisation Pattern IDs  : PASS"
    )

    print(
        "Customer Addition Coverage        : PASS"
    )

    print(
        "Customer Addition Pattern IDs     : PASS"
    )

    print(
        "Market Share Coverage             : PASS"
    )

    print(
        "Market Share Pattern IDs          : PASS"
    )

    print(
        "Industry Capital Cycle Coverage   : PASS"
    )

    print(
        "Industry Capital Cycle Pattern IDs: PASS"
    )

    print(
        "Supply Constraint Coverage        : PASS"
    )

    print(
        "Supply Constraint Pattern IDs     : PASS"
    )

    print(
        "Product Mix Coverage              : PASS"
    )

    print(
        "Product Mix Pattern IDs           : PASS"
    )

    print(
        "Cost Reduction Coverage           : PASS"
    )

    print(
        "Cost Reduction Pattern IDs        : PASS"
    )

    print(
        "Operating Leverage Coverage       : PASS"
    )

    print(
        "Operating Leverage Pattern IDs    : PASS"
    )

    print(
        "Market Recognition Coverage       : PASS"
    )

    print(
        "Pattern Structure                 : PASS"
    )

    print(
        "Unique Pattern IDs                : PASS"
    )

    print(
        "Family Count Consistency          : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST PATTERN REGISTRY : PASS"
    )


if __name__ == "__main__":
    main()