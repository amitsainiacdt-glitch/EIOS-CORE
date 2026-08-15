"""
EIOS
Everest Investment Operating System

Government Policy Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.government_policy_patterns import (
    GOVERNMENT_POLICY_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(GOVERNMENT_POLICY_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.GOVERNMENT_POLICY
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in GOVERNMENT_POLICY_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.transmission_channels

    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.typical_time_horizon

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.second_order_effects

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in GOVERNMENT_POLICY_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-GOVERNMENT-POLICY-INCENTIVE",
        "PAT-GOVERNMENT-POLICY-PROGRAMME",
        "PAT-GOVERNMENT-POLICY-RESTRICTION",
        "PAT-GOVERNMENT-POLICY-IMPLEMENTATION",
        "PAT-GOVERNMENT-POLICY-BENEFICIARY-RERATING",
        "PAT-GOVERNMENT-POLICY-DURABILITY",
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
        "EIOS GOVERNMENT POLICY PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()