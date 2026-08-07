"""
===============================================================================
EIOS
Everest Investment Operating System

Opportunity Section

Passive data model representing one investment opportunity.

Rules:
    - No calculations.
    - No business logic.
    - Engines populate this object.
    - UI displays this object.
===============================================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List

from modules.opportunity.opportunity_models import (
    OpportunityStatus,
    RiskLevel,
)


@dataclass
class OpportunitySection:
    """
    Typed Opportunity domain model.
    """

    # ==========================================================
    # Basic Information
    # ==========================================================

    company: str = ""
    sector: str = ""

    # ==========================================================
    # Pricing
    # ==========================================================

    cmp: float = 0.0
    entry_price: float = 0.0
    target_price: float = 0.0
    stop_loss: float = 0.0

    # ==========================================================
    # Return Expectations
    # ==========================================================

    expected_return: float = 0.0
    expected_months: int = 0

    # ==========================================================
    # Institutional Assessment
    # ==========================================================

    score: float = 0.0
    confidence: float = 0.0

    risk_level: RiskLevel = RiskLevel.MEDIUM
    status: OpportunityStatus = (
        OpportunityStatus.DISCOVERED
    )

    # ==========================================================
    # Thesis
    # ==========================================================

    primary_catalyst: str = ""

    supporting_catalysts: List[str] = field(
        default_factory=list
    )

    summary: str = ""

    # ==========================================================
    # Evidence
    # ==========================================================

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    # ==========================================================
    # Review
    # ==========================================================

    review_date: str = ""

    exit_conditions: List[str] = field(
        default_factory=list
    )

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict = field(
        default_factory=dict
    )