"""
EIOS
Everest Investment Operating System

Trade / Import Substitution Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.patterns.trade_import_substitution_patterns import (
    TRADE_IMPORT_SUBSTITUTION_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert len(TRADE_IMPORT_SUBSTITUTION_PATTERNS) == 6

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.TRADE_IMPORT_SUBSTITUTION
        )

    # ======================================================
    # UNIQUE IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # NAMES
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.confirmation_indicators

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.transmission_channels

    # ======================================================
    # TIME HORIZON
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.typical_time_horizon

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.market_mistake

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.second_order_effects

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in TRADE_IMPORT_SUBSTITUTION_PATTERNS:
        assert pattern.kill_switch

    # ======================================================
    # CANONICAL IDS
    # ======================================================

    expected_ids = {
        "PAT-TRADE-IMPORT-SUBSTITUTION-IMPORT-REPLACEMENT",
        "PAT-TRADE-IMPORT-SUBSTITUTION-DOMESTIC-CAPACITY",
        "PAT-TRADE-IMPORT-SUBSTITUTION-TARIFF-ADVANTAGE",
        "PAT-TRADE-IMPORT-SUBSTITUTION-LOCALISATION",
        "PAT-TRADE-IMPORT-SUBSTITUTION-CUSTOMER-SHIFT",
        "PAT-TRADE-IMPORT-SUBSTITUTION-COMPETITIVE-COST-ADVANTAGE",
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
        "Disconfirming Evidence            : PASS"
    )

    print(
        "Kill Switches                    : PASS"
    )

    print(
        "Canonical Pattern IDs             : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS TRADE / IMPORT SUBSTITUTION PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()
