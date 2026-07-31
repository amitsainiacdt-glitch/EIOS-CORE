"""
===============================================================================
EIOS
Investment Committee Section

Purpose:
    Stores the final Investment Committee assessment and decision.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List

from .base_section import BaseSection


@dataclass
class CommitteeSection(BaseSection):
    """
    Investment Committee assessment stored in the Master Dossier.
    """

    # -------------------------------------------------------------------------
    # Overall Decision
    # -------------------------------------------------------------------------

    recommendation: str = ""
    conviction: str = ""

    overall_score: float = 0.0

    # -------------------------------------------------------------------------
    # Individual Committee Scores
    # -------------------------------------------------------------------------

    business_score: float = 0.0
    financial_score: float = 0.0
    management_score: float = 0.0
    ownership_score: float = 0.0
    competitive_score: float = 0.0
    risk_score: float = 0.0
    valuation_score: float = 0.0
    macro_score: float = 0.0

    # -------------------------------------------------------------------------
    # Decision Framework
    # -------------------------------------------------------------------------

    investment_case: str = ""
    key_strengths: List[str] = field(default_factory=list)
    key_concerns: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Portfolio Decision
    # -------------------------------------------------------------------------

    action: str = ""
    position_size: float = 0.0

    # -------------------------------------------------------------------------
    # Monitoring
    # -------------------------------------------------------------------------

    review_frequency: str = ""
    monitoring_points: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Decision Log
    # -------------------------------------------------------------------------

    committee_notes: List[str] = field(default_factory=list)