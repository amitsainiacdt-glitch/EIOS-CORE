"""
EIOS
Everest Investment Operating System

External Research Query

Purpose
-------
Represents a deterministic external research request.

Architecture
------------
Research Question
        ↓
Research Query
        ↓
External Retriever

Design Principles
-----------------
- Passive typed data model only.
- No retrieval.
- No HTTP calls.
- No evidence assessment.
- No signal creation.
- No analytical conclusions.
- Preserves the originating research question.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalResearchQuery:
    """
    Immutable external research query.

    Represents what EIOS intends to search for,
    not what the external world has confirmed.
    """

    company: str

    ticker: str

    question: str

    query: str

    intent: str


__all__ = [
    "ExternalResearchQuery",
]