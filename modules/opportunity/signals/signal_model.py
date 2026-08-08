"""
EIOS
Everest Investment Operating System

Canonical Opportunity Signal Model

Purpose:
Defines the immutable intelligence object used by the
Opportunity Intelligence Office.

Architecture:

External Information
        ↓
Signal
        ↓
Validation
        ↓
Catalyst
        ↓
Opportunity

Design Principles:
- Passive data model only.
- No business calculations.
- No persistence.
- No company-specific logic.
- Evidence and confidence are explicit.
- Designed to support macro, trade, policy, sector,
  company, earnings, accounting, geopolitical, commodity,
  news and market intelligence.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


# ==========================================================
# SIGNAL DOMAIN
# ==========================================================


class SignalDomain(Enum):
    """
    Primary domain from which the signal originates.
    """

    MACRO = "Macro"
    MONETARY = "Monetary"
    FISCAL = "Fiscal"
    TRADE = "International Trade"
    GEOPOLITICAL = "Geopolitical"
    COMMODITY = "Commodity"
    POLICY = "Government Policy"
    REGULATORY = "Regulatory"
    SECTOR = "Sector"
    CAPITAL_CYCLE = "Capital Cycle"
    COMPANY = "Company"
    EARNINGS = "Earnings"
    ACCOUNTING = "Accounting"
    TECHNOLOGY = "Technology"
    NEWS = "News"
    MARKET = "Market"
    LIQUIDITY = "Liquidity"


class SignalType(Enum):
    """
    Nature of the observed signal.
    """

    CHANGE = "Change"
    ACCELERATION = "Acceleration"
    DECELERATION = "Deceleration"
    INFLECTION = "Inflection"
    SURPRISE = "Surprise"
    DIVERGENCE = "Divergence"
    TREND = "Trend"
    EVENT = "Event"
    ANOMALY = "Anomaly"
    STRUCTURAL = "Structural"


class SignalDirection(Enum):
    """
    Direction of economic or investment impact.
    """

    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    MIXED = "Mixed"
    UNKNOWN = "Unknown"


class SignalStage(Enum):
    """
    Maturity of the signal.
    """

    NOISE = "Noise"
    WEAK = "Weak Signal"
    EMERGING = "Emerging Signal"
    VALIDATED = "Validated Signal"
    CATALYST = "Catalyst"
    EARNINGS_IMPACT = "Earnings Impact"
    MARKET_RECOGNIZED = "Market Recognized"


class TimeHorizon(Enum):
    """
    Expected time horizon of the signal's impact.
    """

    IMMEDIATE = "0-3 Months"
    MEDIUM_TERM = "3-12 Months"
    STRUCTURAL = "1-3 Years"
    LONG_TERM = "3-5+ Years"


class EvidenceQuality(Enum):
    """
    Quality of supporting evidence.
    """

    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"


# ==========================================================
# CANONICAL SIGNAL
# ==========================================================


@dataclass
class Signal:
    """
    Canonical Opportunity Intelligence signal.

    This is a passive data model.

    Engines are responsible for:
        - validation
        - scoring
        - confidence calculation
        - causal analysis
        - aggregation

    The Signal object stores the resulting intelligence.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    signal_id: str = ""

    title: str = ""

    description: str = ""

    domain: SignalDomain = SignalDomain.COMPANY

    signal_type: SignalType = SignalType.CHANGE

    direction: SignalDirection = SignalDirection.UNKNOWN

    stage: SignalStage = SignalStage.WEAK

    horizon: TimeHorizon = TimeHorizon.MEDIUM_TERM

    # ------------------------------------------------------
    # Origin
    # ------------------------------------------------------

    source: str = ""

    source_type: str = ""

    source_date: str = ""

    detected_date: str = ""

    # ------------------------------------------------------
    # Entities
    # ------------------------------------------------------

    countries: List[str] = field(
        default_factory=list
    )

    sectors: List[str] = field(
        default_factory=list
    )

    companies: List[str] = field(
        default_factory=list
    )

    commodities: List[str] = field(
        default_factory=list
    )

    themes: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Economic Meaning
    # ------------------------------------------------------

    economic_mechanism: str = ""

    supply_demand_impact: str = ""

    earnings_impact: str = ""

    valuation_impact: str = ""

    # ------------------------------------------------------
    # Signal Strength
    # ------------------------------------------------------

    magnitude: float = 0.0

    probability: float = 0.0

    persistence: float = 0.0

    relevance: float = 0.0

    corroboration: float = 0.0

    confidence: float = 0.0

    evidence_quality: EvidenceQuality = (
        EvidenceQuality.C
    )

    # ------------------------------------------------------
    # Evidence
    # ------------------------------------------------------

    evidence: List[str] = field(
        default_factory=list
    )

    supporting_sources: List[str] = field(
        default_factory=list
    )

    contradictory_evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Market Context
    # ------------------------------------------------------

    market_expectation: str = ""

    market_recognition: float = 0.0

    price_reaction: str = ""

    # ------------------------------------------------------
    # Causal Chain
    # ------------------------------------------------------

    causal_chain: List[str] = field(
        default_factory=list
    )

    beneficiaries: List[str] = field(
        default_factory=list
    )

    adversely_affected: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    independent_confirmation: int = 0

    historical_precedent: str = ""

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )