"""
EIOS
Everest Investment Operating System

Catalyst Pattern Module Test

Family: GEOPOLITICAL_SUPPLY_CHAIN
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.geopolitical_supply_chain_patterns import (
    GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern
        in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_pattern_ids = {

        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-RELOCATION",

        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "SOURCING-DIVERSIFICATION",

        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "TRADE-ROUTE-DISRUPTION",

        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "SANCTIONS-EXPORT-CONTROL",

        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "STRATEGIC-INVENTORY",

        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "REGIONAL-LOCALISATION",
    }

    assert (
        set(pattern_ids)
        == expected_pattern_ids
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.trigger_signals
        assert len(pattern.trigger_signals) > 0

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.leading_indicators
        assert len(pattern.leading_indicators) > 0

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.confirmation_indicators
        assert len(pattern.confirmation_indicators) > 0

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.transmission_channels
        assert len(pattern.transmission_channels) > 0

    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.typical_time_horizon

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.earnings_channels
        assert len(pattern.earnings_channels) > 0

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.second_order_effects
        assert len(pattern.second_order_effects) > 0

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.disconfirming_evidence
        assert len(pattern.disconfirming_evidence) > 0

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS:

        assert pattern.kill_switch

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
        "EIOS GEOPOLITICAL SUPPLY CHAIN PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()