"""
EIOS
Everest Investment Operating System

External Research Orchestrator Test
====================================

Tests:

Research Query
    ↓
Search Provider
    ↓
Source Selection
    ↓
HTTP Retrieval
    ↓
Content Normalization
    ↓
Source Assessment
    ↓
Research Quality
    ↓
Observation
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

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.observation.observation_persistence import (
    ObservationPersistence,
)

from modules.observation.observation_registry import (
    ObservationRegistry,
)


# ==========================================================
# MOCK SEARCH PROVIDER
# ==========================================================


class MockSearchProvider(SearchProvider):
    """
    Deterministic search provider for testing.
    """

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [
            ExternalSearchResult(
                title="Example Research Result",
                url="https://example.com",
                snippet=(
                    "Synthetic research result "
                    "for orchestrator testing."
                ),
                source="Mock Provider",
            ),

            ExternalSearchResult(
                title="Example Research Result",
                url="https://example.com",
                snippet="Duplicate result.",
                source="Mock Provider",
            ),
        ]


# ==========================================================
# MOCK HTTP RETRIEVER
# ==========================================================


class MockHTTPRetriever:
    """
    Deterministic HTTP retrieval boundary.

    No live Internet access is required.
    """

    def __init__(self) -> None:

        self.received_urls: list[str] = []

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
                "Synthetic research content indicates "
                "that industrial demand is improving "
                "with stronger order activity during "
                "the current testing period. "
                "This deterministic content exists only "
                "to validate the EIOS research pipeline."
            ),
            content_type="text/html",
            headers={
                "Content-Type": "text/html"
            },
        )


# ==========================================================
# MAIN TEST
# ==========================================================


def main() -> None:

    print("=" * 60)
    print(
        "EIOS EXTERNAL RESEARCH ORCHESTRATOR TEST"
    )
    print("=" * 60)

    # ======================================================
    # QUERY
    # ======================================================

    query = ExternalResearchQuery(
        company="Test Company",
        ticker="TEST",
        question=(
            "Is industrial demand improving?"
        ),
        query=(
            '"Test Company" "TEST" '
            '"industrial demand improving"'
        ),
        intent="DEMAND_VALIDATION",
    )

    # ======================================================
    # MOCK COMPONENTS
    # ======================================================

    retriever = MockHTTPRetriever()

    # ------------------------------------------------------
    # ISOLATED OBSERVATION STATE
    # ------------------------------------------------------
    #
    # The normal ObservationEngine loads historical
    # observations from data/observations.json.
    #
    # This test must not depend on developer-machine state.
    #
    # Therefore the test uses its own isolated persistence
    # file and an empty registry.
    # ------------------------------------------------------

    test_persistence = ObservationPersistence(
        path=(
            "data/"
            "test_external_research_orchestrator_observations.json"
        )
    )

    test_persistence.clear()

    observation_engine = ObservationEngine(
        registry=ObservationRegistry(),
        persistence=test_persistence,
    )

    # ======================================================
    # ORCHESTRATOR
    # ======================================================

    orchestrator = (
        ExternalResearchOrchestrator(
            MockSearchProvider(),
            retriever=retriever,
            observation_engine=observation_engine,
        )
    )

    assert orchestrator is not None

    print(
        "External Research Orchestrator : PASS"
    )

    # ======================================================
    # EXECUTE
    # ======================================================

    result = orchestrator.execute(
        query,
        max_sources=5,
        observation_category="External Web",
        observation_confidence=70.0,
    )

    assert result is not None

    print(
        "Orchestration Execution         : PASS"
    )

    # ======================================================
    # QUERY PRESERVATION
    # ======================================================

    assert (
        result.query
        == query
    )

    print(
        "Query Preservation               : PASS"
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

    assert (
        result.selected_sources[0]
        .result.url
        == "https://example.com"
    )

    print(
        "Source Selection                 : PASS"
    )

    # ======================================================
    # HTTP RETRIEVAL
    # ======================================================

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
        retriever.received_urls
        == [
            "https://example.com"
        ]
    )

    print(
        "HTTP Retrieval                   : PASS"
    )

    # ======================================================
    # NORMALIZED CONTENT
    # ======================================================

    assert (
        len(
            result.normalized_content
        )
        == 1
    )

    normalized = (
        result.normalized_content[0]
    )

    assert (
        normalized.url
        == retrieved.url
    )

    assert (
        normalized.status_code
        == retrieved.status_code
    )

    assert (
        normalized.content_type
        == retrieved.content_type
    )

    assert normalized.normalized_text

    print(
        "Normalized Content Creation     : PASS"
    )

    # ======================================================
    # RAW CONTENT PRESERVATION
    # ======================================================

    assert (
        normalized.original_content
        == retrieved.content
    )

    print(
        "Raw Content Preservation        : PASS"
    )

    # ======================================================
    # SOURCE ASSESSMENT
    # ======================================================

    assert (
        len(
            result.source_assessments
        )
        == 1
    )

    source_assessment = (
        result.source_assessments[0]
    )

    assert (
        source_assessment.source_url
        == retrieved.url
    )

    assert (
        source_assessment.domain
        == "example.com"
    )

    assert (
        source_assessment.publisher
        == "Mock Provider"
    )

    assert (
        source_assessment.provenance_complete
        is True
    )

    print(
        "Source Assessment Creation     : PASS"
    )

    # ======================================================
    # SOURCE ASSESSMENT PROVENANCE
    # ======================================================

    assert (
        source_assessment.source_url
        == result.selected_sources[0]
        .result.url
    )

    assert (
        source_assessment.source_url
        == normalized.url
    )

    assert (
        source_assessment.source_url
        == retrieved.url
    )

    print(
        "Source Assessment Provenance    : PASS"
    )

    # ======================================================
    # RESEARCH QUALITY
    # ======================================================

    assert (
        len(
            result.observations
        )
        == 1
    )

    print(
        "Research Quality Gate           : PASS"
    )

    # ======================================================
    # OBSERVATION
    # ======================================================

    observation = (
        result.observations[0]
    )

    assert (
        observation.source
        == "https://example.com"
    )

    assert (
        observation.entity
        == "Test Company"
    )

    assert (
        observation.confidence
        == 70.0
    )

    print(
        "Observation Creation             : PASS"
    )

    # ======================================================
    # NORMALIZED CONTENT → OBSERVATION
    # ======================================================

    assert (
        observation.description
        == normalized.normalized_text
    )

    print(
        "Observation Uses Normalized Text: PASS"
    )

    # ======================================================
    # NORMALIZED CONTENT PROVENANCE
    # ======================================================

    assert (
        normalized.original_content
        == retrieved.content
    )

    assert (
        normalized.url
        == observation.source
    )

    print(
        "Normalized Content Provenance    : PASS"
    )

    # ======================================================
    # REGISTRY
    # ======================================================

    assert (
        orchestrator.observation_engine
        .registry.count()
        == 1
    )

    print(
        "Observation Registry             : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
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
        "Input Immutability               : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        result,
        "evidence",
    )

    assert not hasattr(
        result,
        "signals",
    )

    assert not hasattr(
        result,
        "valuation",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    print(
        "Analytical Boundary              : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "EIOS EXTERNAL RESEARCH ORCHESTRATOR "
        ": ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()