"""
EIOS
Everest Investment Operating System

Commodity Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.commodity_patterns import (
    COMMODITY_PATTERNS,
)


EXPECTED_PATTERN_IDS = {
    "PAT-COMMODITY-PRICE-INFLECTION",
    "PAT-COMMODITY-SUPPLY-CONSTRAINT",
    "PAT-COMMODITY-DEMAND-INFLECTION",
    "PAT-COMMODITY-REALISATION-INFLECTION",
    "PAT-COMMODITY-INVENTORY-CYCLE",
    "PAT-COMMODITY-SPREAD-COST-ADVANTAGE",
}


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert len(COMMODITY_PATTERNS) == 6

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.COMMODITY
        )

    # ======================================================
    # UNIQUE PATTERN IDs
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in COMMODITY_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # CANONICAL PATTERN IDs
    # ======================================================

    assert (
        set(pattern_ids)
        == EXPECTED_PATTERN_IDS
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.name
        assert isinstance(
            pattern.name,
            str,
        )

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.description
        assert isinstance(
            pattern.description,
            str,
        )

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.mechanism
        assert isinstance(
            pattern.mechanism,
            str,
        )

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.trigger_signals
        assert isinstance(
            pattern.trigger_signals,
            list,
        )

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.leading_indicators
        assert isinstance(
            pattern.leading_indicators,
            list,
        )

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.confirmation_indicators
        assert isinstance(
            pattern.confirmation_indicators,
            list,
        )

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.transmission_channels
        assert isinstance(
            pattern.transmission_channels,
            list,
        )

    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.typical_time_horizon
        assert isinstance(
            pattern.typical_time_horizon,
            str,
        )

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.earnings_channels
        assert isinstance(
            pattern.earnings_channels,
            list,
        )

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.market_mistake
        assert isinstance(
            pattern.market_mistake,
            str,
        )

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.second_order_effects
        assert isinstance(
            pattern.second_order_effects,
            list,
        )

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

        assert pattern.disconfirming_evidence
        assert isinstance(
            pattern.disconfirming_evidence,
            list,
        )

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in COMMODITY_PATTERNS:

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
        "EIOS COMMODITY PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()