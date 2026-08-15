"""
EIOS
Everest Investment Operating System

Source Selection → HTTP Integration Test
"""

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.external_intelligence.source_selection_engine import (
    ExternalSourceSelectionEngine,
)


def main() -> None:

    # ======================================================
    # SEARCH RESULTS
    # ======================================================

    results = [

        ExternalSearchResult(
            title="Example Result",
            url="https://example.com",
            snippet="Synthetic valid result.",
            source="Mock Provider",
        ),

        ExternalSearchResult(
            title="Duplicate",
            url="https://example.com",
            snippet="Duplicate URL.",
            source="Mock Provider",
        ),
    ]

    selector = (
        ExternalSourceSelectionEngine()
    )

    selected = selector.select(
        results,
        max_results=5,
    )

    assert len(selected) == 1

    print(
        "Source Selection              : PASS"
    )

    # ======================================================
    # HTTP RETRIEVAL
    # ======================================================

    retriever = HTTPExternalRetriever()

    source = selected[0]

    retrieved = retriever.retrieve(
        source.result.url
    )

    assert (
        retrieved.status_code
        == 200
    )

    assert retrieved.content

    print(
        "Selected Source → HTTP       : PASS"
    )

    # ======================================================
    # SOURCE PRESERVATION
    # ======================================================

    assert (
        retrieved.url
        == source.result.url
    )

    assert (
        source.result.source
        == "Mock Provider"
    )

    print(
        "Source Provenance             : PASS"
    )

    # ======================================================
    # RESULT CONTENT
    # ======================================================

    assert isinstance(
        retrieved.content,
        str,
    )

    assert len(
        retrieved.content
    ) > 0

    print(
        "Retrieved Content             : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        retrieved,
        "confidence",
    )

    assert not hasattr(
        retrieved,
        "evidence_score",
    )

    assert not hasattr(
        retrieved,
        "opportunity_score",
    )

    print(
        "Analytical Boundary           : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS SOURCE SELECTION → "
        "HTTP : PASS"
    )


if __name__ == "__main__":
    main()