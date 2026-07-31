"""
===============================================================================
EIOS
Management Section

Purpose:
    Stores typed Management Intelligence inside the Master Dossier.

Architecture:
    Passive domain model only.
    All management calculations belong inside management engines.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List

from .base_section import BaseSection


@dataclass
class ManagementSection(BaseSection):
    """
    Typed Management Intelligence stored in the Master Dossier.
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
    governance_score: float = 0.0
    behaviour_score: float = 0.0
    execution_score: float = 0.0
    communication_score: float = 0.0

    # -------------------------------------------------------------------------
    # Capital Allocation
    # -------------------------------------------------------------------------

    roiic_assessment: str = ""
    capital_allocation_assessment: str = ""
    reinvestment_quality: str = ""
    acquisition_quality: str = ""
    buyback_policy: str = ""
    dividend_policy: str = ""

    # -------------------------------------------------------------------------
    # Governance
    # -------------------------------------------------------------------------

    promoter_holding: float = 0.0
    promoter_pledge: float = 0.0

    promoter_holding_assessment: str = ""
    promoter_pledge_assessment: str = ""

    related_party_transactions: str = ""
    auditor_quality: str = ""
    regulatory_issues: str = ""
    board_independence: str = ""

    # -------------------------------------------------------------------------
    # Behaviour Assessment
    # -------------------------------------------------------------------------

    execution_assessment: str = ""
    guidance_reliability: str = ""
    capital_discipline: str = ""
    transparency: str = ""
    long_term_focus: str = ""
    shareholder_orientation: str = ""

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Communication Assessment
    # -------------------------------------------------------------------------

    conference_call_quality: str = ""
    annual_report_quality: str = ""
    guidance_clarity: str = ""
    risk_disclosure: str = ""
    shareholder_communication: str = ""
    management_accessibility: str = ""

    # -------------------------------------------------------------------------
    # Historical Intelligence
    # -------------------------------------------------------------------------

    guidance_history: List[str] = field(default_factory=list)
    capital_allocation_history: List[str] = field(default_factory=list)
    communication_notes: List[str] = field(default_factory=list)