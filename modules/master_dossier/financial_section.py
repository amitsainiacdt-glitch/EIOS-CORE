"""
===============================================================================
EIOS
Everest Investment Operating System

Financial Section

Purpose:
    Defines the typed financial domain model stored inside the Master Dossier.

Architecture:
    - FinancialSection is a passive domain data model.
    - It performs no financial calculations.
    - Financial calculations belong exclusively to financial engines.
    - MasterDossier owns the FinancialSection instance.
    - Downstream consumers should read financial intelligence from
      MasterDossier.financial.

Design Principle:
    Dataclasses represent state.
    Engines represent behaviour.

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
class FinancialSection(BaseSection):
    """
    Typed financial intelligence stored in the Master Dossier.

    This section contains financial state only. It must not calculate,
    derive, fetch, score, or interpret financial information.

    All values are populated by the Financial Engine and related
    specialist engines.
    """

    # =========================================================================
    # Profitability
    # =========================================================================

    revenue: float = 0.0
    ebitda: float = 0.0
    operating_profit: float = 0.0
    net_profit: float = 0.0
    eps: float = 0.0

    # =========================================================================
    # Growth
    # =========================================================================

    revenue_growth: float = 0.0
    profit_growth: float = 0.0
    eps_growth: float = 0.0
    fcf_growth: float = 0.0

    # =========================================================================
    # Return Ratios
    # =========================================================================

    roe: float = 0.0
    roce: float = 0.0
    roiic: float = 0.0
    roiic_rating: str = ""
    roa: float = 0.0

    # =========================================================================
    # Margins
    # =========================================================================

    gross_margin: float = 0.0
    ebitda_margin: float = 0.0
    operating_margin: float = 0.0
    net_margin: float = 0.0

    # =========================================================================
    # Cash Flow
    # =========================================================================

    operating_cash_flow: float = 0.0
    free_cash_flow: float = 0.0
    capex: float = 0.0

    operating_cash_conversion: float = 0.0
    cash_quality: str = ""

    # =========================================================================
    # Balance Sheet
    # =========================================================================

    debt: float = 0.0
    cash: float = 0.0
    net_debt: float = 0.0

    debt_to_equity: float = 0.0
    interest_coverage: float = 0.0

    # =========================================================================
    # Operating Efficiency
    # =========================================================================

    asset_turnover: float = 0.0

    # =========================================================================
    # Working Capital
    # =========================================================================

    working_capital: float = 0.0
    current_ratio: float = 0.0
    working_capital_turnover: float = 0.0

    inventory_days: float = 0.0
    receivable_days: float = 0.0
    payable_days: float = 0.0
    cash_conversion_cycle: float = 0.0

    # =========================================================================
    # Financial Scorecard
    # =========================================================================

    raw_score: float = 0.0
    max_score: float = 0.0

    # =========================================================================
    # Financial Quality
    # =========================================================================

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)