"""
EIOS
Everest Investment Operating System

Dedicated Pattern Tests:
    BALANCE_SHEET_CASH_FLOW

Purpose:
Validate the canonical Balance Sheet / Cash Flow catalyst
pattern family.

This test validates:

- Pattern count
- Pattern type integrity
- Family integrity
- Unique pattern IDs
- Pattern names
- Descriptions
- Mechanisms
- Trigger signals
- Leading indicators
- Confirmation indicators
- Transmission channels
- Typical time horizon
- Earnings channels
- Market mistake
- Second-order effects
- Disconfirming evidence
- Kill switches
- Canonical pattern IDs

Design Principles:

- Tests definitions only.
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

from modules.opportunity.catalyst.patterns.balance_sheet_cash_flow_patterns import (
    BALANCE_SHEET_CASH_FLOW_PATTERNS,
)


# ==========================================================
# EXPECTED CANONICAL PATTERN IDS
# ==========================================================

EXPECTED_PATTERN_IDS = {
    "PAT-BALANCE-SHEET-CASH-FLOW-WORKING-CAPITAL-RELEASE",
    "PAT-BALANCE-SHEET-CASH-FLOW-FREE-CASH-FLOW-INFLECTION",
    "PAT-BALANCE-SHEET-CASH-FLOW-CASH-CONVERSION-IMPROVEMENT",
    "PAT-BALANCE-SHEET-CASH-FLOW-BALANCE-SHEET-DELEVERAGING",
    "PAT-BALANCE-SHEET-CASH-FLOW-LIQUIDITY-INFLECTION",
    "PAT-BALANCE-SHEET-CASH-FLOW-CASH-FLOW-REINVESTMENT-CAPACITY",
}


# ==========================================================
# MAIN TEST
# ==========================================================

def main() -> None:

    patterns = (
        BALANCE_SHEET_CASH_FLOW_PATTERNS
    )


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
        == CatalystFamily.BALANCE_SHEET_CASH_FLOW
        for pattern in patterns
    )

    print(
        "Family Integrity                 : PASS"
    )


    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in patterns
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    print(
        "Unique Pattern IDs               : PASS"
    )


    # ======================================================
    # PATTERN NAMES
    # ======================================================

    assert all(
        isinstance(pattern.name, str)
        and pattern.name.strip()
        for pattern in patterns
    )

    print(
        "Pattern Names                    : PASS"
    )


    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    assert all(
        isinstance(pattern.description, str)
        and pattern.description.strip()
        for pattern in patterns
    )

    print(
        "Descriptions                     : PASS"
    )


    # ======================================================
    # MECHANISMS
    # ======================================================

    assert all(
        isinstance(pattern.mechanism, str)
        and pattern.mechanism.strip()
        for pattern in patterns
    )

    print(
        "Mechanisms                       : PASS"
    )


    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    assert all(
        isinstance(
            pattern.trigger_signals,
            list,
        )
        and len(pattern.trigger_signals) > 0
        for pattern in patterns
    )

    print(
        "Trigger Signals                  : PASS"
    )


    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    assert all(
        isinstance(
            pattern.leading_indicators,
            list,
        )
        and len(pattern.leading_indicators) > 0
        for pattern in patterns
    )

    print(
        "Leading Indicators               : PASS"
    )


    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    assert all(
        isinstance(
            pattern.confirmation_indicators,
            list,
        )
        and len(pattern.confirmation_indicators) > 0
        for pattern in patterns
    )

    print(
        "Confirmation Indicators          : PASS"
    )


    # ======================================================
    # TRANSMISSION CHANNELS
    # ======================================================

    assert all(
        isinstance(
            pattern.transmission_channels,
            list,
        )
        and len(pattern.transmission_channels) > 0
        for pattern in patterns
    )

    print(
        "Transmission Channels            : PASS"
    )


    # ======================================================
    # TYPICAL TIME HORIZON
    # ======================================================

    assert all(
        isinstance(
            pattern.typical_time_horizon,
            str,
        )
        and pattern.typical_time_horizon.strip()
        for pattern in patterns
    )

    print(
        "Typical Time Horizon             : PASS"
    )


    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    assert all(
        isinstance(
            pattern.earnings_channels,
            list,
        )
        and len(pattern.earnings_channels) > 0
        for pattern in patterns
    )

    print(
        "Earnings Channels                : PASS"
    )


    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    assert all(
        isinstance(
            pattern.market_mistake,
            str,
        )
        and pattern.market_mistake.strip()
        for pattern in patterns
    )

    print(
        "Market Mistake                   : PASS"
    )


    # ======================================================
    # SECOND ORDER EFFECTS
    # ======================================================

    assert all(
        isinstance(
            pattern.second_order_effects,
            list,
        )
        and len(pattern.second_order_effects) > 0
        for pattern in patterns
    )

    print(
        "Second Order Effects             : PASS"
    )


    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    assert all(
        isinstance(
            pattern.disconfirming_evidence,
            list,
        )
        and len(pattern.disconfirming_evidence) > 0
        for pattern in patterns
    )

    print(
        "Disconfirming Evidence            : PASS"
    )


    # ======================================================
    # KILL SWITCHES
    # ======================================================

    assert all(
        isinstance(
            pattern.kill_switch,
            str,
        )
        and pattern.kill_switch.strip()
        for pattern in patterns
    )

    print(
        "Kill Switches                    : PASS"
    )


    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    assert (
        set(pattern_ids)
        == EXPECTED_PATTERN_IDS
    )

    print(
        "Canonical Pattern IDs            : PASS"
    )


    # ======================================================
    # RESULT
    # ======================================================

    print()
    print(
        "---"
    )
    print()
    print(
        "EIOS BALANCE SHEET / CASH FLOW PATTERNS : PASS"
    )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()