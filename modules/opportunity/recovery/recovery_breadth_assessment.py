"""
EIOS
Everest Investment Operating System

Recovery Breadth Assessment Model

Purpose:
Defines the passive intelligence object used to represent
the breadth and diffusion of recovery across an explicitly
defined sector, theme, industry, macro cluster, or other
economic recovery universe.

Architecture:

Recovery Signals
        ↓
Recovery Detection
        ↓
Recovery Cluster
        ↓
Recovery Breadth Assessment
        ↓
Recovery Breadth Engine
        ↓
Sector / Theme Recovery Intelligence

Design Principles:
- Passive data model only.
- No calculations.
- No scoring logic.
- No persistence.
- No valuation.
- No opportunity decision.
- No company-specific investment logic.
- Engines perform all analysis.
- Missing information is represented explicitly.
- Breadth is distinct from recovery strength.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ==========================================================
# BREADTH TYPE
# ==========================================================


class RecoveryBreadthType(Enum):
    """
    Type of economic universe across which recovery breadth
    is being assessed.
    """

    SECTOR = "Sector"

    INDUSTRY = "Industry"

    THEME = "Theme"

    MACRO = "Macro"

    CAPITAL_CYCLE = "Capital Cycle"

    COMMODITY = "Commodity"

    SUPPLY_CHAIN = "Supply Chain"

    COMPANY_GROUP = "Company Group"

    UNKNOWN = "Unknown"


# ==========================================================
# BREADTH STAGE
# ==========================================================


class RecoveryBreadthStage(Enum):
    """
    Maturity of recovery breadth.
    """

    INSUFFICIENT = "Insufficient Breadth"

    ISOLATED = "Isolated Improvement"

    EARLY_BREADTH = "Early Breadth Expansion"

    BROADENING = "Broadening Recovery"

    BROAD_RECOVERY = "Broad Recovery"

    SATURATED = "Broad Recovery / Saturated"

    CONTRACTING = "Contracting Breadth"


# ==========================================================
# BREADTH DIRECTION
# ==========================================================


class RecoveryBreadthDirection(Enum):
    """
    Direction in which recovery breadth is evolving.
    """

    EXPANDING = "Expanding"

    STABLE = "Stable"

    CONTRACTING = "Contracting"

    MIXED = "Mixed"

    UNKNOWN = "Unknown"


# ==========================================================
# LEADERSHIP STATE
# ==========================================================


class RecoveryLeadershipState(Enum):
    """
    Whether recovery is being led by a meaningful subset
    of the assessed universe.
    """

    NO_LEADERSHIP = "No Leadership"

    EARLY_LEADERS = "Early Leaders"

    CLEAR_LEADERS = "Clear Leaders"

    BROAD_LEADERSHIP = "Broad Leadership"

    ROTATING_LEADERSHIP = "Rotating Leadership"

    UNKNOWN = "Unknown"


# ==========================================================
# CANONICAL RECOVERY BREADTH ASSESSMENT
# ==========================================================


@dataclass
class RecoveryBreadthAssessment:
    """
    Passive institutional assessment of recovery breadth.

    Engines are responsible for calculating:

        - breadth
        - breadth direction
        - stage
        - leadership
        - confidence
        - contradictions
        - temporal evolution
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    breadth_id: str = ""

    breadth_name: str = ""

    breadth_type: RecoveryBreadthType = (
        RecoveryBreadthType.UNKNOWN
    )

    # ------------------------------------------------------
    # Assessment State
    # ------------------------------------------------------

    stage: RecoveryBreadthStage = (
        RecoveryBreadthStage.INSUFFICIENT
    )

    direction: RecoveryBreadthDirection = (
        RecoveryBreadthDirection.UNKNOWN
    )

    leadership_state: RecoveryLeadershipState = (
        RecoveryLeadershipState.UNKNOWN
    )

    # ------------------------------------------------------
    # Population
    # ------------------------------------------------------

    total_entities: int = 0

    assessed_entities: int = 0

    improving_entities: int = 0

    stabilizing_entities: int = 0

    deteriorating_entities: int = 0

    unchanged_entities: int = 0

    insufficient_entities: int = 0

    # ------------------------------------------------------
    # Recovery Stages
    # ------------------------------------------------------

    early_inflection_entities: int = 0

    early_recovery_entities: int = 0

    confirmed_recovery_entities: int = 0

    # ------------------------------------------------------
    # Breadth Measurements
    # ------------------------------------------------------

    improvement_breadth: float = 0.0

    stabilization_breadth: float = 0.0

    recovery_breadth: float = 0.0

    confirmed_recovery_breadth: float = 0.0

    deterioration_breadth: float = 0.0

    contradiction_breadth: float = 0.0

    # ------------------------------------------------------
    # Breadth Evolution
    # ------------------------------------------------------

    previous_breadth: float = 0.0

    current_breadth: float = 0.0

    breadth_change: float = 0.0

    breadth_acceleration: float = 0.0

    # ------------------------------------------------------
    # Leadership
    # ------------------------------------------------------

    leader_count: int = 0

    leader_breadth: float = 0.0

    leading_entities: List[str] = field(
        default_factory=list
    )

    lagging_entities: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Evidence
    # ------------------------------------------------------

    independent_sources: int = 0

    independent_signals: int = 0

    independent_domains: int = 0

    temporal_support: float = 0.0

    corroboration_score: float = 0.0

    contradiction_score: float = 0.0

    # ------------------------------------------------------
    # Intelligence State
    # ------------------------------------------------------

    breadth_expanding: bool = False

    breadth_stable: bool = False

    breadth_contracting: bool = False

    broad_based: bool = False

    early_breadth_signal: bool = False

    recovery_breadth_signal: bool = False

    confirmed_breadth_signal: bool = False

    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------
    # Explanation
    # ------------------------------------------------------

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


__all__ = [
    "RecoveryBreadthType",
    "RecoveryBreadthStage",
    "RecoveryBreadthDirection",
    "RecoveryLeadershipState",
    "RecoveryBreadthAssessment",
]