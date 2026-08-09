"""
EIOS
Everest Investment Operating System

Catalyst Coverage Analyzer Test
"""

from modules.opportunity.catalyst.catalyst_coverage import (
    CatalystCoverageAnalyzer,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
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
    # COVERED FAMILIES
    # ======================================================

    covered = (
        CatalystCoverageAnalyzer.covered_families()
    )

    assert (
        CatalystCoverageAnalyzer.covered_count()
        == 3
    )

    # ======================================================
    # UNCOVERED FAMILIES
    # ======================================================

    uncovered = (
        CatalystCoverageAnalyzer.uncovered_families()
    )

    assert (
        CatalystCoverageAnalyzer.uncovered_count()
        == 27
    )

    # ======================================================
    # TOTAL CONSISTENCY
    # ======================================================

    assert (
        len(covered)
        + len(uncovered)
        == 30
    )

    # ======================================================
    # CAPACITY COVERAGE
    # ======================================================

    capacity = [
        item
        for item in covered
        if item.family
        == CatalystFamily.CAPACITY_EXPANSION
    ]

    assert len(capacity) == 1

    assert (
        capacity[0].pattern_count
        == 2
    )

    # ======================================================
    # ORDER COVERAGE
    # ======================================================

    order = [
        item
        for item in covered
        if item.family
        == CatalystFamily.ORDER_CONTRACT
    ]

    assert len(order) == 1

    assert (
        order[0].pattern_count
        == 6
    )

    # ======================================================
    # REGULATORY COVERAGE
    # ======================================================

    regulatory = [
        item
        for item in covered
        if item.family
        == CatalystFamily.REGULATORY_CHANGE
    ]

    assert len(regulatory) == 1

    assert (
        regulatory[0].pattern_count
        == 6
    )

    # ======================================================
    # EXAMPLE UNCOVERED FAMILY
    # ======================================================

    revenue_growth = [
        item
        for item in uncovered
        if item.family
        == CatalystFamily.REVENUE_GROWTH
    ]

    assert len(revenue_growth) == 1

    assert (
        revenue_growth[0].pattern_count
        == 0
    )

    assert (
        revenue_growth[0].covered
        is False
    )

    # ======================================================
    # IMMUTABILITY
    # ======================================================

    first = covered[0]

    assert first.family in CatalystFamily

    assert isinstance(
        first.pattern_count,
        int,
    )

    assert isinstance(
        first.covered,
        bool,
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