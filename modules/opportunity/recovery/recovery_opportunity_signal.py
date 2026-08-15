"""
EIOS
Everest Investment Operating System

Recovery Opportunity Signal Model

Purpose
-------
Passive contract between Recovery Intelligence and the
Opportunity Engine.

The model represents whether completed Recovery Intelligence
provides sufficient evidence to warrant downstream
Opportunity Engine attention.

Architecture
------------

Recovery Detection
        ↓
Multi-Signal Recovery
        ↓
Recovery Cluster
        ↓
Recovery Breadth
        ↓
Recovery Theme
        ↓
Recovery Theme → Catalyst
        ↓
THIS MODEL
        ↓
Opportunity Engine

Important
---------
This is NOT an investment decision.

It does not calculate:
- valuation
- intrinsic value
- mispricing
- position size
- portfolio weight
- expected return
- investment recommendation

Engines own calculations and reasoning.
This class is a passive data model.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


# ==========================================================
# SIGNAL STAGE
# ==========================================================


class RecoveryOpportunityStage(Enum):
    UNKNOWN = "Unknown"

    WATCH = "Watch"

    DEVELOPING = "Developing"

    ACTIONABLE = "Actionable"


# ==========================================================
# SIGNAL DIRECTION
# ==========================================================


class RecoveryOpportunityDirection(Enum):
    UNKNOWN = "Unknown"

    NEGATIVE = "Negative"

    NEUTRAL = "Neutral"

    POSITIVE = "Positive"


# ==========================================================
# SIGNAL CONFIDENCE
# ==========================================================


class RecoveryOpportunityConfidence(Enum):
    UNKNOWN = "Unknown"

    LOW = "Low"

    MODERATE = "Moderate"

    HIGH = "High"

    VERY_HIGH = "Very High"


# ==========================================================
# SIGNAL TYPE
# ==========================================================


class RecoveryOpportunitySignalType(Enum):
    UNKNOWN = "Unknown"

    RECOVERY = "Recovery"

    RECOVERY_CATALYST = "Recovery Catalyst"

    BROAD_RECOVERY = "Broad Recovery"


# ==========================================================
# PASSIVE MODEL
# ==========================================================


@dataclass
class RecoveryOpportunitySignal:
    """
    Passive downstream signal generated from Recovery
    Intelligence.

    This object does not decide whether an investment should
    be made.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    signal_id: str = ""

    theme_id: str = ""

    theme_name: str = ""

    signal_type: RecoveryOpportunitySignalType = (
        RecoveryOpportunitySignalType.UNKNOWN
    )

    # ------------------------------------------------------
    # Signal Classification
    # ------------------------------------------------------

    stage: RecoveryOpportunityStage = (
        RecoveryOpportunityStage.UNKNOWN
    )

    direction: RecoveryOpportunityDirection = (
        RecoveryOpportunityDirection.UNKNOWN
    )

    confidence_level: RecoveryOpportunityConfidence = (
        RecoveryOpportunityConfidence.UNKNOWN
    )

    # ------------------------------------------------------
    # Recovery Evidence
    # ------------------------------------------------------

    recovery_breadth: float = 0.0

    confirmed_recovery_breadth: float = 0.0

    recovery_confidence: float = 0.0

    recovery_coherence: float = 0.0

    temporal_support: float = 0.0

    persistence_score: float = 0.0

    contradiction_score: float = 0.0

    # ------------------------------------------------------
    # Catalyst Evidence
    # ------------------------------------------------------

    catalyst_count: int = 0

    supporting_catalyst_count: int = 0

    confirming_catalyst_count: int = 0

    accelerating_catalyst_count: int = 0

    catalyst_confidence: float = 0.0

    catalyst_strength: float = 0.0

    catalyst_coherence: float = 0.0

    # ------------------------------------------------------
    # Opportunity Readiness
    # ------------------------------------------------------

    opportunity_ready: bool = False

    requires_more_evidence: bool = True

    catalyst_supported: bool = False

    broad_recovery_supported: bool = False

    confirmed_recovery_supported: bool = False

    # ------------------------------------------------------
    # Evidence References
    # ------------------------------------------------------

    supporting_evidence: List[str] = field(
        default_factory=list
    )

    contradictory_evidence: List[str] = field(
        default_factory=list
    )

    catalyst_families: List[str] = field(
        default_factory=list
    )

    catalyst_patterns: List[str] = field(
        default_factory=list
    )

    evidence_sources: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Reasoning
    # ------------------------------------------------------

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


__all__ = [
    "RecoveryOpportunitySignal",
    "RecoveryOpportunityStage",
    "RecoveryOpportunityDirection",
    "RecoveryOpportunityConfidence",
    "RecoveryOpportunitySignalType",
]