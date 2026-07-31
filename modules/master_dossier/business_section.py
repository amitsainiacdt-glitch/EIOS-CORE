"""
===============================================================================
EIOS
Business Section

Purpose:
    Stores Business Quality Intelligence inside the Master Dossier.

Architecture:
    - Passive domain data model.
    - Contains no business calculations.
    - Populated by Business domain engines.
    - Persisted exclusively through MasterDossier.

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
class BusinessSection(BaseSection):
    """
    Typed Business Quality section stored in the Master Dossier.

    This class is a passive data model. Business analysis, scoring,
    confidence calculation, and interpretation belong to engines.
    """

    # =========================================================================
    # Business Profile
    # =========================================================================

    business_model: str = ""
    industry: str = ""
    sector: str = ""

    # =========================================================================
    # Quality Scores
    # =========================================================================

    business_quality_score: float = 0.0
    moat_score: float = 0.0
    scalability_score: float = 0.0
    predictability_score: float = 0.0
    capital_intensity_score: float = 0.0

    # =========================================================================
    # Competitive Position
    # =========================================================================

    moat: str = ""
    market_position: str = ""
    pricing_power: str = ""
    customer_stickiness: str = ""
    switching_cost: str = ""

    # =========================================================================
    # Market Opportunity and Growth
    # =========================================================================

    addressable_market: str = ""
    growth_runway: str = ""
    reinvestment_runway: str = ""

    growth_drivers: List[str] = field(default_factory=list)

    # =========================================================================
    # Strategic Assessment
    # =========================================================================

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)

    # =========================================================================
    # Key Risks
    # =========================================================================

    key_risks: List[str] = field(default_factory=list)