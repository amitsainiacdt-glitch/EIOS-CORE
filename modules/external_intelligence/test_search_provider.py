"""
EIOS
Everest Investment Operating System

External Search Provider Contract Test
"""

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class TestSearchProvider(SearchProvider):
    """
    Deterministic test implementation of the provider contract.
    """

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [
            ExternalSearchResult(
                title="Test Result",
                url="https://example.com",
                snippet=(
                    f"Result for: {query.query}"
                ),
                source="Test Provider",
            )
        ]


def main() -> None:

    # ======================================================
    # QUERY
    # ======================================================

    query = ExternalResearchQuery(
        company="Test Company",
        ticker="TEST",
        question=(
            "Is industrial demand accelerating?"
        ),
        query=(
            '"Test Company" "TEST" '
            '"industrial demand accelerating"'
        ),
        intent="DEMAND_VALIDATION",
    )

    # ======================================================
    # PROVIDER
    # ======================================================

    provider = TestSearchProvider()

    assert isinstance(
        provider,
        SearchProvider,
    )

    print(
        "Search Provider Contract      : PASS"
    )

    # ======================================================
    # SEARCH
    # ======================================================

    results = provider.search(
        query
    )

    assert isinstance(
        results,
        list,
    )

    assert len(
        results
    ) == 1

    print(
        "Search Execution Contract     : PASS"
    )

    # ======================================================
    # RESULT TYPE
    # ======================================================

    result = results[0]

    assert isinstance(
        result,
        ExternalSearchResult,
    )

    print(
        "Search Result Type             : PASS"
    )

    # ======================================================
    # RESULT CONTENT
    # ======================================================

    assert (
        result.title
        == "Test Result"
    )

    assert (
        result.url
        == "https://example.com"
    )

    assert (
        result.source
        == "Test Provider"
    )

    assert (
        "industrial demand"
        in result.snippet
    )

    print(
        "Search Result Preservation     : PASS"
    )

    # ======================================================
    # QUERY IMMUTABILITY
    # ======================================================

    assert (
        query.company
        == "Test Company"
    )

    assert (
        query.ticker
        == "TEST"
    )

    assert (
        query.intent
        == "DEMAND_VALIDATION"
    )

    print(
        "Query Immutability             : PASS"
    )

    # ======================================================
    # PROVIDER-NEUTRALITY
    # ======================================================

    assert not hasattr(
        result,
        "confidence",
    )

    assert not hasattr(
        result,
        "evidence_score",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    print(
        "Provider Neutrality            : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS SEARCH PROVIDER CONTRACT : PASS"
    )


if __name__ == "__main__":
    main()