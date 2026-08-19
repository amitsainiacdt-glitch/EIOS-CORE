"""
EIOS
Everest Investment Operating System

Full External → Opportunity Evidence Pipeline Test
====================================================

Validates the complete deterministic integration:

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
Content Normalization
        ↓
Source Assessment
        ↓
Observation
        ↓
Explicit Evidence Assessment
        ↓
EvidenceAssessmentEngine
        ↓
EvidenceItem
        ↓
OpportunityEvidenceEngine
        ↓
Opportunity Evidence Pack

No live Internet access is required.

This test validates integration only.
It does not perform investment analysis.
"""

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_assessment_engine import (
    EvidenceAssessmentEngine,
)

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
)

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
)

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

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.opportunity.discovery_opportunity_adapter import (
    DiscoveryOpportunityAdapter,
)

from modules.opportunity.evidence_engine import (
    OpportunityEvidenceEngine,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.observation.observation_registry import (
    ObservationRegistry,
)


# ==========================================================
# MOCK SEARCH PROVIDER
# ==========================================================


class MockSearchProvider(SearchProvider):
    """
    Deterministic external search provider.

    No live Internet access.
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
                title="Synthetic Tata Motors Research",
                url=(
                    "https://example.com/"
                    "tata-motors-demand"
                ),
                snippet=(
                    "Synthetic research source "
                    "for EIOS full-pipeline testing."
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

    No live Internet access.
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
                "Synthetic normalized research content "
                "indicating improving automotive demand "
                "for EIOS integration testing."
            ),
            content_type="text/html",
            headers={
                "Content-Type": "text/html"
            },
        )


# ==========================================================
# ISOLATED OBSERVATION PERSISTENCE
# ==========================================================


class InMemoryObservationPersistence:
    """
    Deterministic persistence boundary used by this integration test.

    The production ObservationEngine deliberately loads historical
    observations and rejects duplicates. The full integration test
    must use isolated state so previous test runs cannot suppress
    the synthetic observation required by this test.

    No production persistence behavior is changed.
    """

    def __init__(self) -> None:
        self._observations = []

    def load(self):
        return list(self._observations)

    def save(self, observations) -> None:
        self._observations = list(observations)


# ==========================================================
# TEST
# ==========================================================


def main() -> None:

    # ======================================================
    # OPPORTUNITY INTAKE
    # ======================================================

    candidate = DiscoveryCandidate(
        company_name="Tata Motors",
        ticker="TATAMOTORS",
        sector="Automobile",
        industry="Automotive",

        quality_score=90.0,
        growth_score=85.0,
        financial_score=88.0,
        management_score=82.0,
        capital_allocation_score=80.0,
        moat_score=86.0,
        risk_score=75.0,
        tailwind_score=90.0,
        valuation_score=70.0,

        overall_score=84.0,

        status="Passed",

        strengths=[
            "Market leadership",
        ],

        concerns=[
            "Demand slowdown",
        ],

        catalysts=[
            "EV adoption",
        ],

        risks=[
            "Margin pressure",
        ],

        discovery_notes=[
            "Candidate identified during Discovery screening.",
        ],

        confidence=82.0,

        source="EIOS Discovery Office",
    )

    adapter = DiscoveryOpportunityAdapter()

    intake = adapter.create_intake(
        candidate
    )

    assert intake.company == "Tata Motors"
    assert intake.ticker == "TATAMOTORS"

    assert intake.discovery_score == 84.0
    assert intake.discovery_confidence == 82.0

    assert intake.research_status == "NOT_STARTED"

    assert candidate.company_name == "Tata Motors"
    assert candidate.ticker == "TATAMOTORS"
    assert candidate.overall_score == 84.0
    assert candidate.confidence == 82.0

    print(
        "Discovery → Opportunity Intake   : PASS"
    )

    # ======================================================
    # OPPORTUNITY → EXTERNAL QUERY
    # ======================================================

    query_engine = (
        OpportunityExternalQueryEngine()
    )

    queries = (
        query_engine.build(
            intake
        )
    )

    assert queries

    external_query = queries[0]

    assert (
        external_query.company
        == "Tata Motors"
    )

    assert (
        external_query.ticker
        == "TATAMOTORS"
    )

    assert (
        external_query.intent
        == "OPPORTUNITY_RESEARCH"
    )

    print(
        "Opportunity → External Query       : PASS"
    )

    # ======================================================
    # MOCK COMPONENTS
    # ======================================================

    provider = MockSearchProvider()

    retriever = MockHTTPRetriever()

    # ======================================================
    # ISOLATED OBSERVATION STATE
    # ======================================================
    #
    # ObservationEngine intentionally loads historical
    # observations and rejects exact duplicates.
    #
    # This integration test must therefore use a fresh,
    # deterministic observation boundary. We do NOT weaken
    # production duplicate detection.
    #

    observation_registry = ObservationRegistry()

    observation_persistence = (
        InMemoryObservationPersistence()
    )

    observation_engine = ObservationEngine(
        registry=observation_registry,
        persistence=observation_persistence,
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
        "External Orchestrator               : PASS"
    )

    # ======================================================
    # EXTERNAL RESEARCH
    # ======================================================

    result = (
        orchestrator.execute(
            external_query,
            max_sources=1,
            observation_category="External Web",
            observation_confidence=70.0,
        )
    )

    assert result is not None

    print(
        "External Research Execution         : PASS"
    )

    # ======================================================
    # SEARCH
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
        "Search Delegation                    : PASS"
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
        == (
            "https://example.com/"
            "tata-motors-demand"
        )
    )

    assert (
        selected.result.source
        == "Mock Provider"
    )

    print(
        "Source Selection                     : PASS"
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

    assert (
        retrieved.url
        == selected.result.url
    )

    assert (
        retriever.received_urls[0]
        == selected.result.url
    )

    print(
        "HTTP Retrieval                       : PASS"
    )

    # ======================================================
    # NORMALIZATION
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

    assert normalized.normalized_text

    assert (
        normalized.url
        == retrieved.url
    )

    assert (
        normalized.original_content
        == retrieved.content
    )

    print(
        "Content Normalization                : PASS"
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
        == selected.result.url
    )

    assert (
        source_assessment.source_url
        == retrieved.url
    )

    assert (
        source_assessment.source_url
        == normalized.url
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
        "Source Assessment                   : PASS"
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
        == normalized.normalized_text
    )

    assert (
        observation.confidence
        == 70.0
    )

    print(
        "Observation Creation                : PASS"
    )

    # ======================================================
    # EXTERNAL PROVENANCE CHAIN
    # ======================================================

    assert (
        selected.result.url
        == retrieved.url
    )

    assert (
        retrieved.url
        == normalized.url
    )

    assert (
        normalized.url
        == source_assessment.source_url
    )

    assert (
        source_assessment.source_url
        == observation.source
    )

    print(
        "External Provenance Chain            : PASS"
    )

    # ======================================================
    # EXPLICIT EVIDENCE ASSESSMENT
    # ======================================================

    evidence_assessment = EvidenceAssessment(
        category="Demand",
        direction="Supporting",
        strength=85.0,
        confidence=80.0,
        independent_confirmation=1,
        is_primary_source=False,
        is_time_sensitive=True,
        notes=(
            "Explicit deterministic assessment "
            "for integration testing."
        ),
    )

    print(
        "Evidence Assessment Metadata         : PASS"
    )

    # ======================================================
    # EVIDENCE ASSESSMENT ENGINE
    # ======================================================

    assessment_engine = (
        EvidenceAssessmentEngine()
    )

    evidence = (
        assessment_engine.assess(
            observation=observation,
            assessment=evidence_assessment,
            evidence_id="FULL-EXT-EVID-001",
        )
    )

    assert evidence is not None

    assert (
        evidence.evidence_id
        == "FULL-EXT-EVID-001"
    )

    assert (
        evidence.statement
        == observation.description
    )

    assert (
        evidence.source
        == observation.source
    )

    assert (
        evidence.category
        == "Demand"
    )

    assert (
        evidence.direction
        == "Supporting"
    )

    assert (
        evidence.strength
        == 85.0
    )

    assert (
        evidence.confidence
        == 80.0
    )

    assert (
        evidence.independent_confirmation
        == 1
    )

    print(
        "Observation → EvidenceItem          : PASS"
    )

    # ======================================================
    # OPPORTUNITY EVIDENCE ENGINE
    # ======================================================

    opportunity_engine = (
        OpportunityEvidenceEngine()
    )

    pack = (
        opportunity_engine.analyze(
            company="Tata Motors",
            supporting_evidence=[
                evidence
            ],
            contradictory_evidence=[],
            assumptions=[
                "Demand improvement persists."
            ],
            kill_switches=[
                "Material demand reversal"
            ],
            monitoring_signals=[
                "Automotive demand growth"
            ],
        )
    )

    assert pack is not None

    print(
        "Opportunity Evidence Engine         : PASS"
    )

    # ======================================================
    # EVIDENCE HANDOFF
    # ======================================================

    assert (
        len(
            pack.supporting_evidence
        )
        == 1
    )

    assert (
        pack.supporting_evidence[0]
        is evidence
    )

    print(
        "Evidence → Opportunity Handoff       : PASS"
    )

    # ======================================================
    # DOWNSTREAM SCORING
    # ======================================================

    assert (
        0.0
        <= pack.evidence_score
        <= 100.0
    )

    assert (
        0.0
        <= pack.confidence
        <= 100.0
    )

    print(
        "Downstream Evidence Scoring          : PASS"
    )

    # ======================================================
    # FINAL PROVENANCE
    # ======================================================

    assert (
        pack.supporting_evidence[0].source
        == selected.result.url
    )

    assert (
        pack.supporting_evidence[0].statement
        == normalized.normalized_text
    )

    print(
        "Final Provenance Preservation        : PASS"
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
        source_assessment,
        "credibility_score",
    )

    assert not hasattr(
        source_assessment,
        "evidence_score",
    )

    assert not hasattr(
        observation,
        "opportunity_score",
    )

    print(
        "Analytical Boundary                  : PASS"
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
        "Input Immutability                    : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS FULL EXTERNAL → OPPORTUNITY "
        "EVIDENCE PIPELINE : ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()