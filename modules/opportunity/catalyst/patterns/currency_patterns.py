"""
EIOS
Everest Investment Operating System

Currency Catalyst Patterns

Purpose:
Canonical catalyst pattern definitions for currency-driven
changes in company economics.

Design Principles:
- Definitions only.
- No scoring.
- No ranking.
- No valuation.
- No company-specific logic.
- No investment decision logic.
"""

from typing import List

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# CURRENCY CATALYST PATTERNS
# ==========================================================

CURRENCY_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. CURRENCY DEPRECIATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CURRENCY-DEPRECIATION",
        family=CatalystFamily.CURRENCY,
        name="Currency Depreciation",
        description=(
            "A sustained depreciation of the domestic currency "
            "materially changes the economics of companies with "
            "meaningful export revenue, foreign-currency exposure, "
            "or imported input costs."
        ),
        mechanism=(
            "Currency depreciation changes the domestic-currency value "
            "of foreign revenues, imported inputs, foreign debt, and "
            "internationally priced products."
        ),
        trigger_signals=[
            "Domestic currency depreciation",
            "Persistent FX weakness",
            "Real effective exchange rate deterioration",
            "Capital outflow pressure",
            "Export competitiveness improvement",
        ],
        leading_indicators=[
            "Spot FX movement",
            "Forward FX curve",
            "Trade balance",
            "Foreign portfolio flows",
            "Export order momentum",
        ],
        confirmation_indicators=[
            "Higher export realisations",
            "Improved reported revenue translation",
            "Stable or improving export margins",
            "Improved cash generation",
            "Earnings estimate revisions",
        ],
        transmission_channels=[
            "Export Revenue",
            "Imported Input Costs",
            "Foreign Currency Debt",
            "Realisation",
            "Operating Margin",
            "Free Cash Flow",
        ],
        typical_time_horizon="3-18 months",
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "The market treats currency depreciation as uniformly "
            "negative and fails to distinguish between companies "
            "that benefit from higher foreign-currency realisations "
            "and companies exposed to imported costs."
        ),
        second_order_effects=[
            "Improved export competitiveness",
            "Higher domestic-currency realisations",
            "Import substitution opportunity",
            "Potential market-share gains",
            "Higher return on export assets",
        ],
        disconfirming_evidence=[
            "Export volumes deteriorate",
            "Imported input costs rise faster than revenue",
            "Currency weakness is fully hedged",
            "Foreign-currency liabilities create material losses",
            "Competitive pricing offsets the benefit",
        ],
        kill_switch=(
            "Currency depreciation fails to improve company economics "
            "because input costs, hedging, demand weakness, or foreign "
            "currency liabilities fully offset the expected benefit."
        ),
    ),

    # ======================================================
    # 2. CURRENCY APPRECIATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CURRENCY-APPRECIATION",
        family=CatalystFamily.CURRENCY,
        name="Currency Appreciation",
        description=(
            "A sustained appreciation of the domestic currency "
            "materially changes input costs, foreign-currency "
            "liabilities, import economics, and reported earnings."
        ),
        mechanism=(
            "Currency appreciation reduces the domestic-currency "
            "cost of imported inputs and foreign-currency liabilities "
            "while potentially reducing the domestic-currency value "
            "of foreign revenue."
        ),
        trigger_signals=[
            "Domestic currency appreciation",
            "Foreign capital inflows",
            "Improving trade balance",
            "Lower imported inflation",
            "Reduced FX volatility",
        ],
        leading_indicators=[
            "Spot FX movement",
            "Forward FX curve",
            "Import cost trends",
            "Foreign capital flows",
            "Commodity import prices",
        ],
        confirmation_indicators=[
            "Lower imported input costs",
            "Lower finance costs on foreign debt",
            "Gross margin improvement",
            "Lower working-capital requirements",
            "Improved cash conversion",
        ],
        transmission_channels=[
            "Imported Input Costs",
            "Foreign Currency Debt",
            "Revenue Translation",
            "Gross Margin",
            "Interest Cost",
            "Free Cash Flow",
        ],
        typical_time_horizon="3-18 months",
        earnings_channels=[
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "The market focuses on the negative translation effect "
            "on exporters while underestimating the earnings benefit "
            "for companies with substantial imported inputs or "
            "foreign-currency liabilities."
        ),
        second_order_effects=[
            "Lower inflation pressure",
            "Improved purchasing power",
            "Lower working-capital requirements",
            "Improved balance-sheet resilience",
            "Potential margin expansion",
        ],
        disconfirming_evidence=[
            "Export revenue declines materially",
            "Imported-cost benefit is hedged",
            "Domestic demand weakens",
            "Currency appreciation reverses quickly",
            "Foreign revenue translation losses dominate",
        ],
        kill_switch=(
            "Currency appreciation fails to generate sustainable "
            "economic benefits because the expected input-cost or "
            "financing benefit is absent or is outweighed by weaker "
            "foreign revenue economics."
        ),
    ),

    # ======================================================
    # 3. EXPORT COMPETITIVENESS
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CURRENCY-EXPORT-COMPETITIVENESS",
        family=CatalystFamily.CURRENCY,
        name="Export Competitiveness Inflection",
        description=(
            "Currency movements materially improve the price "
            "competitiveness of domestic producers in international "
            "markets, creating an opportunity for export growth "
            "and market-share gains."
        ),
        mechanism=(
            "A more competitive currency reduces the effective "
            "foreign-currency price of domestic production, allowing "
            "companies to compete more effectively for international "
            "orders while maintaining acceptable domestic margins."
        ),
        trigger_signals=[
            "Competitive currency depreciation",
            "Export quotation advantage",
            "International price competitiveness",
            "New export enquiries",
            "Customer sourcing diversification",
        ],
        leading_indicators=[
            "Export enquiries",
            "RFQs from overseas customers",
            "New customer qualification",
            "Export quotations",
            "Order-book growth",
        ],
        confirmation_indicators=[
            "Higher export orders",
            "Export revenue growth",
            "New international customers",
            "Improved capacity utilisation",
            "Sustained export market share",
        ],
        transmission_channels=[
            "Export Pricing",
            "Order Intake",
            "Export Volume",
            "Market Share",
            "Capacity Utilisation",
            "Operating Leverage",
        ],
        typical_time_horizon="6-36 months",
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "The market treats currency depreciation as a temporary "
            "macro variable and fails to recognize the potential "
            "structural gain in export competitiveness and customer "
            "share migration."
        ),
        second_order_effects=[
            "International market-share gains",
            "Customer diversification",
            "Higher capacity utilisation",
            "Operating leverage",
            "Improved export credibility",
        ],
        disconfirming_evidence=[
            "International competitors cut prices",
            "Export enquiries fail to convert",
            "Quality or delivery remains uncompetitive",
            "Capacity constraints prevent growth",
            "Currency advantage reverses",
        ],
        kill_switch=(
            "Currency competitiveness does not translate into "
            "sustained export orders, customer wins, or market-share "
            "gains."
        ),
    ),

    # ======================================================
    # 4. INPUT COST INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CURRENCY-INPUT-COST-INFLECTION",
        family=CatalystFamily.CURRENCY,
        name="Currency Input Cost Inflection",
        description=(
            "A meaningful currency movement changes the domestic "
            "cost of imported raw materials, components, energy, "
            "or other internationally priced inputs."
        ),
        mechanism=(
            "Currency movement changes the domestic-currency cost "
            "of imported inputs, creating a direct change in gross "
            "margin, working capital, and free cash flow."
        ),
        trigger_signals=[
            "FX movement",
            "Import cost change",
            "Foreign supplier pricing",
            "Imported commodity exposure",
            "Currency-linked procurement costs",
        ],
        leading_indicators=[
            "Currency movement",
            "Import price indices",
            "Supplier quotations",
            "Inventory replacement cost",
            "Procurement contracts",
        ],
        confirmation_indicators=[
            "Lower or higher landed input cost",
            "Gross margin movement",
            "Inventory cost normalization",
            "Working-capital improvement",
            "Reported procurement savings",
        ],
        transmission_channels=[
            "Input Costs",
            "Gross Margin",
            "Inventory Cost",
            "Working Capital",
            "EBITDA",
            "FCF",
        ],
        typical_time_horizon="1-12 months",
        earnings_channels=[
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "The market focuses on headline currency movements "
            "without recognizing the timing and magnitude of the "
            "pass-through into actual inventory and procurement costs."
        ),
        second_order_effects=[
            "Margin expansion or contraction",
            "Working-capital changes",
            "Inventory valuation effects",
            "Pricing response",
            "Competitive positioning",
        ],
        disconfirming_evidence=[
            "Input costs are fully hedged",
            "Supplier pricing offsets FX movement",
            "Inventory timing delays the effect",
            "Customer pricing fully absorbs the change",
            "FX movement reverses before transmission",
        ],
        kill_switch=(
            "The currency movement fails to produce a material "
            "change in sustainable landed input economics."
        ),
    ),

    # ======================================================
    # 5. TRANSLATION INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CURRENCY-TRANSLATION-INFLECTION",
        family=CatalystFamily.CURRENCY,
        name="Currency Translation Inflection",
        description=(
            "Changes in exchange rates materially alter the "
            "reported domestic-currency value of foreign revenue, "
            "profits, assets, or liabilities."
        ),
        mechanism=(
            "Foreign-currency financial results are translated into "
            "the reporting currency, causing reported revenue, "
            "profit, assets, or liabilities to change even when "
            "underlying local-currency economics remain stable."
        ),
        trigger_signals=[
            "Foreign revenue growth",
            "International subsidiary expansion",
            "FX translation movement",
            "Foreign asset exposure",
            "Cross-border earnings growth",
        ],
        leading_indicators=[
            "Foreign revenue mix",
            "Geographic earnings mix",
            "FX movement",
            "Foreign subsidiary profitability",
            "Currency exposure disclosures",
        ],
        confirmation_indicators=[
            "Reported revenue translation",
            "Reported earnings translation",
            "Foreign-currency asset movement",
            "FX impact disclosed by management",
            "Consensus estimate revisions",
        ],
        transmission_channels=[
            "Reported Revenue",
            "Reported EBITDA",
            "Reported EPS",
            "Net Assets",
            "Net Debt",
        ],
        typical_time_horizon="1-12 months",
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "Net Income",
        ],
        market_mistake=(
            "The market confuses translation-driven changes in "
            "reported financials with changes in underlying operating "
            "performance, or fails to anticipate the magnitude of "
            "translation effects."
        ),
        second_order_effects=[
            "Changed reported growth rates",
            "Analyst estimate revisions",
            "Multiple interpretation changes",
            "Debt-ratio changes",
            "Investor perception changes",
        ],
        disconfirming_evidence=[
            "Foreign exposure is immaterial",
            "Natural hedges offset translation",
            "Underlying local-currency results deteriorate",
            "Currency effect is already fully reflected",
            "Translation impact is non-material to valuation",
        ],
        kill_switch=(
            "Currency translation does not materially alter reported "
            "financial outcomes or investor expectations."
        ),
    ),

    # ======================================================
    # 6. HEDGING INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CURRENCY-HEDGING-INFLECTION",
        family=CatalystFamily.CURRENCY,
        name="Currency Hedging Inflection",
        description=(
            "A change in currency hedging coverage, duration, "
            "strategy, or effectiveness materially changes the "
            "company's exposure to future FX movements."
        ),
        mechanism=(
            "Changes in hedging coverage alter the timing and "
            "magnitude with which currency movements reach reported "
            "revenue, input costs, margins, cash flow, or financial "
            "results."
        ),
        trigger_signals=[
            "Hedging ratio change",
            "Hedging policy change",
            "Forward contract repricing",
            "Hedge maturity change",
            "Natural hedge development",
        ],
        leading_indicators=[
            "Hedging ratio",
            "Hedge maturity profile",
            "Forward contract rates",
            "Foreign currency exposure",
            "Management hedging commentary",
        ],
        confirmation_indicators=[
            "Realised hedge gains or losses",
            "Reported FX impact",
            "Margin impact",
            "Cash-flow impact",
            "Changed sensitivity to FX movement",
        ],
        transmission_channels=[
            "FX Exposure",
            "Input Costs",
            "Revenue Realisation",
            "EBITDA Margin",
            "Finance Cost",
            "FCF",
        ],
        typical_time_horizon="1-18 months",
        earnings_channels=[
            "EBITDA",
            "EBIT",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "The market assumes historical hedging behaviour will "
            "continue and fails to recognize that changing hedge "
            "coverage can materially alter future earnings sensitivity."
        ),
        second_order_effects=[
            "Lower or higher earnings volatility",
            "Changed cash-flow visibility",
            "Changed margin predictability",
            "Balance-sheet exposure changes",
            "Revised risk perception",
        ],
        disconfirming_evidence=[
            "Hedging policy remains unchanged",
            "FX exposure is immaterial",
            "Natural hedges fully offset exposure",
            "Hedge effectiveness remains unchanged",
            "Currency movement has negligible earnings impact",
        ],
        kill_switch=(
            "Changes in hedging strategy fail to produce a material "
            "change in the company's effective currency exposure or "
            "future earnings sensitivity."
        ),
    ),
]


# ==========================================================
# PUBLIC EXPORT
# ==========================================================

__all__ = [
    "CURRENCY_PATTERNS",
]