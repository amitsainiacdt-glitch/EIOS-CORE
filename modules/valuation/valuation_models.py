"""
EIOS
Everest Investment Operating System

Valuation Models

Purpose:
Shared data models used by all valuation engines.

Author:
EIOS

Release:
0.8

Sprint:
008.1
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValuationResult:
    """
    Standard output returned by every valuation method.
    """

    method: str
    fair_value: float
    confidence: float

    summary: str = ""

    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)