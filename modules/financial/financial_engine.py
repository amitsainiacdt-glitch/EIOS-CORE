"""
===============================================================================
EIOS
Everest Investment Operating System

Financial Engine

Purpose:
    Coordinates institutional financial analysis and writes the resulting
    typed financial intelligence into the Master Dossier.

Architecture:
    Financial data
        -> specialist financial engines
        -> FinancialSection
        -> CompanyResearch
        -> MasterDossier.financial

Design Principles:
    - FinancialSection is passive domain state.
    - FinancialEngine owns financial calculations and orchestration.
    - CompanyResearch persists typed domain state.
    - MasterDossier is the single source of truth.
    - No legacy financial dictionary is persisted.
    - Temporary compatibility structures must remain local and must never
      become authoritative domain state.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from modules.research.company_research import CompanyResearch
from modules.master_dossier.financial_section import FinancialSection

from modules.financial.financial_metrics import FinancialMetrics
from modules.financial.ratio_engine import RatioEngine
from modules.financial.roiic_engine import ROIICEngine
from modules.financial.cashflow_engine import CashFlowEngine
from modules.financial.working_capital_engine import WorkingCapitalEngine
from modules.financial.capital_allocation import CapitalAllocationEngine
from modules.financial.financial_scorecard import FinancialScorecard

from modules.valuation.valuation_assumptions import ValuationAssumptionsBuilder

from modules.core.scoring.scoring_engine import ScoringEngine
from modules.core.scoring.confidence_engine import ConfidenceEngine

from modules.intelligence.intelligence import Intelligence


class FinancialEngine:
    """
    Coordinates financial analysis and stores the result as FinancialSection.

    The engine performs calculations and orchestration only.

    It does not persist independent financial dictionaries. The authoritative
    financial state is MasterDossier.financial.
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        self.metrics = FinancialMetrics()
        self.ratios = RatioEngine()
        self.roiic = ROIICEngine()

        self.cashflow = CashFlowEngine()
        self.working_capital = WorkingCapitalEngine()
        self.capital_allocation = CapitalAllocationEngine()

        self.scorecard = FinancialScorecard()

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

        self.valuation_builder = ValuationAssumptionsBuilder()

    def analyze(self, financial_data: dict):

        print("\nStarting Financial Analysis...")

        # =====================================================================
        # BASIC GROWTH METRICS
        # =====================================================================

        revenue_growth = self.metrics.revenue_growth(
            financial_data.get("current_revenue", 0),
            financial_data.get("previous_revenue", 0),
        )

        eps_growth = self.metrics.eps_growth(
            financial_data.get("current_eps", 0),
            financial_data.get("previous_eps", 0),
        )

        profit_growth = self.metrics.profit_growth(
            financial_data.get("current_profit", 0),
            financial_data.get("previous_profit", 0),
        )

        free_cash_flow = self.metrics.free_cash_flow(
            financial_data.get("operating_cash_flow", 0),
            financial_data.get("capital_expenditure", 0),
        )

        # =====================================================================
        # RETURN AND BALANCE-SHEET RATIOS
        # =====================================================================

        roce = self.ratios.roce(
            financial_data.get("ebit", 0),
            financial_data.get("capital_employed", 0),
        )

        roe = self.ratios.roe(
            financial_data.get("net_profit", 0),
            financial_data.get("shareholder_equity", 0),
        )

        debt_to_equity = self.ratios.debt_to_equity(
            financial_data.get("total_debt", 0),
            financial_data.get("shareholder_equity", 0),
        )

        interest_coverage = self.ratios.interest_coverage(
            financial_data.get("ebit", 0),
            financial_data.get("interest_expense", 0),
        )

        asset_turnover = self.ratios.asset_turnover(
            financial_data.get("revenue", 0),
            financial_data.get("total_assets", 0),
        )

        # =====================================================================
        # ROIIC
        # =====================================================================

        roiic = self.roiic.calculate(
            financial_data.get("current_nopat", 0),
            financial_data.get("previous_nopat", 0),
            financial_data.get("current_invested_capital", 0),
            financial_data.get("previous_invested_capital", 0),
        )

        roiic_rating = self.roiic.interpret(roiic)

        # =====================================================================
        # CASH FLOW QUALITY
        # =====================================================================

        operating_cash_conversion = (
            self.cashflow.operating_cash_conversion(
                financial_data.get("operating_cash_flow", 0),
                financial_data.get("net_profit", 0),
            )
        )

        cash_quality = self.cashflow.cash_quality(
            financial_data.get("operating_cash_flow", 0),
            financial_data.get("net_profit", 0),
        )

        # =====================================================================
        # WORKING CAPITAL
        # =====================================================================

        working_capital = self.working_capital.working_capital(
            financial_data.get("current_assets", 0),
            financial_data.get("current_liabilities", 0),
        )

        current_ratio = self.working_capital.current_ratio(
            financial_data.get("current_assets", 0),
            financial_data.get("current_liabilities", 0),
        )

        working_capital_turnover = (
            self.working_capital.working_capital_turnover(
                financial_data.get("revenue", 0),
                working_capital,
            )
        )

        cash_conversion_cycle = (
            self.working_capital.cash_conversion_cycle(
                financial_data.get("inventory_days", 0),
                financial_data.get("receivable_days", 0),
                financial_data.get("payable_days", 0),
            )
        )

        # =====================================================================
        # CAPITAL ALLOCATION
        #
        # Capital allocation remains an analytical output of its specialist
        # engine. It is intentionally not persisted as an untyped dictionary
        # inside FinancialSection.
        # =====================================================================

        capital_allocation = self.capital_allocation.evaluate(
            financial_data.get("capital_expenditure", 0),
            financial_data.get("acquisitions", 0),
            financial_data.get("dividends", 0),
            financial_data.get("share_buybacks", 0),
            financial_data.get("debt_reduction", 0),
        )

        # =====================================================================
        # FINANCIAL SCORECARD
        # =====================================================================

        scorecard = self.scorecard.evaluate(
            revenue_growth,
            eps_growth,
            roce,
            roe,
            debt_to_equity,
            free_cash_flow,
        )

        score_result = self.scoring_engine.calculate(
            score=scorecard["Total Score"],
            max_score=scorecard["Max Score"],
        )

        confidence_result = self.confidence_engine.calculate(
            evidence_items=6,
            expected_items=10,
        )

        # =====================================================================
        # BUILD TYPED FINANCIAL DOMAIN STATE
        # =====================================================================

        financial = FinancialSection()

        # ---------------------------------------------------------------------
        # Profitability
        # ---------------------------------------------------------------------

        financial.revenue = financial_data.get(
            "current_revenue",
            financial_data.get("revenue", 0),
        )

        financial.ebitda = financial_data.get("ebitda", 0)

        financial.operating_profit = financial_data.get(
            "operating_profit",
            financial_data.get("ebit", 0),
        )

        financial.net_profit = financial_data.get(
            "net_profit",
            financial_data.get("current_profit", 0),
        )

        financial.eps = financial_data.get(
            "current_eps",
            financial_data.get("eps", 0),
        )

        # ---------------------------------------------------------------------
        # Growth
        # ---------------------------------------------------------------------

        financial.revenue_growth = revenue_growth
        financial.profit_growth = profit_growth
        financial.eps_growth = eps_growth

        # ---------------------------------------------------------------------
        # Return Ratios
        # ---------------------------------------------------------------------

        financial.roe = roe
        financial.roce = roce
        financial.roiic = roiic
        financial.roiic_rating = roiic_rating

        # ---------------------------------------------------------------------
        # Margins / Additional Ratios
        #
        # These are populated only when supplied by the current financial
        # input dataset. FinancialEngine does not fabricate unavailable data.
        # ---------------------------------------------------------------------

        financial.roa = financial_data.get("roa", 0)

        financial.gross_margin = financial_data.get("gross_margin", 0)
        financial.ebitda_margin = financial_data.get("ebitda_margin", 0)
        financial.operating_margin = financial_data.get(
            "operating_margin",
            0,
        )
        financial.net_margin = financial_data.get("net_margin", 0)

        # ---------------------------------------------------------------------
        # Cash Flow
        # ---------------------------------------------------------------------

        financial.operating_cash_flow = financial_data.get(
            "operating_cash_flow",
            0,
        )

        financial.free_cash_flow = free_cash_flow

        financial.capex = financial_data.get(
            "capital_expenditure",
            0,
        )

        financial.operating_cash_conversion = (
            operating_cash_conversion
        )

        financial.cash_quality = cash_quality

        # ---------------------------------------------------------------------
        # Balance Sheet
        # ---------------------------------------------------------------------

        financial.debt = financial_data.get("total_debt", 0)
        financial.cash = financial_data.get("cash", 0)

        financial.net_debt = (
            financial.debt - financial.cash
        )

        financial.debt_to_equity = debt_to_equity
        financial.interest_coverage = interest_coverage

        # ---------------------------------------------------------------------
        # Operating Efficiency
        # ---------------------------------------------------------------------

        financial.asset_turnover = asset_turnover

        # ---------------------------------------------------------------------
        # Working Capital
        # ---------------------------------------------------------------------

        financial.working_capital = working_capital
        financial.current_ratio = current_ratio

        financial.working_capital_turnover = (
            working_capital_turnover
        )

        financial.inventory_days = financial_data.get(
            "inventory_days",
            0,
        )

        financial.receivable_days = financial_data.get(
            "receivable_days",
            0,
        )

        financial.payable_days = financial_data.get(
            "payable_days",
            0,
        )

        financial.cash_conversion_cycle = cash_conversion_cycle

        # ---------------------------------------------------------------------
        # Scorecard
        # ---------------------------------------------------------------------

        financial.raw_score = score_result.score
        financial.max_score = score_result.max_score

        financial.score = score_result.percentage
        financial.confidence = confidence_result.confidence
        financial.rating = score_result.grade

        # ---------------------------------------------------------------------
        # Assessment
        # ---------------------------------------------------------------------

        financial.summary = (
            "Institutional financial analysis completed successfully."
        )

        financial.evidence = [
            "Revenue Growth",
            "EPS Growth",
            "ROCE",
            "ROE",
            "ROIIC",
            "Free Cash Flow",
        ]

        financial.assumptions = [
            "Financial statements are accurate."
        ]

        financial.source = "FinancialEngine"

        # =====================================================================
        # TEMPORARY VALUATION COMPATIBILITY BRIDGE
        #
        # ValuationAssumptionsBuilder currently expects the legacy financial
        # summary dictionary.
        #
        # This dictionary exists only inside this method and is never stored
        # in CompanyResearch or MasterDossier.
        #
        # It will be removed when ValuationAssumptionsBuilder is migrated to
        # consume FinancialSection directly.
        # =====================================================================

        valuation_compatibility_summary = {
            "Revenue Growth": financial.revenue_growth,
            "ROIIC": financial.roiic,
            "Cash Flow": {
                "Free Cash Flow": financial.free_cash_flow,
            },
        }

        valuation_assumptions = self.valuation_builder.build(
            financial_data,
            valuation_compatibility_summary,
        )

        # Preserve valuation assumptions temporarily as metadata for
        # compatibility and traceability without creating parallel
        # authoritative financial state.
        financial.metadata["valuation_assumptions"] = (
            valuation_assumptions
        )

        # Capital allocation remains available as supporting metadata until
        # its own typed domain representation is introduced.
        financial.metadata["capital_allocation"] = (
            capital_allocation
        )

        # =====================================================================
        # UPDATE MASTER DOSSIER
        #
        # NOTE:
        # Temporary direct persistence during typed migration.
        #
        # Future architecture:
        #
        # FinancialEngine
        #        ↓
        # FinancialSection
        #        ↓
        # AnalysisPack
        #        ↓
        # AnalysisPackProcessor
        #        ↓
        # CompanyResearch
        #
        # This call will be removed once the unified AnalysisPack pipeline
        # becomes the sole persistence path.
        # =====================================================================

        self.research.update_financials(financial)

        # =====================================================================
        # FINANCIAL INTELLIGENCE
        # =====================================================================

        financial_intelligence = Intelligence(
            title="Financial Analysis",
            category="Financial",
            source_engine="FinancialEngine",
            conclusion=financial.summary,
            entity=self.research.dossier.company_name,
            confidence=financial.confidence,
            evidence=list(financial.evidence),
            assumptions=list(financial.assumptions),
            reasoning=[
                (
                    "Financial Engine completed institutional "
                    "financial analysis."
                )
            ],
            tags=[
                "financial",
                "scorecard",
                "roiic",
            ],
        )

        self.research.context.publish_intelligence(
            financial_intelligence
        )

        print("Financial Analysis Completed")