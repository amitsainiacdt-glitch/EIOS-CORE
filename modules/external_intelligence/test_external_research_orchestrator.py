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
Observation
"""

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
)

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
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
                snippet="Synthetic research result.",
                source="Mock Provider",
            ),

            ExternalSearchResult(
                title="Example Research Result",
                url="https://example.com",
                snippet="Duplicate result.",
                source="Mock Provider",
            ),
        ]


def main() -> None:

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
    # ORCHESTRATOR
    # ======================================================

    orchestrator = (
        ExternalResearchOrchestrator(
            MockSearchProvider()
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
    # RETRIEVAL
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

    print(
        "HTTP Retrieval                   : PASS"
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
    # PROVENANCE
    # ======================================================

    assert (
        observation.description
        == retrieved.content
    )

    print(
        "Content Provenance               : PASS"
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
        "Input Immutability                : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        result,
        "evidence_score",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    assert not hasattr(
        observation,
        "evidence_score",
    )

    assert not hasattr(
        observation,
        "opportunity_score",
    )

    print(
        "Analytical Boundary               : PASS"
    )

    # ======================================================
    # INVALID INPUT
    # ======================================================

    try:

        orchestrator.execute(
            None
        )

        raise AssertionError(
            "None query was accepted"
        )

    except ValueError:
        pass

    print(
        "Invalid Input Protection          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL RESEARCH "
        "ORCHESTRATOR : PASS"
    )


if __name__ == "__main__":
    main()