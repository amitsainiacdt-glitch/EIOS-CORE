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

The test uses an isolated temporary observation store so that
historical production/test observations cannot affect novelty
detection.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

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

from modules.observation.observation_persistence import (
    ObservationPersistence,
)

from modules.observation.observation_registry import (
    ObservationRegistry,
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

    print("=" * 60)
    print(
        "EIOS EXTERNAL RESEARCH → EVIDENCE "
        "INTEGRATION TEST"
    )
    print("=" * 60)

    # ======================================================
    # ISOLATED TEST STATE
    # ======================================================

    with TemporaryDirectory() as temp_dir:

        observation_path = (
            Path(temp_dir)
            / "observations.json"
        )

        persistence = ObservationPersistence(
            observation_path
        )

        registry = ObservationRegistry()

        observation_engine = ObservationEngine(
            registry=registry,
            persistence=persistence,
        )

        # ==================================================
        # RESEARCH QUERY
        # ==================================================

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

        # ==================================================
        # SEARCH ENGINE
        # ==================================================

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

        # ==================================================
        # HTTP RETRIEVAL
        # ==================================================

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

        # ==================================================
        # OBSERVATION
        # ==================================================

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

        assert (
            observation.entity
            == "Test Company"
        )

        assert (
            observation.category
            == "External Web"
        )

        assert (
            observation.confidence
            == 75.0
        )

        print(
            "Observation Creation           : PASS"
        )

        # ==================================================
        # EVIDENCE ASSESSMENT
        # ==================================================

        assessment = EvidenceAssessment(

            category="Industry",

            direction="Supporting",

            strength=80.0,

            confidence=85.0,

            independent_confirmation=1,

            is_primary_source=False,

            is_time_sensitive=False,

            notes=(
                "Synthetic external research evidence."
            ),
        )

        assessment_engine = (
            EvidenceAssessmentEngine()
        )

        evidence = (
            assessment_engine.assess(
                observation=observation,
                assessment=assessment,
                evidence_id="EXT-EVIDENCE-001",
            )
        )

        assert evidence is not None

        print(
            "EvidenceItem Creation          : PASS"
        )

        # ==================================================
        # EVIDENCE IDENTITY
        # ==================================================

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
            == "Industry"
        )

        assert (
            evidence.direction
            == "Supporting"
        )

        print(
            "Evidence Identity Preservation  : PASS"
        )

        # ==================================================
        # SOURCE PRESERVATION
        # ==================================================

        assert (
            evidence.source
            == "https://example.com"
        )

        print(
            "Source Preservation             : PASS"
        )

        # ==================================================
        # OPPORTUNITY EVIDENCE ENGINE
        # ==================================================

        opportunity_engine = (
            OpportunityEvidenceEngine()
        )

        opportunity_evidence = (
            opportunity_engine.analyze(
                company="Test Company",
                supporting_evidence=[
                    evidence
                ],
                contradictory_evidence=[],
                assumptions=[],
                kill_switches=[],
                monitoring_signals=[],
            )
        )

        assert (
            opportunity_evidence is not None
        )

        print(
            "Opportunity Evidence Engine     : PASS"
        )

        # ==================================================
        # EVIDENCE → OPPORTUNITY HANDOFF
        # ==================================================

        assert (
            len(
                opportunity_evidence.supporting_evidence
            )
            == 1
        )

        assert (
            opportunity_evidence.supporting_evidence[0]
            is evidence
        )

        print(
            "Evidence → Opportunity Handoff  : PASS"
        )

        # ==================================================
        # DOWNSTREAM SCORING
        # ==================================================

        assert (
            opportunity_evidence.evidence_score
            >= 0
        )

        assert (
            opportunity_evidence.evidence_score
            <= 100
        )

        print(
            "Downstream Evidence Scoring     : PASS"
        )

        # ==================================================
        # ANALYTICAL BOUNDARY
        # ==================================================

        assert not hasattr(
            observation,
            "valuation",
        )

        assert not hasattr(
            observation,
            "opportunity_score",
        )

        assert not hasattr(
            observation,
            "catalyst_score",
        )

        assert not hasattr(
            evidence,
            "valuation",
        )

        assert not hasattr(
            evidence,
            "opportunity_score",
        )

        print(
            "Analytical Boundary             : PASS"
        )

        # ==================================================
        # PERSISTENCE ISOLATION
        # ==================================================

        assert observation_path.exists()

        reloaded_engine = ObservationEngine(
            persistence=ObservationPersistence(
                observation_path
            )
        )

        assert (
            reloaded_engine.registry.count()
            == 1
        )

        assert (
            reloaded_engine.registry.latest().title
            == search_result.title
        )

        print(
            "Observation Persistence         : PASS"
        )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "EIOS EXTERNAL RESEARCH → EVIDENCE : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()