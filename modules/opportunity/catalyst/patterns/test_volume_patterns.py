"""
EIOS
Everest Investment Operating System

Volume Growth Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.volume_patterns import (
    VOLUME_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert len(VOLUME_PATTERNS) == 6


    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in VOLUME_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )


    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in VOLUME_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.VOLUME_GROWTH
        )


    # ======================================================
    # PATTERN STRUCTURE
    # ======================================================

    for pattern in VOLUME_PATTERNS:

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

    ids = [
        pattern.pattern_id
        for pattern in VOLUME_PATTERNS
    ]

    assert (
        len(ids)
        == len(set(ids))
    )


    # ======================================================
    # EXPECTED PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-VOLUME-ORGANIC-ACCELERATION",
        "PAT-VOLUME-END-MARKET-EXPANSION",
        "PAT-VOLUME-USAGE-INTENSIFICATION",
        "PAT-VOLUME-REORDER-CYCLE",
        "PAT-VOLUME-CHANNEL-SELL-THROUGH",
        "PAT-VOLUME-HIGH-VOLUME-PRODUCT-SHIFT",
    }

    assert (
        set(ids)
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
        "EIOS VOLUME GROWTH PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()