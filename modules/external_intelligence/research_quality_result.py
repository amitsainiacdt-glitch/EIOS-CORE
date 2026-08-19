"""
EIOS
Everest Investment Operating System

Research Quality Result
=======================

Passive result produced by ExternalResearchQualityEngine.

This module performs no retrieval, analysis, scoring,
or investment decision-making.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchQualityResult:
    """
    Immutable result of deterministic external research
    quality validation.
    """

    accepted: bool

    reason: str

    content_valid: bool

    source_valid: bool

    research_context_valid: bool


__all__ = [
    "ResearchQualityResult",
]