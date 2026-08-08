"""
EIOS
Everest Investment Operating System

Opportunity Ranking Models

Passive data models only.
No calculations belong here.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class OpportunityRanking:
    """
    Competitive ranking result for one opportunity.
    """

    company: str = ""

    rank: int = 0

    # ------------------------------------------------------
    # Source Scores
    # ------------------------------------------------------

    opportunity_score: float = 0.0

    confidence_score: float = 0.0

    evidence_score: float = 0.0

    evidence_confidence: float = 0.0

    asymmetry_score: float = 0.0

    # ------------------------------------------------------
    # Derived Selection Metrics
    # ------------------------------------------------------

    risk_adjusted_score: float = 0.0

    research_efficiency_score: float = 0.0

    research_priority_score: float = 0.0

    # ------------------------------------------------------
    # Classification
    # ------------------------------------------------------

    tier: str = ""

    priority: str = ""

    eligible: bool = False

    # ------------------------------------------------------
    # Gate Information
    # ------------------------------------------------------

    evidence_gate_passed: bool = False

    permanent_loss_gate_passed: bool = False

    confidence_gate_passed: bool = False

    kill_switch_gate_passed: bool = False

    # ------------------------------------------------------
    # Reasoning
    # ------------------------------------------------------

    exclusion_reasons: List[str] = field(
        default_factory=list
    )

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


@dataclass
class OpportunityRankingSet:
    """
    Competitive ranking of multiple opportunities.
    """

    rankings: List[OpportunityRanking] = field(
        default_factory=list
    )

    eligible_count: int = 0

    excluded_count: int = 0

    top_company: str = ""

    top_priority_score: float = 0.0

    warnings: List[str] = field(
        default_factory=list
    )


__all__ = [
    "OpportunityRanking",
    "OpportunityRankingSet",
]