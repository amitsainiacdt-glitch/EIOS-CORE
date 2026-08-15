"""
EIOS
Everest Investment Operating System

Market Share Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.market_share_patterns import (
    MARKET_SHARE_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(MARKET_SHARE_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.MARKET_SHARE
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in MARKET_SHARE_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.trigger_signals

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.leading_indicators

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.confirmation_indicators

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.earnings_channels

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.disconfirming_evidence

    # ======================================================
    # KILL SWITCHES
    # ======================================================

    for pattern in MARKET_SHARE_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_pattern_ids = {
        "PAT-MARKET-SHARE-ORGANIC-SHARE-GAIN",
        "PAT-MARKET-SHARE-COMPETITOR-SHARE-CAPTURE",
        "PAT-MARKET-SHARE-DISTRIBUTION-LED-GAIN",
        "PAT-MARKET-SHARE-PRODUCT-LED-GAIN",
        "PAT-MARKET-SHARE-CAPACITY-CONSTRAINED-GAIN",
        "PAT-MARKET-SHARE-SHARE-GAIN-COMPOUNDING",
    }

    actual_pattern_ids = {
        pattern.pattern_id
        for pattern in MARKET_SHARE_PATTERNS
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
        "EIOS MARKET SHARE PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()