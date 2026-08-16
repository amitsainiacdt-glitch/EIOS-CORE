"""
EIOS
Everest Investment Operating System

External Research Orchestrator
Partial Retrieval Failure Test
"""

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
)

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class FakeSearchProvider(SearchProvider):
    """
    Deterministic search provider returning three sources.
    """

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [
            ExternalSearchResult(
                title="Blocked Source",
                url="https://blocked.example.com",
                snippet="Blocked source.",
                source="Test Search",
            ),
            ExternalSearchResult(
                title="Successful Source One",
                url="https://success-one.example.com",
                snippet="Successful source one.",
                source="Test Search",
            ),
            ExternalSearchResult(
                title="Successful Source Two",
                url="https://success-two.example.com",
                snippet="Successful source two.",
                source="Test Search",
            ),
        ]


class FakeRetriever:
    """
    Deterministic retriever.

    One source fails.
    Two sources succeed.
    """

    def retrieve(
        self,
        url: str,
    ) -> RetrievedContent:

        if url == "https://blocked.example.com":

            raise RuntimeError(
                "HTTP 403 Forbidden"
            )

        return RetrievedContent(
            url=url,
            status_code=200,
            content=(
                "Synthetic successful content "
                "for EIOS testing."
            ),
            content_type="text/html",
            headers={
                "Content-Type": "text/html"
            },
        )


def main() -> None:

    # ======================================================
    # QUERY
    # ======================================================

    query = ExternalResearchQuery(
        company="Tata Motors",
        ticker="TATAMOTORS",
        question="Test retrieval resilience",
        query="Tata Motors retrieval resilience",
        intent="TEST",
    )

    # ======================================================
    # ORCHESTRATOR
    # ======================================================

    orchestrator = ExternalResearchOrchestrator(
        FakeSearchProvider(),
        retriever=FakeRetriever(),
    )

    # ======================================================
    # EXECUTION
    # ======================================================

    result = orchestrator.execute(
        query,
        max_sources=3,
    )

    # ======================================================
    # SOURCE SELECTION
    # ======================================================

    assert len(
        result.selected_sources
    ) == 3

    print(
        "Source Selection              : PASS"
    )

    # ======================================================
    # SUCCESSFUL RETRIEVALS
    # ======================================================

    assert len(
        result.retrieved_content
    ) == 2

    assert (
        result.retrieved_content[0].url
        == "https://success-one.example.com"
    )

    assert (
        result.retrieved_content[1].url
        == "https://success-two.example.com"
    )

    print(
        "Successful Retrievals         : PASS"
    )

    # ======================================================
    # OBSERVATIONS
    # ======================================================

    assert len(
        result.observations
    ) == 2

    print(
        "Successful Observations       : PASS"
    )

    # ======================================================
    # FAILURE PRESERVATION
    # ======================================================

    assert len(
        result.retrieval_failures
    ) == 1

    failure = (
        result.retrieval_failures[0]
    )

    assert (
        failure.url
        == "https://blocked.example.com"
    )

    assert (
        failure.error_type
        == "RuntimeError"
    )

    assert (
        "HTTP 403"
        in failure.error_message
    )

    print(
        "Retrieval Failure Preservation : PASS"
    )

    # ======================================================
    # FAILURE DOES NOT TERMINATE RUN
    # ======================================================

    assert (
        len(result.observations)
        == 2
    )

    assert (
        len(result.retrieved_content)
        == 2
    )

    print(
        "Failure Isolation             : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        result,
        "opportunity_score",
    )

    assert not hasattr(
        result,
        "valuation",
    )

    print(
        "Analytical Boundary            : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS PARTIAL RETRIEVAL FAILURE : PASS"
    )


if __name__ == "__main__":
    main()