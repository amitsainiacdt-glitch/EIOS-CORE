"""
EIOS
Everest Investment Operating System

Analysis Pack

Purpose:
Standard output object returned by every intelligence engine.

Author:
EIOS

Release:
0.8

Sprint:
008.1
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AnalysisPack:
    """
    Standard analysis output produced by every EIOS intelligence engine.
    """

    engine: str
    score: float | None = None
    confidence: float | None = None
    summary: str = ""

    evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)