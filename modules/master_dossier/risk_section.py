"""
===============================================================================
EIOS
Risk Section

Purpose:
    Stores Risk Intelligence inside the Master Dossier.

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
class RiskSection(BaseSection):
    """
    Risk Intelligence stored in the Master Dossier.
    """

    # -------------------------------------------------------------------------
    # Overall Risk
    # -------------------------------------------------------------------------

    overall_risk_score: float = 0.0
    risk_rating: str = ""

    # -------------------------------------------------------------------------
    # Business Risks
    # -------------------------------------------------------------------------

    business_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Financial Risks
    # -------------------------------------------------------------------------

    financial_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Management Risks
    # -------------------------------------------------------------------------

    management_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Industry Risks
    # -------------------------------------------------------------------------

    industry_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Regulatory Risks
    # -------------------------------------------------------------------------

    regulatory_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # ESG Risks
    # -------------------------------------------------------------------------

    esg_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Market Risks
    # -------------------------------------------------------------------------

    market_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Red Flags
    # -------------------------------------------------------------------------

    red_flags: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Thesis Kill Switch
    # -------------------------------------------------------------------------

    thesis_breakers: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Monitoring
    # -------------------------------------------------------------------------

    watch_items: List[str] = field(default_factory=list)