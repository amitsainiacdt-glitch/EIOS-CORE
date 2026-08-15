"""
EIOS
Everest Investment Operating System

Market Recognition / Expectation Reset Catalyst Pattern Tests
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.market_recognition_expectation_reset_patterns import (
    MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(
            MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS
        )
        == 6
    )


    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in (
        MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS
    ):

        assert isinstance(
            pattern,
            CatalystPattern,
        )


    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in (
        MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS
    ):

        assert (
            pattern.family
            == CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET
        )


    # ======================================================
    # PATTERN STRUCTURE
    # ======================================================

    for pattern in (
        MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS
    ):

        assert pattern.pattern_id
        assert pattern.family
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
        for pattern in (
            MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS
        )
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )


    # ======================================================
    # EXPECTED PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-MARKET-EXPECTATION-EARNINGS-RESET",
        "PAT-MARKET-EXPECTATION-GROWTH-REACCELERATION",
        "PAT-MARKET-EXPECTATION-DURABILITY-RESET",
        "PAT-MARKET-EXPECTATION-RUNWAY-EXTENSION",
        "PAT-MARKET-EXPECTATION-CONSENSUS-CONVERGENCE",
        "PAT-MARKET-EXPECTATION-THESIS-VALIDATION",
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
        "EIOS MARKET RECOGNITION EXPECTATION RESET PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()