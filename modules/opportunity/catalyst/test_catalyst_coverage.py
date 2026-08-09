"""
EIOS
Everest Investment Operating System

Catalyst Coverage Analyzer Test
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage import (
    CatalystCoverageAnalyzer,
)


def main() -> None:

    # ======================================================
    # CANONICAL FAMILY COUNT
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.family_count()
        == 30
    )

    # ======================================================
    # COVERED FAMILY COUNT
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.covered_count()
        == 4
    )

    # ======================================================
    # UNCOVERED FAMILY COUNT
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.uncovered_count()
        == 26
    )

    # ======================================================
    # COVERAGE CONSISTENCY
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.covered_count()
        + CatalystCoverageAnalyzer.uncovered_count()
        == CatalystCoverageAnalyzer.family_count()
    )

    # ======================================================
    # COVERED FAMILY LOOKUP
    # ======================================================

    covered = {
        item.family: item.pattern_count
        for item
        in CatalystCoverageAnalyzer.covered_families()
    }

    assert (
        covered[
            CatalystFamily.CAPACITY_EXPANSION
        ]
        == 2
    )

    assert (
        covered[
            CatalystFamily.ORDER_CONTRACT
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.REGULATORY_CHANGE
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.REVENUE_GROWTH
        ]
        == 6
    )

    # ======================================================
    # REVENUE GROWTH COVERAGE
    # ======================================================

    assert (
        CatalystFamily.REVENUE_GROWTH
        in covered
    )

    # ======================================================
    # UNCOVERED FAMILY DETECTION
    # ======================================================

    uncovered = {
        item.family: item.pattern_count
        for item
        in CatalystCoverageAnalyzer.uncovered_families()
    }

    assert (
        CatalystFamily.REVENUE_GROWTH
        not in uncovered
    )

    assert (
        CatalystFamily.PRICING
        in uncovered
    )

    assert (
        uncovered[
            CatalystFamily.PRICING
        ]
        == 0
    )

    # ======================================================
    # COVERED FAMILY SET
    # ======================================================

    expected_covered = {
        CatalystFamily.CAPACITY_EXPANSION,
        CatalystFamily.ORDER_CONTRACT,
        CatalystFamily.REGULATORY_CHANGE,
        CatalystFamily.REVENUE_GROWTH,
    }

    assert (
        set(covered.keys())
        == expected_covered
    )

    # ======================================================
    # COVERED / UNCOVERED EXCLUSIVITY
    # ======================================================

    assert (
        set(covered.keys()).isdisjoint(
            set(uncovered.keys())
        )
    )

    # ======================================================
    # COMPLETE TAXONOMY COVERAGE
    # ======================================================

    assert (
        set(covered.keys())
        | set(uncovered.keys())
        == set(CatalystFamily)
    )

    # ======================================================
    # COVERAGE RECORD INTEGRITY
    # ======================================================

    records = (
        CatalystCoverageAnalyzer.analyze()
    )

    assert (
        len(records)
        == 30
    )

    for record in records:

        assert (
            record.family
            in CatalystFamily
        )

        assert (
            record.pattern_count
            >= 0
        )

        if record.covered:

            assert (
                record.pattern_count
                > 0
            )

        else:

            assert (
                record.pattern_count
                == 0
            )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Canonical Family Count       : PASS"
    )

    print(
        "Covered Family Count         : PASS"
    )

    print(
        "Uncovered Family Count       : PASS"
    )

    print(
        "Coverage Consistency         : PASS"
    )

    print(
        "Capacity Coverage            : PASS"
    )

    print(
        "Order Coverage               : PASS"
    )

    print(
        "Regulatory Coverage          : PASS"
    )

    print(
        "Revenue Growth Coverage      : PASS"
    )

    print(
        "Uncovered Family Detection   : PASS"
    )

    print(
        "Coverage Record Integrity    : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST COVERAGE : PASS"
    )


if __name__ == "__main__":
    main()