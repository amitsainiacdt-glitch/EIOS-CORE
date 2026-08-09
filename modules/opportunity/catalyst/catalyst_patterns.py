"""
EIOS
Everest Investment Operating System

Catalyst Pattern Model

Purpose:
Represents a specific pattern beneath a canonical
CatalystFamily.

This is a passive data model.
It performs no scoring, ranking, valuation,
classification, or investment decision.
"""

from dataclasses import dataclass, field
from typing import List

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


@dataclass(frozen=True)
class CatalystPattern:
    """
    Specific, machine-readable form of a catalyst.

    Example:

        CatalystFamily.CAPACITY_EXPANSION
                    ↓
        Brownfield Capacity Expansion
    """

    pattern_id: str

    family: CatalystFamily

    name: str

    description: str = ""

    trigger_signals: List[str] = field(
        default_factory=list
    )

    mechanism: str = ""

    transmission_channels: List[str] = field(
        default_factory=list
    )

    leading_indicators: List[str] = field(
        default_factory=list
    )

    confirmation_indicators: List[str] = field(
        default_factory=list
    )

    typical_time_horizon: str = ""

    earnings_channels: List[str] = field(
        default_factory=list
    )

    market_mistake: str = ""

    second_order_effects: List[str] = field(
        default_factory=list
    )

    disconfirming_evidence: List[str] = field(
        default_factory=list
    )

    kill_switch: str = ""


__all__ = [
    "CatalystPattern",
]