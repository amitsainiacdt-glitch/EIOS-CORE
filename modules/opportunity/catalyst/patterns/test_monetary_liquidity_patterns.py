"""
EIOS
Everest Investment Operating System

Monetary / Liquidity Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.monetary_liquidity_patterns import (
    MONETARY_LIQUIDITY_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(MONETARY_LIQUIDITY_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.MONETARY_LIQUIDITY
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in MONETARY_LIQUIDITY_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.transmission_channels

    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.typical_time_horizon

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.second_order_effects

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in MONETARY_LIQUIDITY_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-MONETARY-LIQUIDITY-POLICY-RATE-CHANGE",
        "PAT-MONETARY-LIQUIDITY-LIQUIDITY-INFUSION",
        "PAT-MONETARY-LIQUIDITY-CREDIT-CYCLE-EASING",
        "PAT-MONETARY-LIQUIDITY-TIGHTENING",
        "PAT-MONETARY-LIQUIDITY-TRANSMISSION-INFLECTION",
        "PAT-MONETARY-LIQUIDITY-VALUATION-RERATING",
    }

    assert (
        set(pattern_ids)
        == expected_ids
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
        "Disconfirming Evidence           : PASS"
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
        "EIOS MONETARY / LIQUIDITY PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()