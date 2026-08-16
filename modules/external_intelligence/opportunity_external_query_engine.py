"""
EIOS
Everest Investment Operating System

Opportunity External Query Engine
==================================

Purpose
-------
Bridges Opportunity Research Questions into the
External Intelligence query layer.

Architecture

OpportunityResearchIntake
        ↓
OpportunityResearchQuestionBuilder
        ↓
Question[]
        ↓
ExternalResearchQueryBuilder
        ↓
ExternalResearchQuery[]

Design Principles
-----------------
- Translation/orchestration only.
- Does not perform HTTP retrieval.
- Does not perform search.
- Does not create Observations.
- Does not create Evidence.
- Does not create Signals.
- Does not perform valuation.
- Does not score opportunities.
- Does not mutate the OpportunityResearchIntake.
- Does not mutate Question objects.
"""

from __future__ import annotations

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.research_query_builder import (
    ExternalResearchQueryBuilder,
)

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)

from modules.opportunity.research_question_builder import (
    OpportunityResearchQuestionBuilder,
)


class OpportunityExternalQueryEngine:
    """
    Converts Opportunity research questions into
    deterministic external research queries.
    """

    DEFAULT_INTENT = "OPPORTUNITY_RESEARCH"

    def __init__(
        self,
        question_builder: (
            OpportunityResearchQuestionBuilder | None
        ) = None,
        query_builder: (
            ExternalResearchQueryBuilder | None
        ) = None,
    ) -> None:

        self.question_builder = (
            question_builder
            if question_builder is not None
            else OpportunityResearchQuestionBuilder()
        )

        self.query_builder = (
            query_builder
            if query_builder is not None
            else ExternalResearchQueryBuilder()
        )

    # ======================================================
    # BUILD
    # ======================================================

    def build(
        self,
        intake: OpportunityResearchIntake,
    ) -> list[ExternalResearchQuery]:
        """
        Convert Opportunity research questions into
        external research queries.
        """

        if intake is None:
            raise ValueError(
                "intake must not be None"
            )

        if not intake.company.strip():
            raise ValueError(
                "intake.company must not be empty"
            )

        if not intake.ticker.strip():
            raise ValueError(
                "intake.ticker must not be empty"
            )

        questions = (
            self.question_builder.build(
                intake
            )
        )

        queries: list[
            ExternalResearchQuery
        ] = []

        for question in questions:

            queries.append(
                self.query_builder.build(
                    company=intake.company,
                    ticker=intake.ticker,
                    question=question,
                    intent=self.DEFAULT_INTENT,
                )
            )

        return queries


__all__ = [
    "OpportunityExternalQueryEngine",
]