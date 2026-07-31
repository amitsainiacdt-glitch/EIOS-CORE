"""
===============================================================================
EIOS
Analysis Pack

Purpose:
    Aggregates the output of all research engines into a single immutable
    object that can be consumed by the MasterDossierManager.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class AnalysisPack:
    """
    Container for the complete research output of one company.
    """

    business: Optional[Any] = None
    financial: Optional[Any] = None
    management: Optional[Any] = None
    ownership: Optional[Any] = None
    competitive: Optional[Any] = None
    risk: Optional[Any] = None
    valuation: Optional[Any] = None
    macro: Optional[Any] = None
    committee: Optional[Any] = None