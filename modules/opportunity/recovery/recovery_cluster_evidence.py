"""
EIOS
Everest Investment Operating System

Recovery Cluster Evidence Model

Purpose:
Defines the passive relationship between recovery evidence
and the economic cluster, theme, sector, industry, macro regime,
commodity cycle, or company to which that evidence belongs.

Architecture:

Recovery Evidence
        ↓
Recovery Cluster Evidence
        ↓
Recovery Cluster Engine
        ↓
Recovery Cluster Assessment

Design Principles:
- Passive data model only.
- No calculations.
- No scoring.
- No persistence.
- No valuation.
- No opportunity decision.
- Cluster membership must be explicit.
- Engines perform all analysis.
"""

from dataclasses import dataclass

from modules.opportunity.recovery.recovery_evidence import (
    RecoveryEvidence,
)

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterType,
)


@dataclass
class RecoveryClusterEvidence:
    """
    Passive evidence record connecting recovery evidence
    to an explicit economic recovery cluster.
    """

    # ------------------------------------------------------
    # Cluster Identity
    # ------------------------------------------------------

    cluster_key: str = ""

    cluster_name: str = ""

    cluster_type: RecoveryClusterType = (
        RecoveryClusterType.UNKNOWN
    )

    # ------------------------------------------------------
    # Recovery Evidence
    # ------------------------------------------------------

    recovery_evidence: RecoveryEvidence = None


__all__ = [
    "RecoveryClusterEvidence",
]