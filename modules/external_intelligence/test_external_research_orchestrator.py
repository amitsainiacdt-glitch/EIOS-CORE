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
Observation
"""

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
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
    # RAW RETRIEVAL
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
        "evidence_score",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    assert not hasattr(
        source_assessment,
        "confidence",
    )

    assert not hasattr(
        source_assessment,
        "evidence_score",
    )

    assert not hasattr(
        source_assessment,
        "source_quality",
    )

    assert not hasattr(
        source_assessment,
        "credibility_score",
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
        "Analytical Boundary              : PASS"
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
        "Invalid Input Protection         : PASS"
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