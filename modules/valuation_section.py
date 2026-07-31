"""
===============================================================================
EIOS
Valuation Section

Purpose:
    Stores Valuation Intelligence inside the Master Dossier.

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
class ValuationSection(BaseSection):
    """
    Valuation Intelligence stored in the Master Dossier.
    """

    # -------------------------------------------------------------------------
    # Current Market Data
    # -------------------------------------------------------------------------

    current_price: float = 0.0
    market_cap: float = 0.0
    enterprise_value: float = 0.0

    # -------------------------------------------------------------------------
    # Intrinsic Value
    # -------------------------------------------------------------------------

    intrinsic_value: float = 0.0
    fair_value: float = 0.0
    bear_case_value: float = 0.0
    base_case_value: float = 0.0
    bull_case_value: float = 0.0

    # -------------------------------------------------------------------------
    # Margin of Safety
    # -------------------------------------------------------------------------

    margin_of_safety: float = 0.0
    upside_potential: float = 0.0
    downside_risk: float = 0.0

    # -------------------------------------------------------------------------
    # Valuation Multiples
    # -------------------------------------------------------------------------

    pe: float = 0.0
    pb: float = 0.0
    ev_ebitda: float = 0.0
    ev_sales: float = 0.0
    price_to_fcf: float = 0.0

    # -------------------------------------------------------------------------
    # Expected Returns
    # -------------------------------------------------------------------------

    expected_3y_cagr: float = 0.0
    expected_5y_cagr: float = 0.0
    expected_10y_cagr: float = 0.0

    # -------------------------------------------------------------------------
    # Valuation Models Used
    # -------------------------------------------------------------------------

    valuation_methods: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Key Assumptions
    # -------------------------------------------------------------------------

    growth_assumptions: List[str] = field(default_factory=list)
    risk_assumptions: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Recommendation
    # -------------------------------------------------------------------------

    recommendation: str = ""
    conviction_level: str = ""