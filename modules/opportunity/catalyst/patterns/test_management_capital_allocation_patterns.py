"""
EIOS
Everest Investment Operating System

Catalyst Pattern Test

Family:
    MANAGEMENT_CAPITAL_ALLOCATION

Purpose:
    Validate the canonical Management Capital Allocation
    catalyst pattern definitions.

This test validates structure and integrity only.

It does not perform:
    - scoring
    - ranking
    - valuation
    - investment decisions
"""


from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.management_capital_allocation_patterns import (
    MANAGEMENT_CAPITAL_ALLOCATION_PATTERNS,
)


# ==========================================================
# EXPECTED CANONICAL PATTERN IDS
# ==========================================================

EXPECTED_PATTERN_IDS = {
    "PAT-MANAGEMENT-CAPITAL-ALLOCATION-CAPITAL-DEPLOYMENT-INFLECTION",
    "PAT-MANAGEMENT-CAPITAL-ALLOCATION-HIGH-RETURN-REINVESTMENT",
    "PAT-MANAGEMENT-CAPITAL-ALLOCATION-SHAREHOLDER-DISTRIBUTION-INFLECTION",
    "PAT-MANAGEMENT-CAPITAL-ALLOCATION-DEBT-REDUCTION-BALANCE-SHEET-REPAIR",
    "PAT-MANAGEMENT-CAPITAL-ALLOCATION-ACCRETIVE-ACQUISITION",
    "PAT-MANAGEMENT-CAPITAL-ALLOCATION-DIVESTMENT-CAPITAL-RECYCLING",
}


# ==========================================================
# EXPECTED PATTERN NAMES
# ==========================================================

EXPECTED_PATTERN_NAMES = {
    "Capital Deployment Inflection",
    "High-Return Reinvestment",
    "Shareholder Distribution Inflection",
    "Debt Reduction / Balance-Sheet Repair",
    "Accretive Acquisition Capital Allocation",
    "Divestment / Capital Recycling",
}


# ==========================================================
# MAIN TEST
# ==========================================================

def main() -> None:

    patterns = MANAGEMENT_CAPITAL_ALLOCATION_PATTERNS

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(patterns)
        == 6
    )

    print(
        "Pattern Count                    : PASS"
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    assert all(
        isinstance(
            pattern,
            CatalystPattern,
        )
        for pattern in patterns
    )

    print(
        "Pattern Type Integrity           : PASS"
    )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    assert all(
        pattern.family
        == CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
        for pattern in patterns
    )

    print(
        "Family Integrity                 : PASS"
    )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = {
        pattern.pattern_id
        for pattern in patterns
    }

    assert (
        len(pattern_ids)
        == 6
    )

    print(
        "Unique Pattern IDs               : PASS"
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    assert all(
        pattern.name
        and isinstance(
            pattern.name,
            str,
        )
        for pattern in patterns
    )

    assert (
        {
            pattern.name
            for pattern in patterns
        }
        == EXPECTED_PATTERN_NAMES
    )

    print(
        "Pattern Names                    : PASS"
    )

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    assert all(
        pattern.description
        and isinstance(
            pattern.description,
            str,
        )
        for pattern in patterns
    )

    print(
        "Descriptions                     : PASS"
    )

    # ======================================================
    # MECHANISMS
    # ======================================================

    assert all(
        pattern.mechanism
        and isinstance(
            pattern.mechanism,
            str,
        )
        for pattern in patterns
    )

    print(
        "Mechanisms                       : PASS"
    )

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    assert all(
        pattern.trigger_signals
        and isinstance(
            pattern.trigger_signals,
            list,
        )
        and all(
            isinstance(
                signal,
                str,
            )
            and signal.strip()
            for signal in pattern.trigger_signals
        )
        for pattern in patterns
    )

    print(
        "Trigger Signals                  : PASS"
    )

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    assert all(
        pattern.leading_indicators
        and isinstance(
            pattern.leading_indicators,
            list,
        )
        and all(
            isinstance(
                indicator,
                str,
            )
            and indicator.strip()
            for indicator in pattern.leading_indicators
        )
        for pattern in patterns
    )

    print(
        "Leading Indicators               : PASS"
    )

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    assert all(
        pattern.confirmation_indicators
        and isinstance(
            pattern.confirmation_indicators,
            list,
        )
        and all(
            isinstance(
                indicator,
                str,
            )
            and indicator.strip()
            for indicator in pattern.confirmation_indicators
        )
        for pattern in patterns
    )

    print(
        "Confirmation Indicators          : PASS"
    )

    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    assert all(
        pattern.transmission_channels
        and isinstance(
            pattern.transmission_channels,
            list,
        )
        and all(
            isinstance(
                channel,
                str,
            )
            and channel.strip()
            for channel in pattern.transmission_channels
        )
        for pattern in patterns
    )

    print(
        "Transmission Channels            : PASS"
    )

    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    assert all(
        pattern.typical_time_horizon
        and isinstance(
            pattern.typical_time_horizon,
            str,
        )
        for pattern in patterns
    )

    print(
        "Typical Time Horizon             : PASS"
    )

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    assert all(
        pattern.earnings_channels
        and isinstance(
            pattern.earnings_channels,
            list,
        )
        and all(
            isinstance(
                channel,
                str,
            )
            and channel.strip()
            for channel in pattern.earnings_channels
        )
        for pattern in patterns
    )

    print(
        "Earnings Channels                : PASS"
    )

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    assert all(
        pattern.market_mistake
        and isinstance(
            pattern.market_mistake,
            str,
        )
        for pattern in patterns
    )

    print(
        "Market Mistake                   : PASS"
    )

    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    assert all(
        pattern.second_order_effects
        and isinstance(
            pattern.second_order_effects,
            list,
        )
        and all(
            isinstance(
                effect,
                str,
            )
            and effect.strip()
            for effect in pattern.second_order_effects
        )
        for pattern in patterns
    )

    print(
        "Second Order Effects             : PASS"
    )

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    assert all(
        pattern.disconfirming_evidence
        and isinstance(
            pattern.disconfirming_evidence,
            list,
        )
        and all(
            isinstance(
                evidence,
                str,
            )
            and evidence.strip()
            for evidence in pattern.disconfirming_evidence
        )
        for pattern in patterns
    )

    print(
        "Disconfirming Evidence            : PASS"
    )

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    assert all(
        pattern.kill_switch
        and isinstance(
            pattern.kill_switch,
            str,
        )
        for pattern in patterns
    )

    print(
        "Kill Switches                    : PASS"
    )

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    assert (
        pattern_ids
        == EXPECTED_PATTERN_IDS
    )

    print(
        "Canonical Pattern IDs            : PASS"
    )

    # ======================================================
    # FINAL RESULT
    # ======================================================

    print()
    print(
        "---"
    )
    print()
    print(
        "EIOS MANAGEMENT CAPITAL ALLOCATION PATTERNS : PASS"
    )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()