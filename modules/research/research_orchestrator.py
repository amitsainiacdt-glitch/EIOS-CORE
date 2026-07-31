"""
===============================================================================
EIOS
Research Orchestrator

Purpose:
    Coordinates all research engines and produces a single AnalysisPack.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from .analysis_pack import AnalysisPack
from .business_engine import BusinessEngine


class ResearchOrchestrator:
    """
    Coordinates all research engines.
    """

    def __init__(self):

        self.business_engine = BusinessEngine()

        # Future engines
        self.financial_engine = None
        self.management_engine = None
        self.ownership_engine = None
        self.competitive_engine = None
        self.risk_engine = None
        self.valuation_engine = None
        self.macro_engine = None

    def analyze(self, company):
        """
        Perform complete company research.

        Parameters
        ----------
        company
            Company research object.

        Returns
        -------
        AnalysisPack
        """

        pack = AnalysisPack()

        # ---------------------------------------------------------
        # Business Analysis
        # ---------------------------------------------------------

        pack.business = self.business_engine.analyze(company)

        # ---------------------------------------------------------
        # Future Engines
        # ---------------------------------------------------------

        if self.financial_engine:
            pack.financial = self.financial_engine.analyze(company)

        if self.management_engine:
            pack.management = self.management_engine.analyze(company)

        if self.ownership_engine:
            pack.ownership = self.ownership_engine.analyze(company)

        if self.competitive_engine:
            pack.competitive = self.competitive_engine.analyze(company)

        if self.risk_engine:
            pack.risk = self.risk_engine.analyze(company)

        if self.valuation_engine:
            pack.valuation = self.valuation_engine.analyze(company)

        if self.macro_engine:
            pack.macro = self.macro_engine.analyze(company)

        return pack