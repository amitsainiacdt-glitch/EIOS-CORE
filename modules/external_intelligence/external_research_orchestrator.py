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
- One failed source must not terminate the entire research run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
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

    observations: list[Observation] = field(
        default_factory=list
    )

    retrieval_failures: list[RetrievalFailure] = field(
        default_factory=list
    )


class ExternalResearchOrchestrator:
    """
    Coordinates external research retrieval.

    The orchestrator does not perform any analytical
    transformation of external information.
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
        # RETRIEVE + OBSERVE
        # --------------------------------------------------

        retrieved_content: list[
            RetrievedContent
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
            # OBSERVATION
            # ----------------------------------------------

            observation = (
                self.observation_adapter.ingest(
                    title=result.title,
                    description=retrieved.content,
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
            observations=observations,
            retrieval_failures=retrieval_failures,
        )


__all__ = [
    "RetrievalFailure",
    "ExternalResearchResult",
    "ExternalResearchOrchestrator",
]