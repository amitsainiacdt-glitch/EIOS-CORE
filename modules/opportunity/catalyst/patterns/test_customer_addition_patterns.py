"""
EIOS
Everest Investment Operating System

Customer Addition Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.customer_addition_patterns import (
    CUSTOMER_ADDITION_PATTERNS,
)


EXPECTED_PATTERN_IDS = {
    "PAT-CUSTOMER-ADDITION-STRATEGIC-CUSTOMER-WIN",
    "PAT-CUSTOMER-ADDITION-CUSTOMER-QUALIFICATION-INFLECTION",
    "PAT-CUSTOMER-ADDITION-CONCENTRATION-DILUTION",
    "PAT-CUSTOMER-ADDITION-REPEAT-ORDER-INFLECTION",
    "PAT-CUSTOMER-ADDITION-CUSTOMER-LIFETIME-VALUE-INFLECTION",
    "PAT-CUSTOMER-ADDITION-CUSTOMER-BASE-SCALE-INFLECTION",
}


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(CUSTOMER_ADDITION_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.CUSTOMER_ADDITION
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = {
        pattern.pattern_id
        for pattern in CUSTOMER_ADDITION_PATTERNS
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

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in CUSTOMER_ADDITION_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Pattern Count                  : PASS"
    )

    print(
        "Pattern Type                   : PASS"
    )

    print(
        "Family Integrity               : PASS"
    )

    print(
        "Unique Pattern IDs             : PASS"
    )

    print(
        "Pattern Names                  : PASS"
    )

    print(
        "Descriptions                   : PASS"
    )

    print(
        "Mechanisms                     : PASS"
    )

    print(
        "Trigger Signals               : PASS"
    )

    print(
        "Leading Indicators             : PASS"
    )

    print(
        "Confirmation Indicators        : PASS"
    )

    print(
        "Earnings Channels              : PASS"
    )

    print(
        "Market Mistake                 : PASS"
    )

    print(
        "Disconfirming Evidence         : PASS"
    )

    print(
        "Kill Switches                  : PASS"
    )

    print(
        "Canonical Pattern IDs          : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CUSTOMER ADDITION PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()