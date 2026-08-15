"""
EIOS
Everest Investment Operating System

TAM Expansion Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.tam_expansion_patterns import (
    TAM_EXPANSION_PATTERNS,
)


EXPECTED_PATTERN_IDS = {
    "PAT-TAM-EXPANSION-NEW-APPLICATION",
    "PAT-TAM-EXPANSION-GEOGRAPHIC",
    "PAT-TAM-EXPANSION-NEW-CUSTOMER-CLASS",
    "PAT-TAM-EXPANSION-MARKET-PENETRATION",
    "PAT-TAM-EXPANSION-MARKET-REASSESSMENT",
    "PAT-TAM-EXPANSION-PLATFORM-ADJACENCY",
}


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(TAM_EXPANSION_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.TAM_EXPANSION
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = {
        pattern.pattern_id
        for pattern in TAM_EXPANSION_PATTERNS
    }

    assert (
        len(pattern_ids)
        == 6
    )

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    assert (
        pattern_ids
        == EXPECTED_PATTERN_IDS
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.name
        assert isinstance(
            pattern.name,
            str,
        )

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.description
        assert isinstance(
            pattern.description,
            str,
        )

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.mechanism
        assert isinstance(
            pattern.mechanism,
            str,
        )

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.trigger_signals
        assert all(
            isinstance(
                signal,
                str,
            )
            and signal
            for signal
            in pattern.trigger_signals
        )

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.leading_indicators
        assert all(
            isinstance(
                indicator,
                str,
            )
            and indicator
            for indicator
            in pattern.leading_indicators
        )

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.confirmation_indicators
        assert all(
            isinstance(
                indicator,
                str,
            )
            and indicator
            for indicator
            in pattern.confirmation_indicators
        )

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.transmission_channels
        assert all(
            isinstance(
                channel,
                str,
            )
            and channel
            for channel
            in pattern.transmission_channels
        )

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.earnings_channels
        assert all(
            isinstance(
                channel,
                str,
            )
            and channel
            for channel
            in pattern.earnings_channels
        )

    # ======================================================
    # TIME HORIZON
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.typical_time_horizon
        assert isinstance(
            pattern.typical_time_horizon,
            str,
        )

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.market_mistake
        assert isinstance(
            pattern.market_mistake,
            str,
        )

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.second_order_effects
        assert all(
            isinstance(
                effect,
                str,
            )
            and effect
            for effect
            in pattern.second_order_effects
        )

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

        assert pattern.disconfirming_evidence
        assert all(
            isinstance(
                evidence,
                str,
            )
            and evidence
            for evidence
            in pattern.disconfirming_evidence
        )

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in TAM_EXPANSION_PATTERNS:

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
        "EIOS TAM EXPANSION PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()