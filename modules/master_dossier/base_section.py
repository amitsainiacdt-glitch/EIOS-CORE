"""
===============================================================================
EIOS
Master Dossier Base Section

Common structure shared by all dossier sections.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BaseSection:
    """
    Base class for all Master Dossier sections.
    """

    # -------------------------------------------------------------------------
    # Overall Assessment
    # -------------------------------------------------------------------------

    score: float = 0.0
    confidence: float = 0.0
    rating: str = ""
    summary: str = ""

    # -------------------------------------------------------------------------
    # Evidence
    # -------------------------------------------------------------------------

    evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    metadata: Dict = field(default_factory=dict)

    last_updated: str = ""
    source: str = ""