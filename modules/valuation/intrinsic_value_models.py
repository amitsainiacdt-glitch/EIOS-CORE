"""
EIOS
Everest Investment Operating System

Intrinsic Value Models

Standard result models used by the Intrinsic Value Office.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class IntrinsicValueResult:
    """
    Final institutional intrinsic value estimate.

    Produced by the Intrinsic Value Office after
    evaluating all available valuation methods.
    """

    # --------------------------------------------------
    # Consensus Valuation
    # --------------------------------------------------

    fair_value: float

    low_estimate: float

    high_estimate: float

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    confidence: int

    agreement: str

    # --------------------------------------------------
    # Method Information
    # --------------------------------------------------

    primary_method: str

    supporting_methods: Dict[str, float] = field(
        default_factory=dict
    )

    rejected_methods: Dict[str, str] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    valuation_count: int = 0

    spread_percent: float = 0.0

    # --------------------------------------------------
    # Commentary
    # --------------------------------------------------

    summary: str = ""

    risks: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )