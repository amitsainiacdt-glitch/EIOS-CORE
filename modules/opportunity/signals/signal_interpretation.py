"""
EIOS
Everest Investment Operating System

Signal Interpretation
=====================

Purpose
-------
Defines the explicit interpretation required to convert an
EvidenceItem into a canonical Opportunity Signal.

This is a passive data model only.

The model does not:
- perform semantic interpretation
- perform AI analysis
- calculate opportunity scores
- perform valuation
- perform persistence
- mutate EvidenceItem
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .signal_model import (
    SignalDirection,
    SignalDomain,
    SignalStage,
    SignalType,
    TimeHorizon,
)


@dataclass(frozen=True)
class SignalInterpretation:
    """
    Explicit interpretation supplied to the Signal
    Interpretation Engine.

    No interpretation is inferred automatically.

    Every material Signal classification must therefore be
    explicitly supplied by the caller.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    title: str = ""

    description: str = ""

    # ------------------------------------------------------
    # Detection
    # ------------------------------------------------------

    detected_date: str = ""

    # ------------------------------------------------------
    # Classification
    # ------------------------------------------------------

    domain: SignalDomain = SignalDomain.COMPANY

    signal_type: SignalType = SignalType.CHANGE

    direction: SignalDirection = SignalDirection.UNKNOWN

    stage: SignalStage = SignalStage.WEAK

    horizon: TimeHorizon = TimeHorizon.MEDIUM_TERM

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
    # Validation / Invalidation
    # ------------------------------------------------------

    historical_precedent: str = ""

    invalidation_conditions: List[str] = field(
        default_factory=list
    )


__all__ = [
    "SignalInterpretation",
]