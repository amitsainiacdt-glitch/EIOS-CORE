"""
EIOS
Everest Investment Operating System

Opportunity → External Research Integration Test
=================================================

Validates:

OpportunityResearchIntake
        ↓
OpportunityExternalQueryEngine
        ↓
ExternalResearchQuery
        ↓
ExternalResearchOrchestrator
        ↓
Search
        ↓
Source Selection
        ↓
HTTP Retrieval
        ↓
Observation

The test uses deterministic mock SearchProvider
and HTTP retriever implementations.

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
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence

from modules.external_intelligence.opportunity_external_query_engine import (
    OpportunityExternalQueryEngine,
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

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)


# ==========================================================
# MOCK SEARCH PROVIDER
# ==========================================================


class MockSearchProvider(SearchProvider):
    """
    Deterministic search provider.

    No external API is contacted.
    """

    def __init__(self) -> None:

        self.received_queries = []

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        self.received_queries.append(
            query
        )

        return [
            ExternalSearchResult(
                title="Synthetic Research Source",
                url="https://example.com/eios-test",
                snippet=(
                    "Synthetic research content "
                    "for EIOS integration testing."
                ),
                source="Mock Provider",
            )
        ]


# ==========================================================
# MOCK HTTP RETRIEVER
# ==========================================================


class MockHTTPRetriever:
    """
    Deterministic HTTP retrieval boundary.

    Mimics HTTPExternalRetriever without
    contacting the Internet.
    """

    def __init__(self) -> None:

        self.received_urls = []

    def retrieve(
        self,
        url: str,
    ) -> RetrievedContent:

        self.received_urls.append(
            url
        )

        return RetrievedContent(
            url=url,
            status_code=200,
            content=(
                "Synthetic retrieved webpage content "
                "for EIOS integration testing."
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
    # OPPORTUNITY INTAKE
    # ======================================================

    intake = OpportunityResearchIntake(
        company="Tata Motors",
        ticker="TATAMOTORS",
        sector="Automobile",
        industry="Automotive",
        catalysts=[
            "EV adoption"
        ],
        concerns=[
            "Demand slowdown"
        ],
        risks=[
            "Margin pressure"
        ],
        strengths=[
            "Market leadership"
        ],
    )

    print(
        "Opportunity Intake              : PASS"
    )

    # ======================================================
    # QUERY ENGINE
    # ======================================================

    query_engine = (
        OpportunityExternalQueryEngine()
    )

    queries = query_engine.build(
        intake
    )

    assert queries

    print(
        "Opportunity → External Queries  : PASS"
    )

    # ======================================================
    # MOCK COMPONENTS
    # ======================================================

    provider = MockSearchProvider()

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

    assert orchestrator is not None

    print(
        "External Orchestrator           : PASS"
    )

    # ======================================================
    # EXECUTION
    # ======================================================

    external_query = queries[0]

    result = orchestrator.execute(
        external_query,
        max_sources=1,
        observation_category="External Web",
        observation_confidence=70.0,
    )

    # ======================================================
    # SEARCH DELEGATION
    # ======================================================

    assert (
        len(
            provider.received_queries
        )
        == 1
    )

    assert (
        provider.received_queries[0]
        == external_query
    )

    print(
        "Query → Search Provider         : PASS"
    )

    # ======================================================
    # QUERY IDENTITY
    # ======================================================

    assert (
        result.query.company
        == "Tata Motors"
    )

    assert (
        result.query.ticker
        == "TATAMOTORS"
    )

    assert (
        result.query.question
        == external_query.question
    )

    assert (
        result.query.intent
        == "OPPORTUNITY_RESEARCH"
    )

    print(
        "Query Identity Preservation     : PASS"
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
        selected.result.url
        == "https://example.com/eios-test"
    )

    print(
        "Source Selection                : PASS"
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
        == "https://example.com/eios-test"
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
    # REGISTRY
    # ======================================================

    assert (
        orchestrator.observation_engine
        .registry.count()
        == 1
    )

    assert (
        orchestrator.observation_engine
        .registry.latest()
        is observation
    )

    print(
        "Observation Registry            : PASS"
    )

    # ======================================================
    # END-TO-END PROVENANCE
    # ======================================================

    assert (
        selected.result.source
        == "Mock Provider"
    )

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
    # INPUT IMMUTABILITY
    # ======================================================

    assert (
        intake.company
        == "Tata Motors"
    )

    assert (
        intake.ticker
        == "TATAMOTORS"
    )

    assert (
        intake.catalysts
        == ["EV adoption"]
    )

    assert (
        intake.concerns
        == ["Demand slowdown"]
    )

    print(
        "Intake Immutability             : PASS"
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

    assert not hasattr(
        observation,
        "signal_score",
    )

    print(
        "Analytical Boundary             : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS OPPORTUNITY → EXTERNAL "
        "RESEARCH INTEGRATION : PASS"
    )


if __name__ == "__main__":
    main()
