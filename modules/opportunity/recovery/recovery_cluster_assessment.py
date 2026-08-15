"""
EIOS
Everest Investment Operating System

Recovery Cluster / Theme Assessment Model

Purpose:
Defines the passive typed result representing whether multiple
multi-signal recovery assessments belong to a common recovering
sector, industry, theme, macro regime, commodity cycle, or company.

Architecture:

Individual Signals
        ↓
Temporal Signal Intelligence
        ↓
Recovery Detection
        ↓
Multi-Signal Recovery
        ↓
Recovery Cluster / Theme Assessment
        ↓
Catalyst Intelligence
        ↓
Opportunity Engine

Design Principles:
- Passive data model only.
- No calculations.
- No persistence.
- No scoring logic.
- No valuation.
- No opportunity decision.
- No company-specific logic.
- No sector-specific logic.
- Engines perform all analysis.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ==========================================================
# RECOVERY CLUSTER TYPE
# ==========================================================


class RecoveryClusterType(Enum):
    """
    Generic economic or investment context represented by
    a recovery cluster.
    """

    SECTOR = "Sector"

    INDUSTRY = "Industry"

    THEME = "Theme"

    MACRO_REGIME = "Macro Regime"

    COMMODITY_CYCLE = "Commodity Cycle"

    COMPANY = "Company"

    CROSS_SECTOR = "Cross Sector"

    UNKNOWN = "Unknown"


# ==========================================================
# RECOVERY CLUSTER STAGE
# ==========================================================


class RecoveryClusterStage(Enum):
    """
    Maturity of recovery at cluster level.
    """

    INSUFFICIENT_EVIDENCE = (
        "Insufficient Evidence"
    )

    EARLY_CLUSTERING = (
        "Early Clustering"
    )

    STABILIZING_CLUSTER = (
        "Stabilizing Cluster"
    )

    EARLY_RECOVERY_CLUSTER = (
        "Early Recovery Cluster"
    )

    CONFIRMED_RECOVERY_CLUSTER = (
        "Confirmed Recovery Cluster"
    )


# ==========================================================
# RECOVERY CLUSTER DIRECTION
# ==========================================================


class RecoveryClusterDirection(Enum):
    """
    Aggregate direction of a recovery cluster.
    """

    NEGATIVE = "Negative"

    STABILIZING = "Stabilizing"

    POSITIVE = "Positive"

    MIXED = "Mixed"

    UNKNOWN = "Unknown"


# ==========================================================
# RECOVERY CLUSTER ASSESSMENT
# ==========================================================


@dataclass
class RecoveryClusterAssessment:
    """
    Passive institutional assessment of a recovery cluster.

    The cluster engine is responsible for calculating all
    analytical fields.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    cluster_id: str = ""

    cluster_name: str = ""

    cluster_type: RecoveryClusterType = (
        RecoveryClusterType.UNKNOWN
    )

    # ------------------------------------------------------
    # Classification
    # ------------------------------------------------------

    stage: RecoveryClusterStage = (
        RecoveryClusterStage.INSUFFICIENT_EVIDENCE
    )

    direction: RecoveryClusterDirection = (
        RecoveryClusterDirection.UNKNOWN
    )

    # ------------------------------------------------------
    # Breadth
    # ------------------------------------------------------

    total_recovery_assessments: int = 0

    supporting_assessments: int = 0

    stabilizing_assessments: int = 0

    deteriorating_assessments: int = 0

    contradictory_assessments: int = 0

    # ------------------------------------------------------
    # Independent Evidence
    # ------------------------------------------------------

    independent_sources: int = 0

    independent_domains: int = 0

    independent_signals: int = 0

    # ------------------------------------------------------
    # Recovery Characteristics
    # ------------------------------------------------------

    stabilization_breadth: float = 0.0

    inflection_breadth: float = 0.0

    reversal_breadth: float = 0.0

    persistence_breadth: float = 0.0

    # ------------------------------------------------------
    # Cluster Quality
    # ------------------------------------------------------

    coherence_score: float = 0.0

    breadth_score: float = 0.0

    corroboration_score: float = 0.0

    temporal_score: float = 0.0

    contradiction_score: float = 0.0

    confidence: float = 0.0

    # ------------------------------------------------------
    # Cluster Characteristics
    # ------------------------------------------------------

    emerging_cluster: bool = False

    stabilizing_cluster: bool = False

    early_recovery_cluster: bool = False

    confirmed_recovery_cluster: bool = False

    broad_based: bool = False

    cross_domain_confirmation: bool = False

    # ------------------------------------------------------
    # References
    # ------------------------------------------------------

    supporting_signal_ids: List[str] = field(
        default_factory=list
    )

    contradictory_signal_ids: List[str] = field(
        default_factory=list
    )

    source_keys: List[str] = field(
        default_factory=list
    )

    domains: List[str] = field(
        default_factory=list
    )

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
    "RecoveryClusterType",
    "RecoveryClusterStage",
    "RecoveryClusterDirection",
    "RecoveryClusterAssessment",
]