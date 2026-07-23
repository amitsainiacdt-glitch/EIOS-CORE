"""
Financial Engine

Coordinates all financial analysis modules.
Acts as the entry point for financial intelligence.
"""

from modules.research.company_research import CompanyResearch

from modules.financial.financial_metrics import FinancialMetrics
from modules.financial.ratio_engine import RatioEngine
from modules.financial.roiic_engine import ROIICEngine
from modules.financial.cashflow_engine import CashFlowEngine
from modules.financial.working_capital_engine import WorkingCapitalEngine
from modules.financial.capital_allocation import CapitalAllocationEngine
from modules.financial.financial_scorecard import FinancialScorecard


class FinancialEngine:
    """
    Coordinates financial analysis and updates CompanyResearch.
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

    def analyze(self, financial_data: dict):

        print("\nStarting Financial Analysis...")

        # =====================================================
        # BASIC METRICS
        # =====================================================

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

        # =====================================================
        # RATIOS
        # =====================================================

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

        # =====================================================
        # ROIIC
        # =====================================================

        roiic = self.roiic.calculate(
            financial_data.get("current_nopat", 0),
            financial_data.get("previous_nopat", 0),
            financial_data.get("current_invested_capital", 0),
            financial_data.get("previous_invested_capital", 0),
        )

        roiic_rating = self.roiic.interpret(roiic)

        # =====================================================
        # CASH FLOW ENGINE
        # =====================================================

        operating_cash_conversion = self.cashflow.operating_cash_conversion(
            financial_data.get("operating_cash_flow", 0),
            financial_data.get("net_profit", 0),
        )

        cash_quality = self.cashflow.cash_quality(
            financial_data.get("operating_cash_flow", 0),
            financial_data.get("net_profit", 0),
        )

        cash_flow_summary = {
            "Free Cash Flow": free_cash_flow,
            "Operating Cash Conversion": operating_cash_conversion,
            "Cash Quality": cash_quality,
        }

        # =====================================================
        # WORKING CAPITAL ENGINE
        # =====================================================

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

        working_capital_summary = {
            "Working Capital": working_capital,
            "Current Ratio": current_ratio,
            "Working Capital Turnover": working_capital_turnover,
            "Cash Conversion Cycle": cash_conversion_cycle,
        }

        # =====================================================
        # CAPITAL ALLOCATION ENGINE
        # =====================================================

        capital_allocation = self.capital_allocation.evaluate(
            financial_data.get("capital_expenditure", 0),
            financial_data.get("acquisitions", 0),
            financial_data.get("dividends", 0),
            financial_data.get("share_buybacks", 0),
            financial_data.get("debt_reduction", 0),
        )

        # =====================================================
        # FINANCIAL SCORECARD
        # =====================================================

        scorecard = self.scorecard.evaluate(
            revenue_growth,
            eps_growth,
            roce,
            roe,
            debt_to_equity,
            free_cash_flow,
        )

        # =====================================================
        # MASTER FINANCIAL SUMMARY
        # =====================================================

        financial_summary = {
            "Revenue Growth": revenue_growth,
            "EPS Growth": eps_growth,
            "Profit Growth": profit_growth,
            "ROCE": roce,
            "ROE": roe,
            "Debt to Equity": debt_to_equity,
            "Interest Coverage": interest_coverage,
            "Asset Turnover": asset_turnover,
            "ROIIC": roiic,
            "ROIIC Rating": roiic_rating,

            "Cash Flow": cash_flow_summary,
            "Working Capital": working_capital_summary,
            "Capital Allocation": capital_allocation,
            "Financial Scorecard": scorecard,
        }

        self.research.update_financials(financial_summary)

        print("Financial Analysis Completed")