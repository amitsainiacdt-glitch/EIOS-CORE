"""
EIOS
Everest Investment Operating System

External Source Selection
==========================

Purpose
-------
Represents the result of selecting external search results for
further retrieval.

Design Principles
-----------------
- Passive data model only.
- Preserves search-result provenance.
- Does not calculate evidence quality.
- Does not calculate investment relevance.
- Does not create Evidence.
- Does not create Signals.
- Does not perform valuation.
"""

from dataclasses import dataclass

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


@dataclass(frozen=True)
class SelectedSource:
    """
    Immutable selected external source.

    Selection is a routing decision, not an evidence conclusion.
    """

    result: ExternalSearchResult

    selection_reason: str = ""


__all__ = [
    "SelectedSource",
]