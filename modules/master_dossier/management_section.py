"""
===============================================================================
EIOS
Management Section

Purpose:
    Stores Management Intelligence inside the Master Dossier.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List

from .base_section import BaseSection


@dataclass
class ManagementSection(BaseSection):
    """
    Management Intelligence stored in the Master Dossier.
    """

    # -------------------------------------------------------------------------
    # Leadership
    # -------------------------------------------------------------------------

    ceo: str = ""
    chairman: str = ""
    promoter: str = ""

    # -------------------------------------------------------------------------
    # Management Scores
    # -------------------------------------------------------------------------

    integrity_score: float = 0.0
    capital_allocation_score: float = 0.0
    execution_score: float = 0.0
    governance_score: float = 0.0
    communication_score: float = 0.0

    # -------------------------------------------------------------------------
    # Capital Allocation
    # -------------------------------------------------------------------------

    dividend_policy: str = ""
    buyback_policy: str = ""
    acquisition_quality: str = ""
    reinvestment_quality: str = ""

    # -------------------------------------------------------------------------
    # Governance
    # -------------------------------------------------------------------------

    promoter_holding: float = 0.0
    promoter_pledge: float = 0.0
    board_independence: str = ""
    auditor_quality: str = ""

    # -------------------------------------------------------------------------
    # Behaviour Assessment
    # -------------------------------------------------------------------------

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Conference Call Intelligence
    # -------------------------------------------------------------------------

    guidance_history: List[str] = field(default_factory=list)
    capital_allocation_history: List[str] = field(default_factory=list)
    communication_notes: List[str] = field(default_factory=list)