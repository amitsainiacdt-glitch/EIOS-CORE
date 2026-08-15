"""
EIOS
Everest Investment Operating System

Cost Reduction Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.cost_reduction_patterns import (
    COST_REDUCTION_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(COST_REDUCTION_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.COST_REDUCTION
        )

    # ======================================================
    # PATTERN ID INTEGRITY
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in COST_REDUCTION_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAME INTEGRITY
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTION INTEGRITY
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISM INTEGRITY
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in COST_REDUCTION_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL IDS
    # ======================================================

    expected_ids = {
        "PAT-COST-REDUCTION-INPUT-COST-DECLINE",
        "PAT-COST-REDUCTION-PROCUREMENT-EFFICIENCY",
        "PAT-COST-REDUCTION-AUTOMATION",
        "PAT-COST-REDUCTION-OPERATING-EFFICIENCY",
        "PAT-COST-REDUCTION-MIX-AND-SOURCING",
        "PAT-COST-REDUCTION-HEADCOUNT-PRODUCTIVITY",
    }

    assert (
        set(pattern_ids)
        == expected_ids
    )

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
        "Trigger Signals                : PASS"
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
        "EIOS COST REDUCTION PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()