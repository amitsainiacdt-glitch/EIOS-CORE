"""
EIOS
Everest Investment Operating System

External Source Selection Engine Test
"""

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.external_intelligence.source_selection_engine import (
    ExternalSourceSelectionEngine,
)


def main() -> None:

    engine = (
        ExternalSourceSelectionEngine()
    )

    results = [

        ExternalSearchResult(
            title="Result One",
            url="https://example.com/one",
            snippet="Useful result.",
            source="Provider",
        ),

        ExternalSearchResult(
            title="Duplicate Result",
            url="https://example.com/one",
            snippet="Duplicate URL.",
            source="Provider",
        ),

        ExternalSearchResult(
            title="Result Two",
            url="https://example.com/two",
            snippet="Another useful result.",
            source="Provider",
        ),

        ExternalSearchResult(
            title="Invalid URL",
            url="ftp://example.com/file",
            snippet="Invalid protocol.",
            source="Provider",
        ),

        ExternalSearchResult(
            title="",
            url="https://example.com/empty",
            snippet="",
            source="Provider",
        ),
    ]

    # ======================================================
    # SELECTION
    # ======================================================

    selected = engine.select(
        results,
        max_results=5,
    )

    assert len(selected) == 2

    print(
        "Source Selection               : PASS"
    )

    # ======================================================
    # ORDER PRESERVATION
    # ======================================================

    assert (
        selected[0].result.url
        == "https://example.com/one"
    )

    assert (
        selected[1].result.url
        == "https://example.com/two"
    )

    print(
        "Order Preservation             : PASS"
    )

    # ======================================================
    # DUPLICATE PROTECTION
    # ======================================================

    urls = [
        item.result.url
        for item in selected
    ]

    assert len(urls) == len(set(urls))

    print(
        "Duplicate URL Protection       : PASS"
    )

    # ======================================================
    # INVALID URL REJECTION
    # ======================================================

    assert all(
        item.result.url.startswith(
            (
                "http://",
                "https://",
            )
        )
        for item in selected
    )

    print(
        "Invalid URL Rejection          : PASS"
    )

    # ======================================================
    # EMPTY CONTENT REJECTION
    # ======================================================

    assert all(
        item.result.title.strip()
        or item.result.snippet.strip()
        for item in selected
    )

    print(
        "Empty Result Rejection         : PASS"
    )

    # ======================================================
    # MAXIMUM RESULTS
    # ======================================================

    more_results = [

        ExternalSearchResult(
            title=f"Result {index}",
            url=f"https://example.com/{index}",
            snippet="Valid.",
            source="Provider",
        )

        for index in range(10)
    ]

    limited = engine.select(
        more_results,
        max_results=3,
    )

    assert len(limited) == 3

    print(
        "Maximum Result Limit           : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    assert (
        results[0].url
        == "https://example.com/one"
    )

    assert (
        results[1].url
        == "https://example.com/one"
    )

    print(
        "Input Immutability              : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        selected[0],
        "confidence",
    )

    assert not hasattr(
        selected[0],
        "evidence_score",
    )

    assert not hasattr(
        selected[0],
        "opportunity_score",
    )

    print(
        "No Analytical Fabrication       : PASS"
    )

    # ======================================================
    # INVALID INPUT PROTECTION
    # ======================================================

    try:

        engine.select(
            None
        )

        raise AssertionError(
            "None results were accepted"
        )

    except ValueError:
        pass

    try:

        engine.select(
            [],
            max_results=0,
        )

        raise AssertionError(
            "Invalid max_results was accepted"
        )

    except ValueError:
        pass

    print(
        "Invalid Input Protection        : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL SOURCE SELECTION "
        "ENGINE : PASS"
    )


if __name__ == "__main__":
    main()