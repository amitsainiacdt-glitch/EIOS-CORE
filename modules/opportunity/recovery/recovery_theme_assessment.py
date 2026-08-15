"""
EIOS
Everest Investment Operating System

Recovery Theme Assessment Model

Purpose:
Defines the passive intelligence object used to represent
an economically coherent recovery theme emerging from one
or more Recovery Cluster assessments.

Architecture:

Recovery Cluster
        ↓
Recovery Breadth
        ↓
Recovery Theme Assessment
        ↓
Recovery Theme Engine
        ↓
Catalyst / Opportunity Intelligence

Design Principles:
- Passive data model only.
- No calculations.
- No scoring logic.
- No persistence.
- No company-specific investment logic.
- No valuation.
- No opportunity recommendation.
- Engines own all reasoning.
- Economic mechanism is explicit.
- Theme evidence is explicit.
- Contradiction is explicit.
- Confidence is explicit.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


# ==========================================================
# THEME TYPE
# ==========================================================


class RecoveryThemeType(Enum):
    """
    Economic category represented by the recovery theme.
    """

    DEMAND_RECOVERY = "Demand Recovery"

    SUPPLY_RECOVERY = "Supply Recovery"

    CAPACITY_CYCLE = "Capacity Cycle"

    CAPEX_CYCLE = "Capital Expenditure Cycle"

    INVENTORY_CYCLE = "Inventory Cycle"

    PRICING_RECOVERY = "Pricing Recovery"

    VOLUME_RECOVERY = "Volume Recovery"

    EXPORT_RECOVERY = "Export Recovery"

    IMPORT_SUBSTITUTION = "Import Substitution"

    CREDIT_RECOVERY = "Credit Recovery"

    LIQUIDITY_RECOVERY = "Liquidity Recovery"

    POLICY_DRIVEN = "Policy Driven"

    COMMODITY_CYCLE = "Commodity Cycle"

    TECHNOLOGY_ADOPTION = "Technology Adoption"

    INDUSTRIAL_RECOVERY = "Industrial Recovery"

    CONSUMPTION_RECOVERY = "Consumption Recovery"

    HOUSING_RECOVERY = "Housing Recovery"

    INFRASTRUCTURE_RECOVERY = "Infrastructure Recovery"

    UNKNOWN = "Unknown"


# ==========================================================
# THEME STAGE
# ==========================================================


class RecoveryThemeStage(Enum):
    """
    Maturity of the economic recovery theme.
    """

    UNKNOWN = "Unknown"

    EMERGING = "Emerging Theme"

    DEVELOPING = "Developing Theme"

    BROAD = "Broad Recovery Theme"

    VALIDATED = "Validated Theme"

    STRUCTURAL = "Structural Recovery Theme"

    REVERSING = "Reversing Theme"


# ==========================================================
# THEME DIRECTION
# ==========================================================


class RecoveryThemeDirection(Enum):
    """
    Direction of the underlying economic theme.
    """

    POSITIVE = "Positive"

    STABLE = "Stable"

    MIXED = "Mixed"

    NEGATIVE = "Negative"

    UNKNOWN = "Unknown"


# ==========================================================
# THEME CONFIDENCE
# ==========================================================


class RecoveryThemeConfidence(Enum):
    """
    Qualitative confidence classification.
    """

    LOW = "Low"

    MODERATE = "Moderate"

    HIGH = "High"

    VERY_HIGH = "Very High"

    UNKNOWN = "Unknown"


# ==========================================================
# CANONICAL RECOVERY THEME ASSESSMENT
# ==========================================================


@dataclass
class RecoveryThemeAssessment:
    """
    Passive representation of an economically coherent
    recovery theme.

    The engine is responsible for:

        - identifying the theme
        - aggregating clusters
        - evaluating economic coherence
        - assessing corroboration
        - determining stage
        - determining confidence
        - generating reasoning
        - identifying contradictions

    This model performs none of those calculations.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    theme_id: str = ""

    theme_name: str = ""

    theme_type: RecoveryThemeType = (
        RecoveryThemeType.UNKNOWN
    )

    stage: RecoveryThemeStage = (
        RecoveryThemeStage.UNKNOWN
    )

    direction: RecoveryThemeDirection = (
        RecoveryThemeDirection.UNKNOWN
    )

    confidence_level: RecoveryThemeConfidence = (
        RecoveryThemeConfidence.UNKNOWN
    )

    # ------------------------------------------------------
    # Economic Definition
    # ------------------------------------------------------

    economic_mechanism: str = ""

    demand_driver: str = ""

    supply_driver: str = ""

    policy_driver: str = ""

    capital_cycle_driver: str = ""

    commodity_driver: str = ""

    technology_driver: str = ""

    geographic_driver: str = ""

    # ------------------------------------------------------
    # Recovery Structure
    # ------------------------------------------------------

    cluster_ids: List[str] = field(
        default_factory=list
    )

    cluster_names: List[str] = field(
        default_factory=list
    )

    sectors: List[str] = field(
        default_factory=list
    )

    industries: List[str] = field(
        default_factory=list
    )

    countries: List[str] = field(
        default_factory=list
    )

    regions: List[str] = field(
        default_factory=list
    )

    themes: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Breadth
    # ------------------------------------------------------

    cluster_count: int = 0

    recovering_cluster_count: int = 0

    confirmed_cluster_count: int = 0

    stabilizing_cluster_count: int = 0

    deteriorating_cluster_count: int = 0

    recovery_breadth: float = 0.0

    confirmed_recovery_breadth: float = 0.0

    # ------------------------------------------------------
    # Economic Coherence
    # ------------------------------------------------------

    coherence_score: float = 0.0

    mechanism_consistency: float = 0.0

    cross_cluster_consistency: float = 0.0

    demand_consistency: float = 0.0

    supply_consistency: float = 0.0

    policy_consistency: float = 0.0

    capital_cycle_consistency: float = 0.0

    geographic_consistency: float = 0.0

    # ------------------------------------------------------
    # Evidence
    # ------------------------------------------------------

    independent_sources: int = 0

    independent_signals: int = 0

    independent_clusters: int = 0

    supporting_evidence: List[str] = field(
        default_factory=list
    )

    contradictory_evidence: List[str] = field(
        default_factory=list
    )

    evidence_sources: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Temporal Structure
    # ------------------------------------------------------

    temporal_support: float = 0.0

    persistence_score: float = 0.0

    acceleration_score: float = 0.0

    inflection_score: float = 0.0

    reversal_score: float = 0.0

    # ------------------------------------------------------
    # Market Context
    # ------------------------------------------------------

    market_expectation: str = ""

    market_recognition: float = 0.0

    price_response: str = ""

    earnings_response: str = ""

    valuation_response: str = ""

    # ------------------------------------------------------
    # Opportunity Relevance
    #
    # These fields describe relevance only.
    # They do NOT constitute an investment decision.
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
    # Risk / Invalidation
    # ------------------------------------------------------

    key_risks: List[str] = field(
        default_factory=list
    )

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    contradiction_score: float = 0.0

    # ------------------------------------------------------
    # Final Intelligence
    # ------------------------------------------------------

    confidence: float = 0.0

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
    "RecoveryThemeAssessment",
    "RecoveryThemeType",
    "RecoveryThemeStage",
    "RecoveryThemeDirection",
    "RecoveryThemeConfidence",
]