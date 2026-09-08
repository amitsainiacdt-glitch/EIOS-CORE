"""
EIOS
Everest Investment Operating System

External Research Orchestrator
==============================

Purpose
-------
Coordinates the external research retrieval workflow.

Architecture

ExternalResearchQuery
        ↓
ExternalResearchSearchEngine
        ↓
ExternalSourceSelectionEngine
        ↓
HTTPExternalRetriever
        ↓
RetrievedContent
        ↓
ExternalContentNormalizer
        ↓
NormalizedExternalContent
        ↓
ExternalSourceAssessmentEngine
        ↓
ExternalSourceAssessment
        ↓
ExternalResearchQualityEngine
        ↓
ExternalObservationAdapter
        ↓
Observation[]

Design Principles
-----------------
- Orchestration only.
- Does not create Evidence.
- Does not create Signals.
- Does not perform valuation.
- Does not score opportunities.
- Does not perform investment analysis.
- Uses existing EIOS external-intelligence components.
- Preserves provenance.
- Preserves original retrieved content.
- One failed source must not terminate the entire research run.
- Research quality is a deterministic acceptance gate.
- Duplicate observations are not added to the result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from modules.external_intelligence.external_content_normalizer import (
    ExternalContentNormalizer,
    NormalizedExternalContent,
)

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
)

from modules.external_intelligence.external_research_quality_engine import (
    ExternalResearchQualityEngine,
)

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)

from modules.external_intelligence.external_source_assessment_engine import (
    ExternalSourceAssessmentEngine,
)

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
    RetrievedContent,
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
from modules.external_intelligence.source_quality_service import SourceQualityService

from modules.external_intelligence.source_selection import (
    SelectedSource,
)

from modules.external_intelligence.source_selection_engine import (
    ExternalSourceSelectionEngine,
)

from modules.observation.observation import (
    Observation,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)


# ==========================================================
# RETRIEVAL FAILURE
# ==========================================================


@dataclass(frozen=True)
class RetrievalFailure:
    """
    Records a failed external retrieval.

    This is provenance/status information only.
    It contains no analytical interpretation.
    """

    url: str

    error_type: str

    error_message: str


# ==========================================================
# EXTERNAL RESEARCH RESULT
# ==========================================================


@dataclass
class ExternalResearchResult:
    """
    Complete result of one external research retrieval run.

    This is an orchestration result only.

    It contains:
        - selected sources
        - retrieved content
        - normalized content
        - source assessments
        - observations
        - retrieval failures

    It does not contain:
        - Evidence
        - Signals
        - Catalysts
        - Valuation
        - Opportunity scores
    """

    query: ExternalResearchQuery = field(
        default_factory=lambda: ExternalResearchQuery(
            company="",
            ticker="",
            question="",
            query="",
            intent="",
        )
    )

    selected_sources: list[SelectedSource] = field(
        default_factory=list
    )

    retrieved_content: list[RetrievedContent] = field(
        default_factory=list
    )

    normalized_content: list[
        NormalizedExternalContent
    ] = field(
        default_factory=list
    )

    source_assessments: list[
        ExternalSourceAssessment
    ] = field(
        default_factory=list
    )

    observations: list[Observation] = field(
        default_factory=list
    )

    retrieval_failures: list[RetrievalFailure] = field(
        default_factory=list
    )

    job_id: str | None = None
    execution_count: int = 0
    observation_count: int = 0
    quarter_screening: dict | None = None


# ==========================================================
# ORCHESTRATOR
# ==========================================================


class ExternalResearchOrchestrator:
    """
    Coordinates external research retrieval.

    The orchestrator performs no investment analysis.

    Content normalization is a deterministic transformation
    performed by ExternalContentNormalizer.

    Source assessment is a deterministic metadata
    construction performed by
    ExternalSourceAssessmentEngine.

    Research quality is a deterministic acceptance gate
    performed by ExternalResearchQualityEngine.
    """

    def __init__(
        self,
        provider: SearchProvider,
        *,
        observation_engine: ObservationEngine | None = None,
        retriever: HTTPExternalRetriever | None = None,
        source_selection_engine: (
            ExternalSourceSelectionEngine | None
        ) = None,
        content_normalizer: (
            ExternalContentNormalizer | None
        ) = None,
        source_assessment_engine: (
            ExternalSourceAssessmentEngine | None
        ) = None,
        research_quality_engine: (
            ExternalResearchQualityEngine | None
        ) = None,
    ) -> None:

        if provider is None:
            raise ValueError(
                "provider must not be None"
            )

        # ==================================================
        # SEARCH
        # ==================================================

        self.search_engine = (
            ExternalResearchSearchEngine(
                provider
            )
        )

        # ==================================================
        # SOURCE SELECTION
        # ==================================================

        self.source_selection_engine = (
            source_selection_engine
            if source_selection_engine is not None
            else ExternalSourceSelectionEngine()
        )

        # ==================================================
        # HTTP RETRIEVAL
        # ==================================================

        self.retriever = (
            retriever
            if retriever is not None
            else HTTPExternalRetriever()
        )

        # ==================================================
        # CONTENT NORMALIZATION
        # ==================================================

        self.content_normalizer = (
            content_normalizer
            if content_normalizer is not None
            else ExternalContentNormalizer()
        )

        # ==================================================
        # SOURCE ASSESSMENT
        # ==================================================

        self.source_assessment_engine = (
            source_assessment_engine
            if source_assessment_engine is not None
            else ExternalSourceAssessmentEngine()
        )

        # ==================================================
        # RESEARCH QUALITY
        # ==================================================

        self.research_quality_engine = (
            research_quality_engine
            if research_quality_engine is not None
            else ExternalResearchQualityEngine()
        )

        # ==================================================
        # OBSERVATION
        # ==================================================

        self.observation_engine = (
            observation_engine
            if observation_engine is not None
            else ObservationEngine()
        )

        self.observation_adapter = (
            ExternalObservationAdapter(
                self.observation_engine
            )
        )

    # ======================================================
    # EXECUTE
    # ======================================================

    def execute(
        self,
        query: ExternalResearchQuery,
        *,
        max_sources: int = 5,
        observation_category: str = "External Web",
        observation_confidence: float = 70.0,
        cycle_id: str | None = None,
        job_id: str | None = None,
        retrieved_at: datetime | None = None,
        entity_domain: str | None = None,
    ) -> ExternalResearchResult:
        """
        Execute external research retrieval.

        Workflow:

            Query
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
            Research Quality Gate
              ↓
            Observation

        Retrieval failures are recorded and do not
        terminate the complete research run.

        Research that fails the deterministic quality
        gate does not become an Observation.

        Duplicate observations are rejected by
        ObservationEngine and are not inserted into
        the result list.
        """

        if query is None:
            raise ValueError(
                "query must not be None"
            )

        # ==================================================
        # SEARCH
        # ==================================================

        quarter_plan = None
        quarter_screening = None
        if query.quarter_period_end is not None:
            from dataclasses import replace
            from modules.company_intelligence.quarterly_search_target import quarterly_search_plan, assess_quarterly_search_results
            if query.intent != 'OFFICIAL_DOCUMENT_DISCOVERY' or not query.issuer_domain:
                raise ValueError('Quarter targeting requires official-document intent and issuer domain')
            quarter_plan = quarterly_search_plan(query.company, query.issuer_domain, query.quarter_period_end)
            query = replace(query, query=quarter_plan['queries'][0])
        search_results = (
            self.search_engine.search(
                query
            )
        )

        # ==================================================
        # SOURCE SELECTION
        # ==================================================

        if quarter_plan is not None:
            quarter_screening = assess_quarterly_search_results(search_results, quarter_plan)
            search_results = [result for result, assessment in zip(search_results, quarter_screening['results'])
                              if assessment['status'] == 'TARGET_QUARTER_CANDIDATE']
        selected_sources = (
            self.source_selection_engine.select(
                search_results,
                max_results=max_sources,
            )
        )

        # ==================================================
        # COLLECTIONS
        # ==================================================

        retrieved_content: list[
            RetrievedContent
        ] = []

        normalized_content: list[
            NormalizedExternalContent
        ] = []

        source_assessments: list[
            ExternalSourceAssessment
        ] = []

        observations: list[
            Observation
        ] = []

        retrieval_failures: list[
            RetrievalFailure
        ] = []

        # ==================================================
        # SOURCE LOOP
        # ==================================================

        for selected_source in selected_sources:

            result = selected_source.result

            # ==================================================
            # RETRIEVAL
            # ==================================================

            try:

                retrieved = (
                    self.retriever.retrieve(
                        result.url
                    )
                )

            except Exception as exc:
                # Some official sites block direct automated PDF retrieval.
                # Accept only the provider's preserved raw copy of the exact
                # result URL; never promote the shorter search snippet.
                if getattr(result, "raw_content", "") and getattr(result, "delivery_provider", ""):
                    retrieved = RetrievedContent(
                        url=result.url,
                        status_code=200,
                        content=result.raw_content,
                        content_type="text/plain; delivery=provider-mediated",
                        headers={
                            "X-EIOS-Delivery-Provider": result.delivery_provider,
                            "X-EIOS-Direct-Retrieval-Error": type(exc).__name__,
                        },
                    )
                else:
                    retrieval_failures.append(
                        RetrievalFailure(
                            url=result.url,
                            error_type=type(exc).__name__,
                            error_message=str(exc),
                        )
                    )
                    continue

            # ==================================================
            # SUCCESSFUL RETRIEVAL
            # ==================================================

            retrieved_content.append(
                retrieved
            )

            # ==================================================
            # NORMALIZATION
            # ==================================================

            try:

                normalized = (
                    self.content_normalizer.normalize(
                        retrieved
                    )
                )

            except Exception as exc:

                retrieval_failures.append(
                    RetrievalFailure(
                        url=result.url,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )

                continue

            normalized_content.append(
                normalized
            )

            # ==================================================
            # SOURCE ASSESSMENT
            # ==================================================

            try:

                source_assessment = (
                    self.source_assessment_engine.assess(
                        selected_source=selected_source,
                        retrieved_content=retrieved,
                        normalized_content=normalized,
                    )
                )

            except Exception as exc:

                retrieval_failures.append(
                    RetrievalFailure(
                        url=result.url,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )

                continue

            source_assessments.append(
                source_assessment
            )

            # ==================================================
            # RESEARCH QUALITY GATE
            # ==================================================
            #
            # This is a deterministic structural gate.
            #
            # It does not perform:
            # - semantic interpretation
            # - claim extraction
            # - contradiction detection
            # - valuation
            # - opportunity scoring
            #
            # Research that fails this gate is not converted
            # into an Observation.
            # ==================================================

            try:

                quality_result = (
                    self.research_quality_engine.assess(
                        query=query,
                        normalized_content=normalized,
                        source_assessment=source_assessment,
                    )
                )

            except Exception as exc:

                retrieval_failures.append(
                    RetrievalFailure(
                        url=result.url,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )

                continue

            if not quality_result.accepted:

                continue

            # Official-document and exchange jobs are fail-closed: a third-party
            # result may remain useful elsewhere, but it cannot enter an official
            # intake lane. Issuer and regulatory domains are Tier 1.
            classification = SourceQualityService().classify(
                result.url,
                entity_domain=entity_domain,
            )
            if query.intent in {"OFFICIAL_DOCUMENT_DISCOVERY", "EXCHANGE_DISCLOSURES", "PRIMARY_INDICATOR_MONITORING"} and classification.quality_tier != "TIER_1":
                continue

            # ==================================================
            # OBSERVATION
            # ==================================================

            observation = (
                self.observation_adapter.ingest(
                    title=result.title,
                    description=(
                        normalized.normalized_text
                    ),
                    source=result.url,
                    category=observation_category,
                    entity=query.company,
                    confidence=observation_confidence,
                    cycle_id=cycle_id,
                    job_id=job_id,
                    research_intent=query.intent,
                    retrieved_at=retrieved_at,
                    content_type=normalized.content_type,
                    extraction_method=retrieved.headers.get("X-EIOS-Delivery-Provider"),
                    entity_domain=entity_domain,
                )
            )

            # --------------------------------------------------
            # DUPLICATE PROTECTION
            # --------------------------------------------------
            #
            # ObservationEngine returns None when the
            # information already exists.
            #
            # None is NOT a valid Observation and must
            # never enter ExternalResearchResult.observations.
            #
            # This preserves the contract:
            #
            # observations: list[Observation]
            #
            # rather than:
            #
            # observations: list[Observation | None]
            # --------------------------------------------------

            if observation is not None:

                observations.append(
                    observation
                )

        # ==================================================
        # RESULT
        # ==================================================

        return ExternalResearchResult(
            query=query,
            selected_sources=selected_sources,
            retrieved_content=retrieved_content,
            normalized_content=normalized_content,
            source_assessments=source_assessments,
            observations=observations,
            retrieval_failures=retrieval_failures,
            job_id=job_id,
            execution_count=1 if job_id is not None else 0,
            observation_count=len(observations),
            quarter_screening=quarter_screening,
        )


# ==========================================================
# PUBLIC API
# ==========================================================


__all__ = [
    "RetrievalFailure",
    "ExternalResearchResult",
    "ExternalResearchOrchestrator",
]
