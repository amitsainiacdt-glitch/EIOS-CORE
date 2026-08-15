"""
EIOS
Everest Investment Operating System

Technology Adoption Catalyst Pattern Tests
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.technology_adoption_patterns import (
    TECHNOLOGY_ADOPTION_PATTERNS,
)


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(TECHNOLOGY_ADOPTION_PATTERNS)
        == 6
    )


    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in TECHNOLOGY_ADOPTION_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )


    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in TECHNOLOGY_ADOPTION_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.TECHNOLOGY_ADOPTION
        )


    # ======================================================
    # PATTERN STRUCTURE
    # ======================================================

    for pattern in TECHNOLOGY_ADOPTION_PATTERNS:

        assert pattern.pattern_id
        assert pattern.family
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
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in TECHNOLOGY_ADOPTION_PATTERNS
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )


    # ======================================================
    # EXPECTED PATTERN IDS
    # ======================================================

    expected_ids = {
        "PAT-TECH-ADOPTION-RAMP",
        "PAT-TECH-ADOPTION-PENETRATION",
        "PAT-TECH-ADOPTION-REPLACEMENT",
        "PAT-TECH-ADOPTION-STANDARDIZATION",
        "PAT-TECH-ADOPTION-ECOSYSTEM-RAMP",
        "PAT-TECH-ADOPTION-COST-PARITY",
    }


    assert (
        set(pattern_ids)
        == expected_ids
    )


    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Pattern Count                : PASS"
    )

    print(
        "Pattern Type Integrity       : PASS"
    )

    print(
        "Family Integrity             : PASS"
    )

    print(
        "Pattern Structure            : PASS"
    )

    print(
        "Unique Pattern IDs           : PASS"
    )

    print(
        "Expected Pattern IDs         : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS TECHNOLOGY ADOPTION PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()
    