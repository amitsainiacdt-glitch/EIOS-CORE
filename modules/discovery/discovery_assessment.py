"""
===============================================================================
EIOS
Everest Investment Operating System

Discovery Assessment

Purpose:
    Standard assessment produced by every Discovery filter.

Architecture:
    - Passive data model.
    - Shared by all Discovery filters.
    - Contains no business logic.

Author:
    EIOS

Release:
    3.1
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class DiscoveryAssessment:
    """
    Standard output of every Discovery filter.
    """

    filter_name: str = ""

    score: float = 0.0

    passed: bool = False

    confidence: float = 0.0

    strengths: List[str] = field(default_factory=list)

    concerns: List[str] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    notes: List[str] = field(default_factory=list)