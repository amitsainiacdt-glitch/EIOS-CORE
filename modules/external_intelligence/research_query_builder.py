"""
EIOS
Everest Investment Operating System

External Research Query Builder

Purpose
-------
Converts an existing research question into a deterministic
external research query.

Design Principles
-----------------
- Query generation only.
- No HTTP retrieval.
- No evidence creation.
- No evidence assessment.
- No analytical conclusions.
- Does not mutate the source Question.
- Deterministic output.
"""

from __future__ import annotations

from modules.research.question_engine import Question

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)


class ExternalResearchQueryBuilder:
    """
    Builds deterministic external research queries.
    """

    def build(
        self,
        *,
        company: str,
        ticker: str,
        question: Question,
        intent: str = "GENERAL_RESEARCH",
    ) -> ExternalResearchQuery:
        """
        Convert a research Question into an external query.

        The original question is preserved exactly.
        """

        if not company.strip():
            raise ValueError(
                "company must not be empty"
            )

        if not ticker.strip():
            raise ValueError(
                "ticker must not be empty"
            )

        if not question.question.strip():
            raise ValueError(
                "question must not be empty"
            )

        normalized_company = company.strip()
        normalized_ticker = ticker.strip()
        normalized_question = (
            question.question.strip()
        )
        normalized_intent = intent.strip()

        if not normalized_intent:
            raise ValueError(
                "intent must not be empty"
            )

        query = (
            f'"{normalized_company}" '
            f'"{normalized_ticker}" '
            f'{normalized_question}'
        )

        return ExternalResearchQuery(
            company=normalized_company,
            ticker=normalized_ticker,
            question=normalized_question,
            query=query,
            intent=normalized_intent,
        )


__all__ = [
    "ExternalResearchQueryBuilder",
]