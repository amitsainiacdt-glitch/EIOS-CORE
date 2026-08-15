"""
EIOS
Everest Investment Operating System

Catalyst Development Selector Test

Final Catalyst Architecture State:

    30 Catalyst Families
    30 Covered Families
     0 Uncovered Families
     0 Development Queue Items

Therefore:

    CatalystDevelopmentSelector.select_next()
        -> None

The selector must not invent a development item when
there are no uncovered catalyst families.
"""


from modules.opportunity.catalyst.catalyst_development_queue_engine import (
    CatalystDevelopmentQueueEngine,
)

from modules.opportunity.catalyst.catalyst_development_selector import (
    CatalystDevelopmentSelector,
)


def main() -> None:

    # ======================================================
    # DEVELOPMENT QUEUE MUST BE EMPTY
    # ======================================================

    queue = (
        CatalystDevelopmentQueueEngine.build_queue()
    )

    assert isinstance(
        queue,
        list,
    )

    assert (
        queue
        == []
    )

    # ======================================================
    # SELECTOR MUST RETURN NO ITEM
    # ======================================================

    selected = (
        CatalystDevelopmentSelector.select_next()
    )

    assert (
        selected
        is None
    )

    # ======================================================
    # DETERMINISTIC EMPTY SELECTION
    # ======================================================

    selected_again = (
        CatalystDevelopmentSelector.select_next()
    )

    assert (
        selected_again
        is None
    )

    assert (
        selected_again
        == selected
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Development Queue Empty          : PASS"
    )

    print(
        "Development Queue Count          : PASS"
    )

    print(
        "No Next Development Item         : PASS"
    )

    print(
        "Selector Empty-State             : PASS"
    )

    print(
        "Deterministic Empty Selection    : PASS"
    )

    print()
    print(
        "---"
    )
    print()

    print(
        "EIOS CATALYST DEVELOPMENT SELECTOR : PASS"
    )


if __name__ == "__main__":
    main()