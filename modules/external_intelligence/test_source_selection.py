"""
EIOS
Everest Investment Operating System

External Source Selection Test
"""

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.external_intelligence.source_selection import (
    SelectedSource,
)


def main() -> None:

    result = ExternalSearchResult(
        title="Synthetic Search Result",
        url="https://example.com",
        snippet="Synthetic result.",
        source="Mock Provider",
    )

    selected = SelectedSource(
        result=result,
        selection_reason=(
            "Selected for direct source retrieval."
        ),
    )

    # ======================================================
    # TYPE
    # ======================================================

    assert isinstance(
        selected,
        SelectedSource,
    )

    print(
        "Selected Source Model          : PASS"
    )

    # ======================================================
    # RESULT PRESERVATION
    # ======================================================

    assert (
        selected.result
        is result
    )

    assert (
        selected.result.url
        == "https://example.com"
    )

    assert (
        selected.result.title
        == "Synthetic Search Result"
    )

    print(
        "Search Result Preservation     : PASS"
    )

    # ======================================================
    # REASON
    # ======================================================

    assert (
        "direct source retrieval"
        in selected.selection_reason
    )

    print(
        "Selection Reason Preservation  : PASS"
    )

    # ======================================================
    # IMMUTABILITY
    # ======================================================

    assert (
        selected.result.source
        == "Mock Provider"
    )

    print(
        "Source Provenance Preservation : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FIELDS
    # ======================================================

    assert not hasattr(
        selected,
        "confidence",
    )

    assert not hasattr(
        selected,
        "evidence_score",
    )

    assert not hasattr(
        selected,
        "opportunity_score",
    )

    print(
        "No Analytical Fabrication      : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL SOURCE SELECTION : PASS"
    )


if __name__ == "__main__":
    main()