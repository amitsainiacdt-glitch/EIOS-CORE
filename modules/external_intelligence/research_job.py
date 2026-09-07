"""
EIOS
Everest Investment Operating System

Research Job
============

Represents one scheduled external research task.

Architecture

Research Job
     ↓
ExternalResearchQuery
     ↓
ExternalResearchOrchestrator

Design Principles
-----------------
- Passive typed data model only.
- No retrieval.
- No HTTP calls.
- No scheduling logic.
- No evidence creation.
- No opportunity scoring.
- Immutable job definition.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchJob:
    """
    Immutable definition of an external research task.

    The job describes WHAT EIOS wants to monitor.

    Scheduling infrastructure will determine WHEN
    the job is executed.
    """

    job_id: str

    company: str

    ticker: str

    question: str

    intent: str

    frequency_minutes: int

    enabled: bool = True

    priority: int = 50

    max_sources: int = 5

    observation_category: str = "External Web"

    observation_confidence: float = 70.0

    entity_domain: str | None = None
    quarter_period_end: str | None = None

    def validate(self) -> None:
        """
        Validate the research job definition.
        """

        if not self.job_id.strip():
            raise ValueError(
                "job_id must not be empty"
            )

        if not self.company.strip():
            raise ValueError(
                "company must not be empty"
            )

        if not self.ticker.strip():
            raise ValueError(
                "ticker must not be empty"
            )

        if not self.question.strip():
            raise ValueError(
                "question must not be empty"
            )

        if not self.intent.strip():
            raise ValueError(
                "intent must not be empty"
            )

        if self.frequency_minutes <= 0:
            raise ValueError(
                "frequency_minutes must be greater than zero"
            )

        if self.priority < 0:
            raise ValueError(
                "priority must not be negative"
            )

        if self.max_sources <= 0:
            raise ValueError(
                "max_sources must be greater than zero"
            )

        if not (
            0.0
            <= self.observation_confidence
            <= 100.0
        ):
            raise ValueError(
                "observation_confidence must be "
                "between 0 and 100"
            )

        if self.entity_domain is not None and not self.entity_domain.strip():
            raise ValueError("entity_domain must be None or a non-empty domain")
        if self.quarter_period_end is not None:
            from modules.company_intelligence.quarterly_search_target import quarterly_search_plan
            if self.intent != 'OFFICIAL_DOCUMENT_DISCOVERY' or not self.entity_domain:
                raise ValueError('Quarter targeting requires official-document intent and issuer domain')
            quarterly_search_plan(self.company, self.entity_domain, self.quarter_period_end)


__all__ = [
    "ResearchJob",
]
