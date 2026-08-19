"""
EIOS
Everest Investment Operating System

Research Execution Service
==========================

Bridges scheduled ResearchJob objects with the existing
ExternalResearchOrchestrator.

Responsibilities:
    - Convert ResearchJob question text into the existing
      EIOS Question model.
    - Build ExternalResearchQuery.
    - Execute external research.
    - Record scheduler execution state.

Does NOT:
    - perform scheduling decisions
    - implement HTTP retrieval
    - create evidence
    - create signals
    - score opportunities
"""

from __future__ import annotations

from datetime import datetime

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
    ExternalResearchResult,
)

from modules.external_intelligence.research_query_builder import (
    ExternalResearchQueryBuilder,
)

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_scheduler import (
    ResearchScheduler,
)

from modules.research.question_engine import (
    Question,
)


class ResearchExecutionService:
    """
    Executes ResearchJob objects through the existing
    EIOS external research architecture.

    ResearchJob stores question text as a passive string.

    At the execution boundary, that text is converted into
    the existing EIOS Question model required by
    ExternalResearchQueryBuilder.
    """

    def __init__(
        self,
        orchestrator: ExternalResearchOrchestrator,
        scheduler: ResearchScheduler,
        query_builder: (
            ExternalResearchQueryBuilder | None
        ) = None,
    ) -> None:

        if orchestrator is None:
            raise ValueError(
                "orchestrator must not be None"
            )

        if scheduler is None:
            raise ValueError(
                "scheduler must not be None"
            )

        self.orchestrator = orchestrator

        self.scheduler = scheduler

        self.query_builder = (
            query_builder
            if query_builder is not None
            else ExternalResearchQueryBuilder()
        )

    # ======================================================
    # QUESTION ADAPTER
    # ======================================================

    @staticmethod
    def _build_question(
        question_text: str,
    ) -> Question:
        """
        Convert ResearchJob question text into the
        existing EIOS Question model.

        ResearchJob remains a passive string-based
        scheduling definition.
        """

        if not question_text.strip():
            raise ValueError(
                "question must not be empty"
            )

        return Question(
            question=question_text.strip(),
            weight=1,
        )

    # ======================================================
    # EXECUTE
    # ======================================================

    def execute(
        self,
        job: ResearchJob,
        *,
        run_time: datetime,
    ) -> ExternalResearchResult:
        """
        Execute one research job.

        Workflow:

            ResearchJob
                ↓
            Question adapter
                ↓
            ExternalResearchQueryBuilder
                ↓
            ExternalResearchOrchestrator
                ↓
            Observation Engine

        Scheduler state is updated only after successful
        orchestrator execution.
        """

        if job is None:
            raise ValueError(
                "job must not be None"
            )

        job.validate()

        question = self._build_question(
            job.question
        )

        query = self.query_builder.build(
            company=job.company,
            ticker=job.ticker,
            question=question,
            intent=job.intent,
        )

        result = self.orchestrator.execute(
            query,
            max_sources=job.max_sources,
            observation_category=(
                job.observation_category
            ),
            observation_confidence=(
                job.observation_confidence
            ),
        )

        self.scheduler.mark_run(
            job,
            run_time,
        )

        return result


__all__ = [
    "ResearchExecutionService",
]