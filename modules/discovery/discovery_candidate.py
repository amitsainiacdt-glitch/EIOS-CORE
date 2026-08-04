"""
===============================================================================
EIOS
Everest Investment Operating System

Discovery Candidate

Purpose:
    Represents a company under evaluation by the Discovery Office before
    a full Master Dossier is created.

Architecture:
    - Passive typed data model.
    - Contains no business logic.
    - Discovery filters populate this object.
    - Approved candidates are promoted to Master Dossier.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class DiscoveryCandidate:
    """
    Represents a company being evaluated by the Discovery Office.
    """

    # =========================================================================
    # Company Identity
    # =========================================================================

    company_name: str
    ticker: str
    sector: str
    industry: str

    # =========================================================================
    # Discovery Scores
    # =========================================================================

    quality_score: float = 0.0
    growth_score: float = 0.0
    financial_score: float = 0.0
    management_score: float = 0.0
    capital_allocation_score: float = 0.0
    moat_score: float = 0.0
    risk_score: float = 0.0
    tailwind_score: float = 0.0
    valuation_score: float = 0.0

    overall_score: float = 0.0

    # =========================================================================
    # Discovery Status
    # =========================================================================

    status: str = "Pending"

    # =========================================================================
    # Discovery Intelligence
    # =========================================================================

    strengths: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    catalysts: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)

    # =========================================================================
    # Metadata
    # =========================================================================

    discovery_notes: List[str] = field(default_factory=list)

    confidence: float = 0.0

    source: str = ""