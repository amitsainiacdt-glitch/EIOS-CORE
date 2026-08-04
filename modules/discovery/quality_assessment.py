"""
===============================================================================
EIOS
Everest Investment Operating System

Quality Assessment

Purpose:
    Stores the output of the Quality Filter.

Architecture:
    - Passive typed data model.
    - No calculations.
    - Used by QualityFilter.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class QualityAssessment:
    """
    Output of the Quality Filter.
    """

    score: float = 0.0

    rating: str = ""

    passed: bool = False

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)

    confidence: float = 0.0