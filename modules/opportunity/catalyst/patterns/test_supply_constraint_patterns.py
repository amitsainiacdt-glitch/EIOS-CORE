"""
EIOS
Everest Investment Operating System

Supply Constraint Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.supply_constraint_patterns import (
    SUPPLY_CONSTRAINT_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(SUPPLY_CONSTRAINT_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.SUPPLY_CONSTRAINT
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in SUPPLY_CONSTRAINT_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.name

    # ======================================================
    # DESCRIPTIONS
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.description

    # ======================================================
    # MECHANISMS
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.mechanism

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.trigger_signals
        assert len(pattern.trigger_signals) > 0

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.leading_indicators
        assert len(pattern.leading_indicators) > 0

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.confirmation_indicators
        assert len(pattern.confirmation_indicators) > 0

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.earnings_channels
        assert len(pattern.earnings_channels) > 0

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.market_mistake

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.disconfirming_evidence
        assert len(pattern.disconfirming_evidence) > 0

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in SUPPLY_CONSTRAINT_PATTERNS:

        assert pattern.kill_switch

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-SUPPLY-CONSTRAINT-CAPACITY-SHORTAGE",
        "PAT-SUPPLY-CONSTRAINT-LEAD-TIME-EXTENSION",
        "PAT-SUPPLY-CONSTRAINT-INVENTORY-DEPLETION",
        "PAT-SUPPLY-CONSTRAINT-SUPPLIER-CONSOLIDATION",
        "PAT-SUPPLY-CONSTRAINT-RAW-MATERIAL-SCARCITY",
        "PAT-SUPPLY-CONSTRAINT-PRICING-POWER-INFLECTION",
    }

    actual_ids = set(
        pattern_ids
    )

    assert (
        actual_ids
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
        "Trigger Signals               : PASS"
    )

    print(
        "Leading Indicators            : PASS"
    )

    print(
        "Confirmation Indicators       : PASS"
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
        "EIOS SUPPLY CONSTRAINT PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()