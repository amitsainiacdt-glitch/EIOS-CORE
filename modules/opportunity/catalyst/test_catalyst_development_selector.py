"""
EIOS
Everest Investment Operating System

Catalyst Development Selector Test
"""


from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CoveragePriority,
)


from modules.opportunity.catalyst.catalyst_development_queue import (
    CatalystDevelopmentItem,
)


from modules.opportunity.catalyst.catalyst_development_selector import (
    CatalystDevelopmentSelector,
)


def main() -> None:

    # ======================================================
    # SELECT NEXT
    # ======================================================

    selected = (
        CatalystDevelopmentSelector.select_next()
    )

    assert selected is not None


    # ======================================================
    # RECORD TYPE
    # ======================================================

    assert isinstance(
        selected,
        CatalystDevelopmentItem,
    )


    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    assert (
        selected.family
        in CatalystFamily
    )


    # ======================================================
    # PRIORITY
    # ======================================================

    assert (
        selected.priority
        == CoveragePriority.CRITICAL
    )


    # ======================================================
    # REVENUE GROWTH MUST NOT BE SELECTED
    # ======================================================

    assert (
        selected.family
        != CatalystFamily.REVENUE_GROWTH
    )


    # ======================================================
    # SELECTED FAMILY MUST BE UNCOVERED
    # ======================================================

    assert (
        selected.family
        in {
            CatalystFamily.VOLUME_GROWTH,
            CatalystFamily.PRICING,
            CatalystFamily.MARGIN_EXPANSION,
            CatalystFamily.TECHNOLOGY_ADOPTION,
            CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        }
    )


    # ======================================================
    # DETERMINISTIC SELECTION
    # ======================================================

    selected_again = (
        CatalystDevelopmentSelector.select_next()
    )

    assert (
        selected_again
        == selected
    )


    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Next Item Selection           : PASS"
    )

    print(
        "Development Item Type         : PASS"
    )

    print(
        "Family Integrity              : PASS"
    )

    print(
        "Priority Selection            : PASS"
    )

    print(
        "Revenue Growth Exclusion      : PASS"
    )

    print(
        "Uncovered Family Selection    : PASS"
    )

    print(
        "Deterministic Selection       : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST DEVELOPMENT SELECTOR : PASS"
    )


if __name__ == "__main__":
    main()