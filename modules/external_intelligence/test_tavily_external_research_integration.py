"""
EIOS
Everest Investment Operating System

Tavily → External Research Integration Test
============================================

Validates the existing external research pipeline with
a deterministic Tavily-compatible mock provider.

No live Internet access is required.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

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
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence


# ==========================================================
# MOCK TAVILY PROVIDER
# ==========================================================


class MockTavilySearchProvider(SearchProvider):
    """
    Deterministic Tavily-compatible provider.

    This deliberately does not contact Tavily.
    """

    def __init__(self) -> None:
        self.received_queries = []

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        self.received_queries.append(query)

        return [
            ExternalSearchResult(
                title="Tavily Test Result",
                url="https://example.com/tavily-eios-test",
                snippet=(
                    "Synthetic Tavily search result "
                    "for EIOS integration testing."
                ),
                source="Tavily Search",
            )
        ]


# ==========================================================
# MOCK HTTP RETRIEVER
# ==========================================================


class MockHTTPRetriever:
    """
    Deterministic HTTP retrieval boundary.
    """

    def __init__(self) -> None:
        self.received_urls = []

    def retrieve(
        self,
        url: str,
    ) -> RetrievedContent:

        self.received_urls.append(url)

        return RetrievedContent(
            url=url,
            status_code=200,
            content=(
                "Synthetic webpage content retrieved "
                "from the selected Tavily source."
            ),
            content_type="text/html",
            headers={
                "Content-Type": "text/html"
            },
        )


# ==========================================================
# TEST
# ==========================================================


def main() -> None:

    # ======================================================
    # QUERY
    # ======================================================

    query = ExternalResearchQuery(
        company="Tata Motors",
        ticker="TATAMOTORS",
        question=(
            "What are the latest developments "
            "affecting demand?"
        ),
        query=(
            "Tata Motors TATAMOTORS "
            "latest demand developments"
        ),
        intent="OPPORTUNITY_RESEARCH",
    )

    # ======================================================
    # PROVIDER + RETRIEVER
    # ======================================================

    provider = MockTavilySearchProvider()

    retriever = MockHTTPRetriever()

    temp_dir = TemporaryDirectory()
    observation_engine = ObservationEngine(
        persistence=ObservationPersistence(
            Path(temp_dir.name) / "observations.json"
        )
    )

    orchestrator = (
        ExternalResearchOrchestrator(
            provider,
            retriever=retriever,
            observation_engine=observation_engine,
        )
    )

    print(
        "Tavily Provider Boundary        : PASS"
    )

    # ======================================================
    # EXECUTE
    # ======================================================

    result = orchestrator.execute(
        query,
        max_sources=1,
        observation_category="External Web",
        observation_confidence=70.0,
    )

    # ======================================================
    # QUERY PRESERVATION
    # ======================================================

    assert (
        len(
            provider.received_queries
        )
        == 1
    )

    assert (
        provider.received_queries[0]
        is query
    )

    assert (
        result.query
        is query
    )

    print(
        "Query Preservation              : PASS"
    )

    # ======================================================
    # SOURCE SELECTION
    # ======================================================

    assert (
        len(
            result.selected_sources
        )
        == 1
    )

    selected = (
        result.selected_sources[0]
    )

    assert (
        selected.result.source
        == "Tavily Search"
    )

    assert (
        selected.result.url
        == "https://example.com/tavily-eios-test"
    )

    print(
        "Tavily Source Selection        : PASS"
    )

    # ======================================================
    # HTTP RETRIEVAL
    # ======================================================

    assert (
        len(
            retriever.received_urls
        )
        == 1
    )

    assert (
        retriever.received_urls[0]
        == selected.result.url
    )

    assert (
        len(
            result.retrieved_content
        )
        == 1
    )

    retrieved = (
        result.retrieved_content[0]
    )

    assert (
        retrieved.status_code
        == 200
    )

    assert retrieved.content

    assert (
        retrieved.url
        == selected.result.url
    )

    print(
        "HTTP Retrieval                 : PASS"
    )

    # ======================================================
    # OBSERVATION
    # ======================================================

    assert (
        len(
            result.observations
        )
        == 1
    )

    observation = (
        result.observations[0]
    )

    assert (
        observation.entity
        == "Tata Motors"
    )

    assert (
        observation.source
        == retrieved.url
    )

    assert (
        observation.description
        == retrieved.content
    )

    assert (
        observation.confidence
        == 70.0
    )

    print(
        "Observation Creation            : PASS"
    )

    # ======================================================
    # PROVENANCE
    # ======================================================

    assert (
        selected.result.url
        == retrieved.url
    )

    assert (
        retrieved.url
        == observation.source
    )

    assert (
        retrieved.content
        == observation.description
    )

    print(
        "End-to-End Provenance           : PASS"
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

    assert not hasattr(
        observation,
        "opportunity_score",
    )

    assert not hasattr(
        observation,
        "valuation",
    )

    print(
        "Analytical Boundary             : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS TAVILY → EXTERNAL "
        "RESEARCH INTEGRATION : PASS"
    )


if __name__ == "__main__":
    main()
