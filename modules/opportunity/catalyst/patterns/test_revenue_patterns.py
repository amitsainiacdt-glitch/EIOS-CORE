"""
EIOS
Everest Investment Operating System

Revenue Growth Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.patterns.revenue_patterns import (
    REVENUE_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert len(REVENUE_PATTERNS) == 6

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in REVENUE_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

        assert (
            pattern.family
            == CatalystFamily.REVENUE_GROWTH
        )

    # ======================================================
    # REQUIRED STRUCTURE
    # ======================================================

    for pattern in REVENUE_PATTERNS:

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
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in REVENUE_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # EXPECTED PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-REVENUE-ACCELERATION",
        "PAT-REVENUE-CUSTOMER-COHORT-RAMP",
        "PAT-REVENUE-CROSS-SELL",
        "PAT-REVENUE-CHANNEL-EXPANSION",
        "PAT-REVENUE-GEOGRAPHIC-EXPANSION",
        "PAT-REVENUE-RECURRING-MIX",
    }

    assert (
        set(pattern_ids)
        == expected_ids
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Pattern Count                : PASS"
    )

    print(
        "Pattern Type Integrity       : PASS"
    )

    print(
        "Family Integrity             : PASS"
    )

    print(
        "Pattern Structure            : PASS"
    )

    print(
        "Unique Pattern IDs           : PASS"
    )

    print(
        "Expected Pattern IDs         : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS REVENUE GROWTH PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()