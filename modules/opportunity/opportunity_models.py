"""
===============================================================================
EIOS
Everest Investment Operating System

Opportunity Models

Shared models used throughout the Opportunity Office.

Release:
    4.0
===============================================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict


class OpportunityStatus(Enum):
    """
    Opportunity lifecycle.
    """

    DISCOVERED = "Discovered"
    UNDER_RESEARCH = "Under Research"
    WATCHLIST = "Watchlist"
    COMMITTEE_REVIEW = "Committee Review"
    APPROVED = "Approved"
    ACTIVE = "Active"
    TARGET_HIT = "Target Hit"
    STOP_LOSS = "Stop Loss"
    EXITED = "Exited"
    ARCHIVED = "Archived"


class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class OpportunityScore:

    catalyst: float = 0.0
    earnings: float = 0.0
    sector: float = 0.0
    valuation: float = 0.0
    institutional: float = 0.0
    expansion: float = 0.0
    risk: float = 0.0

    total: float = 0.0
    confidence: float = 0.0


@dataclass
class OpportunityIdea:

    company: str = ""

    sector: str = ""

    cmp: float = 0.0

    entry_price: float = 0.0

    target_price: float = 0.0

    stop_loss: float = 0.0

    expected_return: float = 0.0

    expected_months: int = 0

    confidence: float = 0.0

    risk: RiskLevel = RiskLevel.MEDIUM

    status: OpportunityStatus = (
        OpportunityStatus.DISCOVERED
    )

    catalyst: str = ""

    supporting_catalysts: List[str] = field(
        default_factory=list
    )

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )