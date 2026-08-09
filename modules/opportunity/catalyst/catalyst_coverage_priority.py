"""
EIOS
Everest Investment Operating System

Catalyst Coverage Priority

Purpose:
    Defines the evidence dimensions used to determine
    development priority for Catalyst Families.

Important:
    This module prioritizes PATTERN DEVELOPMENT.
    It does NOT determine investment attractiveness.

Architecture:

    Catalyst Taxonomy
            ↓
    Catalyst Coverage
            ↓
    Coverage Evidence Profile
            ↓
    Coverage Priority
            ↓
    Pattern Development Queue

Design Principles:
    - Passive data models only.
    - No company-specific logic.
    - No investment scoring.
    - No valuation.
    - No company ranking.
    - No automatic investment decision.
    - Priority must remain explainable.
"""

from dataclasses import dataclass
from enum import Enum

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# PRIORITY LEVEL
# ==========================================================


class CoveragePriority(Enum):
    """
    Priority for developing catalyst patterns.

    This is a development priority, not an
    investment attractiveness score.
    """

    CRITICAL = "Critical"

    HIGH = "High"

    MEDIUM = "Medium"

    LOW = "Low"


# ==========================================================
# EVIDENCE PROFILE
# ==========================================================


@dataclass(frozen=True)
class CatalystCoverageEvidence:
    """
    Immutable evidence profile used to assess the
    usefulness of developing a catalyst pattern.

    Each dimension is deliberately independent.

    Scale:
        0 = very low
        1 = low
        2 = moderate
        3 = high
        4 = very high
        5 = exceptional
    """

    earnings_impact: int = 0

    detection_lead_time: int = 0

    cross_sector_applicability: int = 0

    observability: int = 0

    persistence: int = 0

    evidence_availability: int = 0

    second_order_potential: int = 0

    market_mispricing_potential: int = 0


# ==========================================================
# PRIORITY RECORD
# ==========================================================


@dataclass(frozen=True)
class CatalystCoveragePriority:
    """
    Immutable priority record for one Catalyst Family.
    """

    family: CatalystFamily

    priority: CoveragePriority

    rationale: str

    evidence: CatalystCoverageEvidence = (
        CatalystCoverageEvidence()
    )


__all__ = [
    "CoveragePriority",
    "CatalystCoverageEvidence",
    "CatalystCoveragePriority",
]