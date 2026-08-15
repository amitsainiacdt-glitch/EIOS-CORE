"""
EIOS
Everest Investment Operating System

Multi-Signal Recovery Assessment Model

Purpose:
Defines the passive typed result used to represent whether
multiple independent signals corroborate a recovery.

Architecture:

Individual Temporal Signals
            ↓
Recovery Detection
            ↓
Multi-Signal Recovery Aggregation
            ↓
Multi-Signal Recovery Assessment

Design Principles:
- Passive data model only.
- No calculations.
- No persistence.
- No valuation.
- No opportunity scoring.
- No investment decision.
- No sector-specific logic.
- No company-specific logic.
- Engines perform all calculations.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ==========================================================
# MULTI-SIGNAL RECOVERY STAGE
# ==========================================================


class MultiSignalRecoveryStage(Enum):
    """
    Generic stage of a recovery based on multiple signals.
    """

    INSUFFICIENT_EVIDENCE = (
        "Insufficient Evidence"
    )

    ISOLATED_IMPROVEMENT = (
        "Isolated Improvement"
    )

    BROAD_STABILIZATION = (
        "Broad Stabilization"
    )

    EARLY_BROAD_RECOVERY = (
        "Early Broad Recovery"
    )

    CONFIRMED_BROAD_RECOVERY = (
        "Confirmed Broad Recovery"
    )


# ==========================================================
# MULTI-SIGNAL RECOVERY DIRECTION
# ==========================================================


class MultiSignalRecoveryDirection(Enum):
    """
    Aggregate direction of multiple recovery signals.
    """

    NEGATIVE = "Negative"

    STABILIZING = "Stabilizing"

    POSITIVE = "Positive"

    MIXED = "Mixed"

    UNKNOWN = "Unknown"


# ==========================================================
# MULTI-SIGNAL RECOVERY ASSESSMENT
# ==========================================================


@dataclass
class MultiSignalRecoveryAssessment:
    """
    Passive institutional assessment of multi-signal recovery.

    The aggregation engine is responsible for calculating
    these fields.
    """

    # ------------------------------------------------------
    # Classification
    # ------------------------------------------------------

    stage: MultiSignalRecoveryStage = (
        MultiSignalRecoveryStage.INSUFFICIENT_EVIDENCE
    )

    direction: MultiSignalRecoveryDirection = (
        MultiSignalRecoveryDirection.UNKNOWN
    )

    # ------------------------------------------------------
    # Breadth
    # ------------------------------------------------------

    total_signals: int = 0

    improving_signals: int = 0

    stabilizing_signals: int = 0

    deteriorating_signals: int = 0

    neutral_signals: int = 0

    # ------------------------------------------------------
    # Evidence Quality
    # ------------------------------------------------------

    breadth_score: float = 0.0

    corroboration_score: float = 0.0

    temporal_score: float = 0.0

    consistency_score: float = 0.0

    contradiction_score: float = 0.0

    # ------------------------------------------------------
    # Recovery Characteristics
    # ------------------------------------------------------

    isolated_improvement: bool = False

    broad_stabilization: bool = False

    broad_inflection: bool = False

    broad_reversal: bool = False

    persistent_recovery: bool = False

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

    # ------------------------------------------------------
    # Signal / Evidence References
    # ------------------------------------------------------

    supporting_signal_ids: List[str] = field(
        default_factory=list
    )

    contradictory_signal_ids: List[str] = field(
        default_factory=list
    )


__all__ = [
    "MultiSignalRecoveryStage",
    "MultiSignalRecoveryDirection",
    "MultiSignalRecoveryAssessment",
]