"""
EIOS
Everest Investment Operating System

Recovery Assessment Model

Purpose:
Defines the typed result produced by the Recovery Engine.

Architecture:

Temporal Signal Evolution
        ↓
Recovery Engine
        ↓
Recovery Assessment

Design Principles:
- Passive data model only.
- No calculations.
- No persistence.
- No internet access.
- No valuation.
- No opportunity scoring.
- No investment decision.
- Recovery interpretation is performed by engines.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ==========================================================
# RECOVERY STAGE
# ==========================================================


class RecoveryStage(Enum):
    """
    Generic stage of economic/business recovery.
    """

    DETERIORATING = "Deteriorating"

    SLOWING_DETERIORATION = (
        "Slowing Deterioration"
    )

    STABILIZING = "Stabilizing"

    EARLY_INFLECTION = (
        "Early Inflection"
    )

    EARLY_RECOVERY = (
        "Early Recovery"
    )

    CONFIRMED_RECOVERY = (
        "Confirmed Recovery"
    )


# ==========================================================
# RECOVERY DIRECTION
# ==========================================================


class RecoveryDirection(Enum):
    """
    Direction of the recovery process.
    """

    NEGATIVE = "Negative"

    STABILIZING = "Stabilizing"

    POSITIVE = "Positive"

    UNKNOWN = "Unknown"


# ==========================================================
# RECOVERY ASSESSMENT
# ==========================================================


@dataclass
class RecoveryAssessment:
    """
    Passive institutional recovery assessment.

    The Recovery Engine is responsible for determining
    these values.

    This object stores the resulting assessment only.
    """

    # ------------------------------------------------------
    # Classification
    # ------------------------------------------------------

    stage: RecoveryStage = (
        RecoveryStage.DETERIORATING
    )

    direction: RecoveryDirection = (
        RecoveryDirection.UNKNOWN
    )

    # ------------------------------------------------------
    # Evidence Structure
    # ------------------------------------------------------

    temporal_support: float = 0.0

    signal_breadth: float = 0.0

    corroboration: float = 0.0

    persistence: float = 0.0

    contradiction: float = 0.0

    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------
    # Recovery Characteristics
    # ------------------------------------------------------

    bottoming_detected: bool = False

    stabilization_detected: bool = False

    inflection_detected: bool = False

    reversal_detected: bool = False

    persistence_detected: bool = False

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
    "RecoveryStage",
    "RecoveryDirection",
    "RecoveryAssessment",
]