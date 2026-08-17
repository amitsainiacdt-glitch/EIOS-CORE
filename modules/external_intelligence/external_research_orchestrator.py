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
- Does not perform source-quality analysis.
- Does not perform investment analysis.
- Uses existing EIOS external-intelligence components.
- Preserves provenance.
- Preserves original retrieved content.
- One failed source must not terminate the entire research run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from modules.external_intelligence.external_content_normalizer import (
    ExternalContentNormalizer,
    NormalizedExternalContent,
)

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
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


class ExternalResearchOrchestrator:
    """
    Coordinates external research retrieval.

    The orchestrator performs no investment analysis.

    Content normalization is a deterministic transformation
    performed by ExternalContentNormalizer.

    Source assessment is a deterministic metadata
    construction performed by
    ExternalSourceAssessmentEngine.
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
    ) -> None:

        if provider is None:
            raise ValueError(
                "provider must not be None"
            )

        self.search_engine = (
            ExternalResearchSearchEngine(
                provider
            )
        )

        self.source_selection_engine = (
            source_selection_engine
            if source_selection_engine is not None
            else ExternalSourceSelectionEngine()
        )

        self.retriever = (
            retriever
            if retriever is not None
            else HTTPExternalRetriever()
        )

        self.content_normalizer = (
            content_normalizer
            if content_normalizer is not None
            else ExternalContentNormalizer()
        )

        self.source_assessment_engine = (
            source_assessment_engine
            if source_assessment_engine is not None
            else ExternalSourceAssessmentEngine()
        )

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
            Observation

        Retrieval failures are recorded and do not
        terminate the complete research run.
        """

        if query is None:
            raise ValueError(
                "query must not be None"
            )

        # --------------------------------------------------
        # SEARCH
        # --------------------------------------------------

        search_results = (
            self.search_engine.search(
                query
            )
        )

        # --------------------------------------------------
        # SOURCE SELECTION
        # --------------------------------------------------

        selected_sources = (
            self.source_selection_engine.select(
                search_results,
                max_results=max_sources,
            )
        )

        # --------------------------------------------------
        # RETRIEVE + NORMALIZE + ASSESS + OBSERVE
        # --------------------------------------------------

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

        for selected_source in selected_sources:

            result = selected_source.result

            # ----------------------------------------------
            # RETRIEVAL
            # ----------------------------------------------

            try:

                retrieved = (
                    self.retriever.retrieve(
                        result.url
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

            # ----------------------------------------------
            # SUCCESSFUL RETRIEVAL
            # ----------------------------------------------

            retrieved_content.append(
                retrieved
            )

            # ----------------------------------------------
            # NORMALIZATION
            # ----------------------------------------------

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

            # ----------------------------------------------
            # SOURCE ASSESSMENT
            # ----------------------------------------------

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

            # ----------------------------------------------
            # OBSERVATION
            # ----------------------------------------------

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
                )
            )

            observations.append(
                observation
            )

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        return ExternalResearchResult(
            query=query,
            selected_sources=selected_sources,
            retrieved_content=retrieved_content,
            normalized_content=normalized_content,
            source_assessments=source_assessments,
            observations=observations,
            retrieval_failures=retrieval_failures,
        )


__all__ = [
    "RetrievalFailure",
    "ExternalResearchResult",
    "ExternalResearchOrchestrator",
]