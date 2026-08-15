"""
EIOS
Everest Investment Operating System

Currency Catalyst Pattern Tests

Purpose:
Validate the canonical Currency catalyst pattern definitions.

Design Principles:
- Pattern definitions are validated structurally.
- No scoring.
- No ranking.
- No valuation.
- No investment decision logic.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.currency_patterns import (
    CURRENCY_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert len(CURRENCY_PATTERNS) == 6

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.CURRENCY
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in CURRENCY_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_pattern_ids = {
        "PAT-CURRENCY-DEPRECIATION",
        "PAT-CURRENCY-APPRECIATION",
        "PAT-CURRENCY-EXPORT-COMPETITIVENESS",
        "PAT-CURRENCY-INPUT-COST-INFLECTION",
        "PAT-CURRENCY-TRANSLATION-INFLECTION",
        "PAT-CURRENCY-HEDGING-INFLECTION",
    }

    assert (
        set(pattern_ids)
        == expected_pattern_ids
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.name
        assert isinstance(
            pattern.name,
            str,
        )

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.description
        assert isinstance(
            pattern.description,
            str,
        )

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.mechanism
        assert isinstance(
            pattern.mechanism,
            str,
        )

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.trigger_signals
        assert isinstance(
            pattern.trigger_signals,
            list,
        )

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.leading_indicators
        assert isinstance(
            pattern.leading_indicators,
            list,
        )

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.confirmation_indicators
        assert isinstance(
            pattern.confirmation_indicators,
            list,
        )

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.transmission_channels
        assert isinstance(
            pattern.transmission_channels,
            list,
        )

    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.typical_time_horizon
        assert isinstance(
            pattern.typical_time_horizon,
            str,
        )

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.earnings_channels
        assert isinstance(
            pattern.earnings_channels,
            list,
        )

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.market_mistake
        assert isinstance(
            pattern.market_mistake,
            str,
        )

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.second_order_effects
        assert isinstance(
            pattern.second_order_effects,
            list,
        )

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.disconfirming_evidence
        assert isinstance(
            pattern.disconfirming_evidence,
            list,
        )

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in CURRENCY_PATTERNS:

        assert pattern.kill_switch
        assert isinstance(
            pattern.kill_switch,
            str,
        )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Pattern Count                    : PASS"
    )

    print(
        "Pattern Type Integrity           : PASS"
    )

    print(
        "Family Integrity                 : PASS"
    )

    print(
        "Unique Pattern IDs               : PASS"
    )

    print(
        "Pattern Names                    : PASS"
    )

    print(
        "Descriptions                     : PASS"
    )

    print(
        "Mechanisms                       : PASS"
    )

    print(
        "Trigger Signals                  : PASS"
    )

    print(
        "Leading Indicators               : PASS"
    )

    print(
        "Confirmation Indicators          : PASS"
    )

    print(
        "Transmission Channels            : PASS"
    )

    print(
        "Typical Time Horizon             : PASS"
    )

    print(
        "Earnings Channels                : PASS"
    )

    print(
        "Market Mistake                   : PASS"
    )

    print(
        "Second Order Effects             : PASS"
    )

    print(
        "Disconfirming Evidence            : PASS"
    )

    print(
        "Kill Switches                    : PASS"
    )

    print(
        "Canonical Pattern IDs            : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CURRENCY PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()