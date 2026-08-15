"""
EIOS
Everest Investment Operating System

External Source Selection Engine
=================================

Purpose
-------
Selects external search results for downstream retrieval.

This engine performs routing/filtering only.

It does NOT:
- assess evidence quality
- calculate confidence
- calculate investment relevance
- create Evidence
- create Signals
- create Catalysts
- perform valuation
- rank investment opportunities

Selection principles:
- Valid URL required.
- Title or snippet should contain useful content.
- Duplicate URLs are removed.
- Original search ordering is preserved.
- Selection is deterministic.
"""

from __future__ import annotations

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.external_intelligence.source_selection import (
    SelectedSource,
)


class ExternalSourceSelectionEngine:
    """
    Deterministic routing/filtering engine for external
    search results.
    """

    def select(
        self,
        results: list[ExternalSearchResult],
        *,
        max_results: int = 5,
    ) -> list[SelectedSource]:
        """
        Select valid and unique external sources.

        No analytical ranking is performed.
        """

        if results is None:
            raise ValueError(
                "results must not be None"
            )

        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero"
            )

        selected: list[SelectedSource] = []

        seen_urls: set[str] = set()

        for result in results:

            if not isinstance(
                result,
                ExternalSearchResult,
            ):
                continue

            url = result.url.strip()

            if not url:
                continue

            if not (
                url.startswith("http://")
                or url.startswith("https://")
            ):
                continue

            if url in seen_urls:
                continue

            title = result.title.strip()

            snippet = result.snippet.strip()

            if not title and not snippet:
                continue

            seen_urls.add(url)

            selected.append(
                SelectedSource(
                    result=result,
                    selection_reason=(
                        "Valid unique search result "
                        "selected for retrieval."
                    ),
                )
            )

            if len(selected) >= max_results:
                break

        return selected


__all__ = [
    "ExternalSourceSelectionEngine",
]