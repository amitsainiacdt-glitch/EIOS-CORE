"""
EIOS
Everest Investment Operating System

External Research Search Engine
================================

Purpose
-------
Coordinates an ExternalResearchQuery with a SearchProvider.

Architecture

ExternalResearchQuery
        ↓
ExternalResearchSearchEngine
        ↓
SearchProvider
        ↓
ExternalSearchResult[]

Design Principles
-----------------
- Orchestration only.
- No HTTP implementation.
- No provider-specific logic.
- No evidence creation.
- No observation creation.
- No signal creation.
- No scoring.
- Deterministic provider boundary.
"""

from __future__ import annotations

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class ExternalResearchSearchEngine:
    """
    Coordinates external research queries with a
    provider-neutral SearchProvider.
    """

    def __init__(
        self,
        provider: SearchProvider,
    ) -> None:

        if provider is None:
            raise ValueError(
                "provider must not be None"
            )

        self.provider = provider

    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:
        """
        Execute a validated external research query
        through the configured provider.
        """

        if query is None:
            raise ValueError(
                "query must not be None"
            )

        if not isinstance(
            query,
            ExternalResearchQuery,
        ):
            raise ValueError(
                "query must be an ExternalResearchQuery"
            )

        return list(
            self.provider.search(
                query
            )
        )


__all__ = [
    "ExternalResearchSearchEngine",
]