"""
===============================================================================
EIOS
Ownership Section

Purpose:
    Ownership Intelligence section stored inside the Master Dossier.

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
class OwnershipSection(BaseSection):
    """
    Ownership Intelligence stored inside the Master Dossier.
    Inherits common fields from BaseSection.
    """

    # -------------------------------------------------------------------------
    # Component Scores
    # -------------------------------------------------------------------------

    promoter_score: float = 0.0
    fii_score: float = 0.0
    dii_score: float = 0.0
    insider_score: float = 0.0
    concentration_score: float = 0.0
    governance_score: float = 0.0

    # -------------------------------------------------------------------------
    # Ownership Details
    # -------------------------------------------------------------------------

    promoter_holding: float = 0.0
    promoter_pledge: float = 0.0

    fii_holding: float = 0.0
    dii_holding: float = 0.0
    public_holding: float = 0.0

    # -------------------------------------------------------------------------
    # Trend Analysis
    # -------------------------------------------------------------------------

    promoter_trend: str = ""
    fii_trend: str = ""
    dii_trend: str = ""

    # -------------------------------------------------------------------------
    # Ownership Intelligence
    # -------------------------------------------------------------------------

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)