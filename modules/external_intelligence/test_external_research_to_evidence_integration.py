"""
EIOS
Everest Investment Operating System

External Research → Evidence Integration Test

Architecture

Research Question
        ↓
External Research Query
        ↓
Search Engine
        ↓
Search Result
        ↓
HTTP Retrieval
        ↓
Observation
        ↓
Evidence Assessment
        ↓
EvidenceItem
        ↓
Opportunity Evidence Engine

This test verifies the complete external-research-to-evidence
boundary without requiring a real search-provider API key.
"""

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_assessment_engine import (
    EvidenceAssessmentEngine,
)

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
)

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
)

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

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.opportunity.evidence_engine import (
    OpportunityEvidenceEngine,
)


# ==========================================================
# MOCK SEARCH PROVIDER
# ==========================================================


class MockSearchProvider(SearchProvider):
    """
    Deterministic provider used only for integration testing.
    """

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [

            ExternalSearchResult(
                title=(
                    "Industrial demand "
                    "improvement evidence"
                ),

                url="https://example.com",

                snippet=(
                    "Synthetic evidence indicating "
                    "industrial demand improvement."
                ),

                source="Mock Search Provider",
            )
        ]


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    # ======================================================
    # RESEARCH QUERY
    # ======================================================

    query = ExternalResearchQuery(

        company="Test Company",

        ticker="TEST",

        question=(
            "Is industrial demand improving "
            "and supported by independent evidence?"
        ),

        query=(
            '"Test Company" "TEST" '
            '"industrial demand improving"'
        ),

        intent="DEMAND_VALIDATION",
    )

    print(
        "External Research Query        : PASS"
    )

    # ======================================================
    # SEARCH ENGINE
    # ======================================================

    provider = MockSearchProvider()

    search_engine = (
        ExternalResearchSearchEngine(
            provider
        )
    )

    search_results = (
        search_engine.search(
            query
        )
    )

    assert len(
        search_results
    ) == 1

    search_result = (
        search_results[0]
    )

    print(
        "External Search                : PASS"
    )

    # ======================================================
    # HTTP RETRIEVAL
    # ======================================================

    retriever = HTTPExternalRetriever()

    retrieved = retriever.retrieve(
        search_result.url
    )

    assert (
        retrieved.status_code
        == 200
    )

    assert retrieved.content

    print(
        "HTTP Retrieval                 : PASS"
    )

    # ======================================================
    # OBSERVATION
    # ======================================================

    observation_engine = (
        ObservationEngine()
    )

    observation_adapter = (
        ExternalObservationAdapter(
            observation_engine
        )
    )

    observation = (
        observation_adapter.ingest(

            title=search_result.title,

            description=retrieved.content,

            source=search_result.url,

            category="External Web",

            entity="Test Company",

            confidence=75.0,
        )
    )

    assert observation is not None

    assert (
        observation.source
        == search_result.url
    )

    assert (
        observation.title
        == search_result.title
    )

    print(
        "Observation Creation           : PASS"
    )

    # ======================================================
    # EVIDENCE ASSESSMENT
    # ======================================================

    assessment = EvidenceAssessment(

        category="Industry",

        direction="Supporting",

        strength=80.0,

        confidence=75.0,

        independent_confirmation=2,

        is_primary_source=False,

        is_time_sensitive=True,

        notes=(
            "Synthetic external research "
            "assessment."
        ),
    )

    assessment_engine = (
        EvidenceAssessmentEngine()
    )

    evidence_item = (
        assessment_engine.assess(

            observation=observation,

            assessment=assessment,

            evidence_id="EXT-INT-EVID-001",
        )
    )

    assert (
        evidence_item.evidence_id
        == "EXT-INT-EVID-001"
    )

    assert (
        evidence_item.statement
        == observation.description
    )

    assert (
        evidence_item.source
        == observation.source
    )

    print(
        "EvidenceItem Creation          : PASS"
    )

    # ======================================================
    # OPPORTUNITY EVIDENCE ENGINE
    # ======================================================

    opportunity_evidence_engine = (
        OpportunityEvidenceEngine()
    )

    # ------------------------------------------------------
    # Build enough supporting evidence to exercise the
    # existing institutional evidence engine.
    #
    # We intentionally create additional assessment-backed
    # items from independent synthetic observations.
    # ------------------------------------------------------

    additional_observations = [

        (
            "Industry capacity utilisation improvement",
            "Industry Data",
            "Sector",
            85.0,
            85.0,
            2,
            False,
        ),

        (
            "Company order visibility improvement",
            "Company Filing",
            "Company",
            90.0,
            90.0,
            2,
            True,
        ),
    ]

    additional_evidence = []

    for index, (
        title,
        source,
        category,
        strength,
        confidence,
        confirmation,
        primary,
    ) in enumerate(
        additional_observations,
        start=2,
    ):

        extra_observation = (
            observation_adapter.ingest(

                title=title,

                description=title,

                source=source,

                category=category,

                entity="Test Company",

                confidence=confidence,
            )
        )

        extra_assessment = EvidenceAssessment(

            category=category,

            direction="Supporting",

            strength=strength,

            confidence=confidence,

            independent_confirmation=confirmation,

            is_primary_source=primary,

            is_time_sensitive=True,

            notes=(
                "Synthetic independent "
                "supporting evidence."
            ),
        )

        extra_evidence = (
            assessment_engine.assess(

                observation=extra_observation,

                assessment=extra_assessment,

                evidence_id=(
                    f"EXT-INT-EVID-{index:03d}"
                ),
            )
        )

        additional_evidence.append(
            extra_evidence
        )

    supporting_evidence = [
        evidence_item,
        *additional_evidence,
    ]

    assert (
        len(supporting_evidence)
        == 3
    )

    print(
        "Supporting Evidence Assembly   : PASS"
    )

    # ======================================================
    # CONTRADICTORY EVIDENCE
    # ======================================================

    contradictory_observation = (
        observation_adapter.ingest(

            title=(
                "Industrial demand uncertainty"
            ),

            description=(
                "Some end markets remain uncertain."
            ),

            source="Industry Commentary",

            category="Risk",

            entity="Test Company",

            confidence=70.0,
        )
    )

    contradictory_assessment = (
        EvidenceAssessment(

            category="Risk",

            direction="Contradictory",

            strength=55.0,

            confidence=70.0,

            independent_confirmation=1,

            is_primary_source=False,

            is_time_sensitive=True,

            notes=(
                "Synthetic contradictory evidence."
            ),
        )
    )

    contradictory_item = (
        assessment_engine.assess(

            observation=(
                contradictory_observation
            ),

            assessment=(
                contradictory_assessment
            ),

            evidence_id=(
                "EXT-INT-CONTRA-001"
            ),
        )
    )

    print(
        "Contradictory Evidence          : PASS"
    )

    # ======================================================
    # RUN OPPORTUNITY EVIDENCE ENGINE
    # ======================================================

    evidence_pack = (
        opportunity_evidence_engine.analyze(

            company="Test Company",

            supporting_evidence=(
                supporting_evidence
            ),

            contradictory_evidence=[
                contradictory_item
            ],

            assumptions=[
                (
                    "Industrial demand recovery "
                    "continues."
                )
            ],

            kill_switches=[
                (
                    "Material demand reversal"
                )
            ],

            monitoring_signals=[
                "Order growth",
                "Capacity utilisation",
            ],
        )
    )

    assert (
        evidence_pack is not None
    )

    print(
        "Opportunity Evidence Engine    : PASS"
    )

    # ======================================================
    # HAND-OFF
    # ======================================================

    assert (
        len(
            evidence_pack.supporting_evidence
        )
        == 3
    )

    assert (
        len(
            evidence_pack.contradictory_evidence
        )
        == 1
    )

    print(
        "Evidence → Opportunity Handoff : PASS"
    )

    # ======================================================
    # SCORING
    # ======================================================

    assert (
        0.0
        <= evidence_pack.evidence_score
        <= 100.0
    )

    assert (
        0.0
        <= evidence_pack.confidence
        <= 100.0
    )

    print(
        "Downstream Evidence Scoring    : PASS"
    )

    # ======================================================
    # SOURCE PRESERVATION
    # ======================================================

    sources = {
        item.source
        for item
        in evidence_pack.supporting_evidence
    }

    assert (
        "Company Filing"
        in sources
    )

    assert (
        "Industry Data"
        in sources
    )

    assert (
        "https://example.com"
        in sources
    )

    print(
        "Source Preservation             : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        observation,
        "opportunity_score",
    )

    assert not hasattr(
        evidence_item,
        "opportunity_score",
    )

    assert not hasattr(
        evidence_item,
        "valuation",
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
        "EIOS EXTERNAL RESEARCH → "
        "OPPORTUNITY EVIDENCE : PASS"
    )


if __name__ == "__main__":
    main()