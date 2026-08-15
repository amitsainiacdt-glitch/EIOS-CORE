"""
EIOS
Everest Investment Operating System

External Search Provider Contract
==================================

Purpose
-------
Defines the provider-neutral interface for external search.

Architecture

ExternalResearchQuery
        ↓
SearchProvider
        ↓
ExternalSearchResult[]

Design Principles
-----------------
- Provider-neutral.
- No investment analysis.
- No evidence assessment.
- No Signal creation.
- No valuation.
- No Opportunity scoring.
- Concrete providers implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class SearchProvider(ABC):
    """
    Abstract contract for an external search provider.
    """

    @abstractmethod
    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:
        """
        Execute an external search and return search results.

        Concrete providers are responsible only for search
        retrieval and result normalization.
        """

        raise NotImplementedError


__all__ = [
    "SearchProvider",
]