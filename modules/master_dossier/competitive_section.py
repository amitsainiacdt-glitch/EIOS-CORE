"""
===============================================================================
EIOS
Competitive Section

Purpose:
    Stores Competitive Intelligence inside the Master Dossier.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .base_section import BaseSection


@dataclass
class CompetitiveSection(BaseSection):
    """
    Competitive Intelligence stored in the Master Dossier.
    """

    # -------------------------------------------------------------------------
    # Industry
    # -------------------------------------------------------------------------

    industry: str = ""
    market_size: str = ""
    market_growth: str = ""

    # -------------------------------------------------------------------------
    # Market Position
    # -------------------------------------------------------------------------

    market_share: float = 0.0
    industry_rank: int = 0
    competitive_position: str = ""

    # -------------------------------------------------------------------------
    # Competitive Advantages
    # -------------------------------------------------------------------------

    economic_moat: str = ""
    cost_advantage: str = ""
    technology_advantage: str = ""
    distribution_strength: str = ""
    brand_strength: str = ""
    customer_relationships: str = ""

    # -------------------------------------------------------------------------
    # Competition
    # -------------------------------------------------------------------------

    major_competitors: List[str] = field(default_factory=list)
    peer_comparison: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Market Dynamics
    # -------------------------------------------------------------------------

    barriers_to_entry: str = ""
    threat_of_substitutes: str = ""
    supplier_power: str = ""
    customer_power: str = ""

    # -------------------------------------------------------------------------
    # Competitive Intelligence
    # -------------------------------------------------------------------------

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)