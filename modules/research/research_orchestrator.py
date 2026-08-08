"""
EIOS
Everest Investment Operating System

Research Orchestrator

Purpose:
Coordinates all research engines and produces a single
AnalysisPack.

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
        ↓
AnalysisPackProcessor
        ↓
CompanyResearch
        ↓
MasterDossier

Rules:

- Performs orchestration only.
- Performs no persistence.
- Does not update CompanyResearch directly.
- Engines perform domain calculations.
- AnalysisPack is the consolidated research result.
- AnalysisPackProcessor is the persistence layer.
"""

from .analysis_pack import AnalysisPack

from .business_engine import BusinessEngine
from .business_quality import BusinessQualityEngine

from modules.financial.financial_engine import FinancialEngine
from modules.management.management_engine import ManagementEngine
from modules.ownership.typed_ownership_engine import TypedOwnershipEngine
from modules.competitive.competitive_engine import CompetitiveEngine
from modules.risk.risk_engine import RiskEngine
from modules.valuation.valuation_engine import ValuationEngine


class ResearchOrchestrator:
    """
    Coordinates all institutional research engines.

    Produces one AnalysisPack.

    Persistence is deliberately excluded from this class.
    """

    def __init__(self, research):

        self.research = research

        # ==========================================================
        # RESEARCH ENGINES
        # ==========================================================

        self.business_engine = BusinessEngine()

        self.business_quality = BusinessQualityEngine(
            research
        )

        self.financial_engine = FinancialEngine(
            research
        )

        self.management_engine = ManagementEngine(
            research
        )

        self.ownership_engine = TypedOwnershipEngine(
            research
        )

        self.competitive_engine = CompetitiveEngine(
            research
        )

        self.risk_engine = RiskEngine(
            research
        )

        self.valuation_engine = ValuationEngine(
            research
        )

    # ==============================================================
    # ANALYZE
    # ==============================================================

    def analyze(
        self,
        company,
        financial_data: dict,
        ownership_data: dict,
        management_data: dict,
        risk_data: dict,
        business_data: dict,
        peers: list | None = None,
    ) -> AnalysisPack:
        """
        Run all research engines and construct one AnalysisPack.

        No persistence occurs in this method.
        """

        # ==========================================================
        # BUSINESS
        # ==========================================================

        business = self.business_quality.analyze(
            business_model=business_data.get(
                "business_model",
                "",
            ),
            moat=business_data.get(
                "moat",
                "",
            ),
            industry=business_data.get(
                "industry",
                company.industry,
            ),
            market_size=business_data.get(
                "market_size",
                "",
            ),
            growth_drivers=business_data.get(
                "growth_drivers",
                [],
            ),
            risks=business_data.get(
                "risks",
                [],
            ),
        )

        # ==========================================================
        # FINANCIAL
        # ==========================================================

        financial = self.financial_engine.analyze(
            financial_data
        )

        # ==========================================================
        # VALUATION
        # ==========================================================

        valuation = self.valuation_engine.analyze(
            financial_data
        )

        # ==========================================================
        # MANAGEMENT
        # ==========================================================

        management = self.management_engine.analyze(
            management_data
        )

        # ==========================================================
        # OWNERSHIP
        # ==========================================================

        ownership = self.ownership_engine.analyze(
            **ownership_data
        )

        # ==========================================================
        # RISK
        # ==========================================================

        risk = self.risk_engine.analyze(
            risk_data
        )

        # ==========================================================
        # COMPETITIVE
        # ==========================================================

        if peers:
            for peer in peers:
                self.competitive_engine.add_peer(
                    peer
                )

        competitive = self.competitive_engine.analyze()

        # ==========================================================
        # ANALYSIS PACK
        # ==========================================================

        pack = AnalysisPack(
            business=business,
            financial=financial,
            management=management,
            ownership=ownership,
            competitive=competitive,
            risk=risk,
            valuation=valuation,
        )

        return pack