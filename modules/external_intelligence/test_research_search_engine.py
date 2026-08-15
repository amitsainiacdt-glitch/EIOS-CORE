"""
EIOS
Everest Investment Operating System

External Research Search Engine Test
"""

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.research_search_engine import (
    ExternalResearchSearchEngine,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class MockSearchProvider(SearchProvider):

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [
            ExternalSearchResult(
                title="Synthetic Result",
                url="https://example.com",
                snippet=query.query,
                source="Mock Provider",
            )
        ]


def main() -> None:

    query = ExternalResearchQuery(
        company="Test Company",
        ticker="TEST",
        question="Is demand improving?",
        query=(
            '"Test Company" "TEST" '
            '"demand improving"'
        ),
        intent="DEMAND_VALIDATION",
    )

    provider = MockSearchProvider()

    engine = ExternalResearchSearchEngine(
        provider
    )

    # ======================================================
    # ENGINE
    # ======================================================

    assert engine is not None

    print(
        "Research Search Engine        : PASS"
    )

    # ======================================================
    # SEARCH
    # ======================================================

    results = engine.search(
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
        "Provider Delegation            : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    assert isinstance(
        results[0],
        ExternalSearchResult,
    )

    assert (
        results[0].source
        == "Mock Provider"
    )

    print(
        "Result Preservation             : PASS"
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
        "Query Immutability              : PASS"
    )

    # ======================================================
    # NONE PROTECTION
    # ======================================================

    try:

        engine.search(
            None
        )

        raise AssertionError(
            "None query was accepted"
        )

    except ValueError:
        pass

    print(
        "None Query Protection           : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        results[0],
        "confidence",
    )

    assert not hasattr(
        results[0],
        "evidence_score",
    )

    assert not hasattr(
        results[0],
        "opportunity_score",
    )

    print(
        "No Analytical Fabrication       : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL RESEARCH SEARCH ENGINE : PASS"
    )


if __name__ == "__main__":
    main()