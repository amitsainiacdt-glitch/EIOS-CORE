"""
EIOS
Everest Investment Operating System

Discovery → Opportunity Research Intake

Purpose:
Creates the typed hand-off from the Discovery Office
into Opportunity research.

Design Principles:
- Passive data model only.
- No scoring.
- No valuation.
- No opportunity conclusions.
- No invented analytical inputs.
- Preserves Discovery evidence.
- Opportunity research begins from this object.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class OpportunityResearchIntake:
    """
    Typed research request created from a Discovery Candidate.

    This object represents the START of Opportunity research,
    not the result of Opportunity analysis.
    """

    # ======================================================
    # Identity
    # ======================================================

    company: str = ""

    ticker: str = ""

    sector: str = ""

    industry: str = ""

    # ======================================================
    # Discovery Context
    # ======================================================

    discovery_score: float = 0.0

    discovery_confidence: float = 0.0

    discovery_status: str = ""

    discovery_source: str = ""

    # ======================================================
    # Discovery Intelligence
    # ======================================================

    strengths: List[str] = field(
        default_factory=list
    )

    concerns: List[str] = field(
        default_factory=list
    )

    catalysts: List[str] = field(
        default_factory=list
    )

    risks: List[str] = field(
        default_factory=list
    )

    discovery_notes: List[str] = field(
        default_factory=list
    )

    # ======================================================
    # Research State
    # ======================================================

    research_status: str = "NOT_STARTED"

    research_questions: List[str] = field(
        default_factory=list
    )

    # ======================================================
    # Metadata
    # ======================================================

    metadata: dict = field(
        default_factory=dict
    )


__all__ = [
    "OpportunityResearchIntake",
]