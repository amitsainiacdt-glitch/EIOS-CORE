"""
EIOS
Everest Investment Operating System

Catalyst Pattern Registry Integrity Test
"""

from modules.opportunity.catalyst.catalyst_pattern_registry import (
    CatalystPatternRegistry,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


def main() -> None:

    patterns = (
        CatalystPatternRegistry.all()
    )

    # ======================================================
    # EVERY PATTERN MUST HAVE A VALID FAMILY
    # ======================================================

    for pattern in patterns:

        assert isinstance(
            pattern.family,
            CatalystFamily,
        )

    # ======================================================
    # EVERY PATTERN ID MUST BE UNIQUE
    # ======================================================

    pattern_ids = [
        pattern.pattern_id
        for pattern in patterns
    ]

    assert (
        len(pattern_ids)
        == len(set(pattern_ids))
    )

    # ======================================================
    # EVERY PATTERN MUST HAVE A NAME
    # ======================================================

    for pattern in patterns:

        assert pattern.pattern_id
        assert pattern.name

    # ======================================================
    # EVERY PATTERN MUST BE RETRIEVABLE
    # ======================================================

    for pattern in patterns:

        retrieved = (
            CatalystPatternRegistry.get(
                pattern.pattern_id
            )
        )

        assert retrieved is pattern

    # ======================================================
    # FAMILY DISTRIBUTION
    # ======================================================

    family_pattern_counts = {
        family: len(
            CatalystPatternRegistry.get_by_family(
                family
            )
        )
        for family in CatalystFamily
    }

    # ======================================================
    # TOTAL CONSISTENCY
    # ======================================================

    assert (
        sum(family_pattern_counts.values())
        == CatalystPatternRegistry.count()
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Valid Catalyst Families        : PASS"
    )

    print(
        "Unique Pattern IDs             : PASS"
    )

    print(
        "Pattern Names                  : PASS"
    )

    print(
        "Pattern Retrieval              : PASS"
    )

    print(
        "Family Distribution             : PASS"
    )

    print(
        "Registry Count Consistency      : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST PATTERN INTEGRITY : PASS"
    )


if __name__ == "__main__":
    main()