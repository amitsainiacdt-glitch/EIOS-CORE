"""
EIOS
Everest Investment Operating System

Catalyst Pattern Registry Test
"""


from modules.opportunity.catalyst.catalyst_pattern_registry import (
    CatalystPatternRegistry,
)


from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


def main() -> None:

    # ======================================================
    # REGISTRY COUNT
    # ======================================================

    assert (
        CatalystPatternRegistry.count()
        == 20
    )

    # ======================================================
    # GET BY ID
    # ======================================================

    brownfield = (
        CatalystPatternRegistry.get(
            "PAT-CAPACITY-BROWNFIELD"
        )
    )

    debottleneck = (
        CatalystPatternRegistry.get(
            "PAT-CAPACITY-DEBOTTLENECK"
        )
    )

    revenue_acceleration = (
        CatalystPatternRegistry.get(
            "PAT-REVENUE-ACCELERATION"
        )
    )

    assert (
        brownfield.name
        == "Brownfield Capacity Expansion"
    )

    assert (
        debottleneck.name
        == "Capacity Debottlenecking"
    )

    assert (
        revenue_acceleration.name
        == "Revenue Growth Acceleration"
    )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    assert (
        brownfield.family
        == CatalystFamily.CAPACITY_EXPANSION
    )

    assert (
        debottleneck.family
        == CatalystFamily.CAPACITY_EXPANSION
    )

    assert (
        revenue_acceleration.family
        == CatalystFamily.REVENUE_GROWTH
    )

    # ======================================================
    # FAMILY LOOKUP
    # ======================================================

    capacity_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.CAPACITY_EXPANSION
        )
    )

    order_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.ORDER_CONTRACT
        )
    )

    regulatory_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.REGULATORY_CHANGE
        )
    )

    revenue_patterns = (
        CatalystPatternRegistry.get_by_family(
            CatalystFamily.REVENUE_GROWTH
        )
    )

    assert len(capacity_patterns) == 2

    assert len(order_patterns) == 6

    assert len(regulatory_patterns) == 6

    assert len(revenue_patterns) == 6

    # ======================================================
    # ALL PATTERN INTEGRITY
    # ======================================================

    all_patterns = (
        CatalystPatternRegistry.all()
    )

    assert len(all_patterns) == 20

    for pattern in all_patterns:

        assert pattern.pattern_id

        assert pattern.name

        assert pattern.description

        assert pattern.trigger_signals

        assert pattern.mechanism

        assert pattern.transmission_channels

        assert pattern.leading_indicators

        assert pattern.confirmation_indicators

        assert pattern.typical_time_horizon

        assert pattern.earnings_channels

        assert pattern.market_mistake

        assert pattern.second_order_effects

        assert pattern.disconfirming_evidence

        assert pattern.kill_switch

    # ======================================================
    # UNIQUE IDS
    # ======================================================

    ids = [
        pattern.pattern_id
        for pattern in all_patterns
    ]

    assert (
        len(ids)
        == len(set(ids))
    )

    # ======================================================
    # FAMILY COUNT CONSISTENCY
    # ======================================================

    covered_pattern_count = (
        len(capacity_patterns)
        + len(order_patterns)
        + len(regulatory_patterns)
        + len(revenue_patterns)
    )

    assert (
        covered_pattern_count
        == CatalystPatternRegistry.count()
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Registry Count              : PASS"
    )

    print(
        "Pattern Retrieval           : PASS"
    )

    print(
        "Family Integrity            : PASS"
    )

    print(
        "Family Lookup               : PASS"
    )

    print(
        "Pattern Structure            : PASS"
    )

    print(
        "Unique Pattern IDs           : PASS"
    )

    print(
        "Family Count Consistency     : PASS"
    )

    print(
        "Revenue Growth Coverage     : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST PATTERN REGISTRY : PASS"
    )


if __name__ == "__main__":
    main()