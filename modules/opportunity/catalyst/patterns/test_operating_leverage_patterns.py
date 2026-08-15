"""
EIOS
Everest Investment Operating System

Operating Leverage Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.operating_leverage_patterns import (
    OPERATING_LEVERAGE_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(OPERATING_LEVERAGE_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.OPERATING_LEVERAGE
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in OPERATING_LEVERAGE_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in OPERATING_LEVERAGE_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-OPERATING-LEVERAGE-FIXED-COST-ABSORPTION",
        "PAT-OPERATING-LEVERAGE-INCREMENTAL-MARGIN-INFLECTION",
        "PAT-OPERATING-LEVERAGE-UTILISATION-TO-LEVERAGE",
        "PAT-OPERATING-LEVERAGE-REVENUE-THRESHOLD-CROSSING",
        "PAT-OPERATING-LEVERAGE-VOLUME-TO-EARNINGS-AMPLIFICATION",
        "PAT-OPERATING-LEVERAGE-EPS-INFLECTION",
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
        "EIOS OPERATING LEVERAGE PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()