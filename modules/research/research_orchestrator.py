"""
===============================================================================
EIOS
Research Orchestrator

Purpose:
    Coordinates all research engines and produces a single AnalysisPack.

Architecture:

ResearchOrchestrator
        ↓
Business Engine
Financial Engine
Management Engine
Ownership Engine
Competitive Engine
Risk Engine
Valuation Engine
        ↓
AnalysisPack

Release:
    3.0
===============================================================================
"""

from .analysis_pack import AnalysisPack

from .business_engine import BusinessEngine
from .business_quality import BusinessQualityEngine

from modules.financial.financial_engine import FinancialEngine
from modules.management.management_engine import ManagementEngine
from modules.ownership.typed_ownership_engine import (
    TypedOwnershipEngine,
)
from modules.competitive.competitive_engine import (
    CompetitiveEngine,
)
from modules.risk.risk_engine import RiskEngine
from modules.valuation.valuation_engine import (
    ValuationEngine,
)


class ResearchOrchestrator:
    """
    Coordinates all research engines.

    Produces a fully populated AnalysisPack.

    Performs no persistence.
    """

    def __init__(self, research):

        self.research = research

        # ==========================================================
        # Research Engines
        # ==========================================================

        self.business_engine = BusinessEngine()
        self.business_quality = BusinessQualityEngine(research)

        self.financial_engine = FinancialEngine(research)

        self.management_engine = ManagementEngine(research)

        self.ownership_engine = TypedOwnershipEngine(research)

        self.competitive_engine = CompetitiveEngine(research)

        self.risk_engine = RiskEngine(research)

        self.valuation_engine = ValuationEngine(research)

    def analyze(self, company):

        pack = AnalysisPack()

        # ==========================================================
        # Business
        # ==========================================================

        business_result = self.business_engine.analyze(
            company
        )

        pack.business = self.business_quality.analyze(
            result=business_result
        )

        # ==========================================================
        # Financial
        # ==========================================================

        pack.financial = self.financial_engine.analyze(
            company
        )

        # ==========================================================
        # Management
        # ==========================================================

        pack.management = self.management_engine.analyze(
            company
        )

        # ==========================================================
        # Ownership
        # ==========================================================

        pack.ownership = self.ownership_engine.analyze(
            company
        )

        # ==========================================================
        # Competitive
        # ==========================================================

        pack.competitive = self.competitive_engine.analyze(
            company
        )

        # ==========================================================
        # Risk
        # ==========================================================

        pack.risk = self.risk_engine.analyze(
            company
        )

        # ==========================================================
        # Valuation
        # ==========================================================

        pack.valuation = self.valuation_engine.analyze(
            company
        )

        return pack