"""
===============================================================================
EIOS
Everest Investment Operating System

Committee Section

Purpose:
    Stores the final Investment Committee assessment.

Architecture:
    Passive data model.
    No calculations are performed inside this class.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List

from .base_section import BaseSection


@dataclass
class CommitteeSection(BaseSection):
    """
    Typed Investment Committee section.

    This section stores the final committee decision together with
    the votes, scores, confidence and portfolio recommendation.
    """

    # =========================================================================
    # Overall Decision
    # =========================================================================

    recommendation: str = ""
    conviction: str = ""
    overall_score: float = 0.0
    confidence: float = 0.0
    summary: str = ""

    # =========================================================================
    # Individual Committee Scores
    # =========================================================================

    business_score: float = 0.0
    financial_score: float = 0.0
    management_score: float = 0.0
    ownership_score: float = 0.0
    competitive_score: float = 0.0
    risk_score: float = 0.0
    valuation_score: float = 0.0
    macro_score: float = 0.0

    # =========================================================================
    # Individual Member Votes
    # =========================================================================

    business_vote: str = ""
    financial_vote: str = ""
    management_vote: str = ""
    ownership_vote: str = ""
    competitive_vote: str = ""
    risk_vote: str = ""
    valuation_vote: str = ""
    macro_vote: str = ""

    # =========================================================================
    # Committee Statistics
    # =========================================================================

    total_members: int = 0
    pass_votes: int = 0
    watch_votes: int = 0
    reject_votes: int = 0

    # =========================================================================
    # Investment Case
    # =========================================================================

    investment_case: str = ""

    key_strengths: List[str] = field(
        default_factory=list
    )

    key_concerns: List[str] = field(
        default_factory=list
    )

    # =========================================================================
    # Portfolio Recommendation
    # =========================================================================

    action: str = ""
    position_size: float = 0.0

    # =========================================================================
    # Monitoring
    # =========================================================================

    review_frequency: str = ""

    monitoring_points: List[str] = field(
        default_factory=list
    )

    # =========================================================================
    # Committee Notes
    # =========================================================================

    committee_notes: List[str] = field(
        default_factory=list
    )