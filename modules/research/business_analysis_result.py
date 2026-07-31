"""
===============================================================================
EIOS
Business Analysis Result

Purpose:
    Stores the final consolidated output of the Business Engine.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BusinessAnalysisResult:
    """
    Final output produced by the Business Engine.
    """

    # ------------------------------------------------------------------
    # Business Model
    # ------------------------------------------------------------------
    business_model: str = ""
    revenue_model: str = ""

    # ------------------------------------------------------------------
    # Market Opportunity
    # ------------------------------------------------------------------
    tam: str = ""
    sam: str = ""
    som: str = ""

    # ------------------------------------------------------------------
    # Competitive Advantage
    # ------------------------------------------------------------------
    moat: str = ""
    pricing_power: str = ""
    customer_stickiness: str = ""
    switching_costs: str = ""

    # ------------------------------------------------------------------
    # Scalability
    # ------------------------------------------------------------------
    scalability: str = ""
    reinvestment_runway: str = ""
    capital_intensity: str = ""

    # ------------------------------------------------------------------
    # SWOT Analysis
    # ------------------------------------------------------------------
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------------------
    executive_summary: Optional[str] = None

    # ------------------------------------------------------------------
    # Scores
    # ------------------------------------------------------------------
    business_quality_score: float = 0.0
    confidence: float = 0.0

    # ------------------------------------------------------------------
    # Supporting Evidence
    # ------------------------------------------------------------------
    evidence: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)