"""
EIOS
Everest Investment Operating System

External Research Quality Engine
================================

Purpose
-------
Performs deterministic quality gating between external research
retrieval and Observation creation.

This engine does not:
    - perform retrieval
    - perform HTTP requests
    - create Evidence
    - create Intelligence
    - perform valuation
    - score opportunities
    - make investment decisions
"""

from __future__ import annotations

from modules.external_intelligence.external_content_normalizer import (
    NormalizedExternalContent,
)

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.research_quality_result import (
    ResearchQualityResult,
)


class ExternalResearchQualityEngine:
    """
    Deterministic quality gate for externally retrieved research.

    The engine performs structural validation only.
    """

    def assess(
        self,
        *,
        query: ExternalResearchQuery,
        normalized_content: NormalizedExternalContent,
        source_assessment: ExternalSourceAssessment,
    ) -> ResearchQualityResult:

        if query is None:
            raise ValueError(
                "query must not be None"
            )

        if normalized_content is None:
            raise ValueError(
                "normalized_content must not be None"
            )

        if source_assessment is None:
            raise ValueError(
                "source_assessment must not be None"
            )

        content_valid = (
            self._content_is_valid(
                normalized_content
            )
        )

        source_valid = (
            self._source_is_valid(
                normalized_content,
                source_assessment,
            )
        )

        research_context_valid = (
            self._research_context_is_valid(
                query
            )
        )

        if not content_valid:

            return ResearchQualityResult(
                accepted=False,
                reason=(
                    "Normalized research content is "
                    "empty or insufficient."
                ),
                content_valid=False,
                source_valid=source_valid,
                research_context_valid=(
                    research_context_valid
                ),
            )

        if not source_valid:

            return ResearchQualityResult(
                accepted=False,
                reason=(
                    "External source provenance is "
                    "incomplete or invalid."
                ),
                content_valid=True,
                source_valid=False,
                research_context_valid=(
                    research_context_valid
                ),
            )

        if not research_context_valid:

            return ResearchQualityResult(
                accepted=False,
                reason=(
                    "Research query context is "
                    "incomplete."
                ),
                content_valid=True,
                source_valid=True,
                research_context_valid=False,
            )

        return ResearchQualityResult(
            accepted=True,
            reason=(
                "External research passed deterministic "
                "quality validation."
            ),
            content_valid=True,
            source_valid=True,
            research_context_valid=True,
        )

    @staticmethod
    def _content_is_valid(
        normalized_content: NormalizedExternalContent,
    ) -> bool:

        text = (
            normalized_content.normalized_text
        )

        if not isinstance(
            text,
            str,
        ):
            return False

        return (
            len(
                text.strip()
            )
            >= 50
        )

    @staticmethod
    def _source_is_valid(
        normalized_content: NormalizedExternalContent,
        source_assessment: ExternalSourceAssessment,
    ) -> bool:

        if not source_assessment.provenance_complete:
            return False

        if not normalized_content.url:
            return False

        if (
            source_assessment.source_url
            != normalized_content.url
        ):
            return False

        if (
            normalized_content.status_code
            < 200
            or normalized_content.status_code
            >= 400
        ):
            return False

        return True

    @staticmethod
    def _research_context_is_valid(
        query: ExternalResearchQuery,
    ) -> bool:

        return all(
            isinstance(
                value,
                str,
            )
            and bool(
                value.strip()
            )
            for value in (
                query.company,
                query.ticker,
                query.question,
                query.query,
                query.intent,
            )
        )


__all__ = [
    "ExternalResearchQualityEngine",
]