"""
===============================================================================
EIOS
Valuation Section

Purpose:
    Stores institutional valuation analysis inside the Master Dossier.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from dataclasses import dataclass, field

from .base_section import BaseSection


@dataclass
class ValuationSection(BaseSection):
    """
    Stores valuation analysis for the company.
    """

    # -------------------------------------------------------------------------
    # Intrinsic Value
    # -------------------------------------------------------------------------

    intrinsic_value: float = 0.0
    current_price: float = 0.0
    margin_of_safety: float = 0.0

    # -------------------------------------------------------------------------
    # Fair Value
    # -------------------------------------------------------------------------

    fair_value: float = 0.0
    expected_cagr: float = 0.0

    # -------------------------------------------------------------------------
    # Valuation Method
    # -------------------------------------------------------------------------

    valuation_method: str = ""

    # -------------------------------------------------------------------------
    # Supporting Information
    # -------------------------------------------------------------------------

    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)