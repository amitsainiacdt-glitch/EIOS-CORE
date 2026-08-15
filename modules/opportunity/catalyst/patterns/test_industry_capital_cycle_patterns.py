"""
EIOS
Everest Investment Operating System

Industry Capital Cycle Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.industry_capital_cycle_patterns import (
    INDUSTRY_CAPITAL_CYCLE_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(INDUSTRY_CAPITAL_CYCLE_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_pattern_ids = {
        "PAT-CAPITAL-CYCLE-CAPACITY-DISCIPLINE-INFLECTION",
        "PAT-CAPITAL-CYCLE-DEMAND-LED-CAPACITY-ABSORPTION",
        "PAT-CAPITAL-CYCLE-CAPEX-CYCLE-TURN",
        "PAT-CAPITAL-CYCLE-UNDERINVESTMENT-SUPPLY-TIGHTENING",
        "PAT-CAPITAL-CYCLE-PEAK-CAPACITY-UTILISATION",
        "PAT-CAPITAL-CYCLE-CAPITAL-RETURNS-INFLECTION",
    }

    actual_pattern_ids = {
        pattern.pattern_id
        for pattern in INDUSTRY_CAPITAL_CYCLE_PATTERNS
    }

    assert (
        actual_pattern_ids
        == expected_pattern_ids
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
        "EIOS INDUSTRY CAPITAL CYCLE PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()