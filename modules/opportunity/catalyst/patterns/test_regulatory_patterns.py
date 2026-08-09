"""
EIOS
Everest Investment Operating System

Regulatory Catalyst Pattern Tests
"""

from modules.opportunity.catalyst.patterns.regulatory_patterns import (
    REGULATORY_PATTERNS,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


def main() -> None:

    # ======================================================
    # COUNT
    # ======================================================

    assert len(REGULATORY_PATTERNS) == 6

    # ======================================================
    # FAMILY
    # ======================================================

    for pattern in REGULATORY_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.REGULATORY_CHANGE
        )

    # ======================================================
    # UNIQUE IDS
    # ======================================================

    ids = [
        pattern.pattern_id
        for pattern in REGULATORY_PATTERNS
    ]

    assert len(ids) == len(set(ids))

    # ======================================================
    # REQUIRED STRUCTURE
    # ======================================================

    for pattern in REGULATORY_PATTERNS:

        assert pattern.pattern_id
        assert pattern.name
        assert pattern.description

        assert pattern.trigger_signals
        assert pattern.mechanism

        assert pattern.transmission_channels

        assert pattern.leading_indicators
        assert pattern.confirmation_indicators

        assert pattern.typical_time_horizon

        assert pattern.earnings_channels

        assert pattern.market_mistake

        assert pattern.second_order_effects

        assert pattern.disconfirming_evidence

        assert pattern.kill_switch

    # ======================================================
    # SPECIFIC PATTERNS
    # ======================================================

    names = {
        pattern.name
        for pattern in REGULATORY_PATTERNS
    }

    expected_names = {
        "Product Approval",
        "Licence / Permit Approval",
        "Regulatory Relaxation",
        "Import Restriction",
        "Export Permission",
        "Compliance-Driven Demand",
    }

    assert names == expected_names

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Regulatory Pattern Count       : PASS"
    )

    print(
        "Regulatory Family Integrity     : PASS"
    )

    print(
        "Unique Pattern IDs              : PASS"
    )

    print(
        "Pattern Structure               : PASS"
    )

    print(
        "Pattern Names                   : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS REGULATORY CATALYST PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()