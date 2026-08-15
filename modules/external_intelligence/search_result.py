"""
EIOS
Everest Investment Operating System

External Search Result
======================

Purpose
-------
Represents one result returned by an external search provider.

This is a passive data model.

It does NOT:
- perform search
- retrieve URLs
- assess evidence
- calculate confidence
- create Signals
- create Catalysts
- calculate valuation
- make Opportunity decisions
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalSearchResult:
    """
    Immutable result returned by a search provider.
    """

    title: str = ""

    url: str = ""

    snippet: str = ""

    source: str = ""


__all__ = [
    "ExternalSearchResult",
]