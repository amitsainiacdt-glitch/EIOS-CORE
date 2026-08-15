"""
EIOS
Everest Investment Operating System

Recovery Theme → Catalyst Intelligence Link Model

Purpose
-------
Defines the passive data contract connecting a validated
Recovery Theme with Catalyst Intelligence.

Architecture
------------

Recovery Signal
      ↓
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
THIS MODEL
      ↓
Catalyst Intelligence
      ↓
Opportunity Engine

Design Principles
-----------------
- Passive data model only.
- No calculations.
- No catalyst scoring.
- No catalyst classification.
- No valuation.
- No company selection.
- No portfolio decision.
- No mutation.
- Engines own reasoning.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


# ==========================================================
# CATALYST RELEVANCE
# ==========================================================


class RecoveryCatalystRelevance(Enum):
    """
    Degree to which a catalyst family may be relevant to
    the identified recovery theme.
    """

    UNKNOWN = "Unknown"

    LOW = "Low"

    MODERATE = "Moderate"

    HIGH = "High"

    VERY_HIGH = "Very High"


# ==========================================================
# CATALYST RELATIONSHIP
# ==========================================================


class RecoveryCatalystRelationship(Enum):
    """
    Relationship between recovery theme and catalyst.
    """

    UNKNOWN = "Unknown"

    SUPPORTING = "Supporting"

    ACCELERATING = "Accelerating"

    CONFIRMING = "Confirming"

    ENABLING = "Enabling"

    AMPLIFYING = "Amplifying"

    OFFSETTING = "Offsetting"

    CONTRADICTING = "Contradicting"


# ==========================================================
# TRANSMISSION TYPE
# ==========================================================


class RecoveryCatalystTransmission(Enum):
    """
    Economic transmission mechanism between recovery theme
    and catalyst.
    """

    UNKNOWN = "Unknown"

    DEMAND = "Demand"

    VOLUME = "Volume"

    PRICING = "Pricing"

    MARGIN = "Margin"

    CAPACITY = "Capacity"

    CAPEX = "Capital Expenditure"

    ORDER_FLOW = "Order Flow"

    REGULATORY = "Regulatory"

    TECHNOLOGY = "Technology"

    EXPORT = "Export"

    IMPORT_SUBSTITUTION = "Import Substitution"

    MARKET_RECOGNITION = "Market Recognition"


# ==========================================================
# PASSIVE LINK MODEL
# ==========================================================


@dataclass
class RecoveryThemeCatalystLink:
    """
    Passive relationship object connecting a Recovery Theme
    to Catalyst Intelligence.

    The model stores facts and classifications.

    It does NOT determine:

        - whether a catalyst is real
        - catalyst probability
        - catalyst timing
        - stock impact
        - valuation impact
        - investment attractiveness
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    link_id: str = ""

    theme_id: str = ""

    theme_name: str = ""

    # ------------------------------------------------------
    # Catalyst Identity
    # ------------------------------------------------------

    catalyst_family: str = ""

    catalyst_pattern: str = ""

    catalyst_id: str = ""

    # ------------------------------------------------------
    # Relationship
    # ------------------------------------------------------

    relevance: RecoveryCatalystRelevance = (
        RecoveryCatalystRelevance.UNKNOWN
    )

    relationship: RecoveryCatalystRelationship = (
        RecoveryCatalystRelationship.UNKNOWN
    )

    transmission: RecoveryCatalystTransmission = (
        RecoveryCatalystTransmission.UNKNOWN
    )

    # ------------------------------------------------------
    # Economic Mechanism
    # ------------------------------------------------------

    economic_mechanism: str = ""

    transmission_description: str = ""

    catalyst_rationale: str = ""

    expected_effect: str = ""

    # ------------------------------------------------------
    # Recovery Context
    # ------------------------------------------------------

    recovery_stage: str = ""

    recovery_direction: str = ""

    recovery_breadth: float = 0.0

    confirmed_recovery_breadth: float = 0.0

    recovery_confidence: float = 0.0

    # ------------------------------------------------------
    # Catalyst Context
    # ------------------------------------------------------

    catalyst_strength: float = 0.0

    catalyst_confidence: float = 0.0

    catalyst_timing: str = ""

    catalyst_persistence: str = ""

    catalyst_dependencies: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Supporting Evidence
    # ------------------------------------------------------

    supporting_evidence: List[str] = field(
        default_factory=list
    )

    contradictory_evidence: List[str] = field(
        default_factory=list
    )

    evidence_sources: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Beneficiary / Impact Mapping
    # ------------------------------------------------------

    potential_beneficiaries: List[str] = field(
        default_factory=list
    )

    potential_adversely_affected: List[str] = field(
        default_factory=list
    )

    second_order_effects: List[str] = field(
        default_factory=list
    )

    transmission_channels: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Risk
    # ------------------------------------------------------

    key_risks: List[str] = field(
        default_factory=list
    )

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    contradiction_score: float = 0.0

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
    "RecoveryThemeCatalystLink",
    "RecoveryCatalystRelevance",
    "RecoveryCatalystRelationship",
    "RecoveryCatalystTransmission",
]