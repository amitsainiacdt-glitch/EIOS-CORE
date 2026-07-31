"""
===============================================================================
EIOS
Macro Section

Purpose:
    Stores Macro Intelligence inside the Master Dossier.

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
class MacroSection(BaseSection):
    """
    Macro Intelligence stored in the Master Dossier.
    """

    # -------------------------------------------------------------------------
    # Economy
    # -------------------------------------------------------------------------

    gdp_growth: float = 0.0
    inflation: float = 0.0
    interest_rate: float = 0.0

    # -------------------------------------------------------------------------
    # Currency
    # -------------------------------------------------------------------------

    currency: str = ""
    exchange_rate: float = 0.0

    # -------------------------------------------------------------------------
    # Commodity Environment
    # -------------------------------------------------------------------------

    crude_oil: float = 0.0
    natural_gas: float = 0.0
    commodity_outlook: str = ""

    # -------------------------------------------------------------------------
    # Industry Environment
    # -------------------------------------------------------------------------

    industry_cycle: str = ""
    demand_outlook: str = ""
    regulatory_environment: str = ""

    # -------------------------------------------------------------------------
    # Geopolitics
    # -------------------------------------------------------------------------

    geopolitical_risks: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Macro Opportunities
    # -------------------------------------------------------------------------

    tailwinds: List[str] = field(default_factory=list)
    headwinds: List[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Monitoring
    # -------------------------------------------------------------------------

    watch_items: List[str] = field(default_factory=list)