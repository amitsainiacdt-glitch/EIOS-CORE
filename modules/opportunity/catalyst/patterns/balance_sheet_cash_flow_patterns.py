"""
EIOS
Everest Investment Operating System

Catalyst Pattern Family:
    BALANCE_SHEET_CASH_FLOW

Purpose:
Canonical catalyst patterns describing balance-sheet and
cash-flow inflections that can create earnings, liquidity,
capital-allocation, or market-expectation changes.

Architecture:

    Catalyst Taxonomy
            ↓
    Balance Sheet / Cash Flow Pattern Definitions
            ↓
    Catalyst Pattern Registry
            ↓
    Opportunity Engine

Design Principles:

- Definitions only.
- No company-specific assumptions.
- No scoring.
- No ranking.
- No valuation.
- No investment decisions.
- No internet access.
"""


from typing import List


from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)


from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# 1. WORKING CAPITAL RELEASE
# ==========================================================

WORKING_CAPITAL_RELEASE = CatalystPattern(
    pattern_id=(
        "PAT-BALANCE-SHEET-CASH-FLOW-"
        "WORKING-CAPITAL-RELEASE"
    ),

    family=(
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ),

    name="Working Capital Release",

    description=(
        "A structural or cyclical reduction in working capital "
        "requirements releases cash previously absorbed by "
        "receivables, inventory, or other operating assets."
    ),

    trigger_signals=[
        "Reduction in receivable days",
        "Reduction in inventory days",
        "Improvement in payable discipline",
        "Working capital intensity begins to decline",
        "Operating cash flow improves faster than earnings",
    ],

    mechanism=(
        "Lower working capital intensity releases operating "
        "cash and improves the conversion of accounting earnings "
        "into free cash flow."
    ),

    transmission_channels=[
        "Operating cash flow",
        "Free cash flow",
        "Liquidity",
        "Return on invested capital",
        "Debt reduction capacity",
    ],

    leading_indicators=[
        "Receivable days",
        "Inventory days",
        "Payable days",
        "Cash conversion cycle",
        "Working capital as percentage of revenue",
    ],

    confirmation_indicators=[
        "Sustained operating cash flow improvement",
        "Positive free cash flow conversion",
        "Lower working capital intensity",
        "Reduced cash tied up in operations",
    ],

    typical_time_horizon=(
        "2 to 8 quarters"
    ),

    earnings_channels=[
        "Free cash flow improvement",
        "Interest-cost reduction where cash is used for debt repayment",
        "Improved capital efficiency",
    ],

    market_mistake=(
        "The market focuses on reported earnings and fails to "
        "recognize that improving cash conversion can materially "
        "increase the quality and deployability of those earnings."
    ),

    second_order_effects=[
        "Accelerated debt reduction",
        "Greater capacity for reinvestment",
        "Higher shareholder distributions",
        "Improved balance-sheet resilience",
    ],

    disconfirming_evidence=[
        "Working capital improvement reverses",
        "Receivables continue expanding faster than revenue",
        "Inventory remains structurally elevated",
        "Operating cash flow fails to improve",
    ],

    kill_switch=(
        "Working capital intensity fails to improve or the "
        "apparent cash release proves temporary."
    ),
)


# ==========================================================
# 2. FREE CASH FLOW INFLECTION
# ==========================================================

FREE_CASH_FLOW_INFLECTION = CatalystPattern(
    pattern_id=(
        "PAT-BALANCE-SHEET-CASH-FLOW-"
        "FREE-CASH-FLOW-INFLECTION"
    ),

    family=(
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ),

    name="Free Cash Flow Inflection",

    description=(
        "A sustained transition from weak, volatile, or negative "
        "free cash flow toward materially stronger free cash flow "
        "generation."
    ),

    trigger_signals=[
        "Operating cash flow exceeds capital expenditure",
        "Capital expenditure intensity begins normalising",
        "Cash conversion improves",
        "Free cash flow turns sustainably positive",
        "Free cash flow growth exceeds earnings growth",
    ],

    mechanism=(
        "Improving operating cash generation combined with "
        "normalising investment requirements creates a step-up "
        "in distributable and reinvestable cash."
    ),

    transmission_channels=[
        "Free cash flow",
        "Debt repayment",
        "Shareholder distributions",
        "Reinvestment capacity",
        "Intrinsic value perception",
    ],

    leading_indicators=[
        "Operating cash flow",
        "Capital expenditure intensity",
        "Cash conversion",
        "Working capital intensity",
        "Maintenance capex requirements",
    ],

    confirmation_indicators=[
        "Positive free cash flow",
        "Sustained free cash flow generation",
        "Free cash flow conversion improves",
        "Cash generation persists across reporting periods",
    ],

    typical_time_horizon=(
        "2 to 8 quarters"
    ),

    earnings_channels=[
        "Free cash flow per share",
        "Lower financing costs",
        "Higher distributable cash",
        "Higher reinvestment capacity",
    ],

    market_mistake=(
        "The market continues to value the company primarily "
        "through historical earnings while underestimating the "
        "importance of a new free-cash-flow regime."
    ),

    second_order_effects=[
        "Debt reduction",
        "Higher dividends",
        "Share repurchases",
        "Greater strategic flexibility",
        "Improved capital allocation options",
    ],

    disconfirming_evidence=[
        "Free cash flow remains persistently negative",
        "Capital expenditure remains structurally elevated",
        "Operating cash flow does not improve",
        "Cash conversion deteriorates",
    ],

    kill_switch=(
        "The expected free-cash-flow inflection fails to become "
        "sustainable or requires structurally higher investment."
    ),
)


# ==========================================================
# 3. CASH CONVERSION IMPROVEMENT
# ==========================================================

CASH_CONVERSION_IMPROVEMENT = CatalystPattern(
    pattern_id=(
        "PAT-BALANCE-SHEET-CASH-FLOW-"
        "CASH-CONVERSION-IMPROVEMENT"
    ),

    family=(
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ),

    name="Cash Conversion Improvement",

    description=(
        "A measurable improvement in the conversion of reported "
        "profits into operating and free cash flow."
    ),

    trigger_signals=[
        "Operating cash flow increasingly tracks reported earnings",
        "Cash conversion ratio improves",
        "Non-cash earnings components decline",
        "Working capital absorption falls",
        "Cash earnings quality improves",
    ],

    mechanism=(
        "Higher cash conversion reduces the gap between accounting "
        "profit and economic cash generation, increasing the quality "
        "and financial utility of reported earnings."
    ),

    transmission_channels=[
        "Operating cash flow",
        "Free cash flow",
        "Balance-sheet liquidity",
        "Debt repayment capacity",
        "Capital allocation",
    ],

    leading_indicators=[
        "Operating cash flow to EBITDA",
        "Operating cash flow to PAT",
        "Receivable movement",
        "Inventory movement",
        "Cash conversion cycle",
    ],

    confirmation_indicators=[
        "Sustained cash conversion improvement",
        "Operating cash flow tracks earnings",
        "Reduced divergence between profit and cash",
        "Improved free cash flow generation",
    ],

    typical_time_horizon=(
        "2 to 6 quarters"
    ),

    earnings_channels=[
        "Higher free cash flow",
        "Lower funding requirements",
        "Lower interest expense after deleveraging",
    ],

    market_mistake=(
        "The market treats earnings quality as unchanged even "
        "though a larger proportion of reported profits is becoming "
        "convertible into actual cash."
    ),

    second_order_effects=[
        "Reduced dependence on external financing",
        "Improved capital allocation flexibility",
        "Potential valuation-quality re-rating",
        "Greater balance-sheet resilience",
    ],

    disconfirming_evidence=[
        "Cash conversion deteriorates",
        "Operating cash flow repeatedly trails earnings",
        "Receivables or inventory absorb incremental cash",
        "Free cash flow remains weak despite reported profits",
    ],

    kill_switch=(
        "Cash conversion improvement reverses or is shown to be "
        "temporary and non-recurring."
    ),
)


# ==========================================================
# 4. BALANCE-SHEET DELEVERAGING
# ==========================================================

BALANCE_SHEET_DELEVERAGING = CatalystPattern(
    pattern_id=(
        "PAT-BALANCE-SHEET-CASH-FLOW-"
        "BALANCE-SHEET-DELEVERAGING"
    ),

    family=(
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ),

    name="Balance-Sheet Deleveraging",

    description=(
        "A sustained reduction in financial leverage that lowers "
        "balance-sheet risk and increases the proportion of future "
        "cash flow available to equity holders."
    ),

    trigger_signals=[
        "Net debt begins declining",
        "Debt repayment accelerates",
        "Net debt to EBITDA improves",
        "Interest coverage improves",
        "Free cash flow is increasingly directed toward debt reduction",
    ],

    mechanism=(
        "Debt reduction lowers financial obligations and interest "
        "burden, improving liquidity, resilience, and future "
        "capital-allocation flexibility."
    ),

    transmission_channels=[
        "Interest expense",
        "Net debt",
        "Free cash flow",
        "Liquidity",
        "Equity risk",
    ],

    leading_indicators=[
        "Net debt",
        "Gross debt",
        "Net debt to EBITDA",
        "Interest coverage",
        "Debt repayment trajectory",
    ],

    confirmation_indicators=[
        "Sustained net debt reduction",
        "Lower interest expense",
        "Improved leverage ratios",
        "Improved liquidity position",
    ],

    typical_time_horizon=(
        "2 to 12 quarters"
    ),

    earnings_channels=[
        "Lower interest expense",
        "Higher profit after tax",
        "Higher free cash flow",
        "Lower financing risk",
    ],

    market_mistake=(
        "The market continues to apply a high financial-risk "
        "discount despite an observable and sustainable reduction "
        "in leverage."
    ),

    second_order_effects=[
        "Improved credit capacity",
        "Greater acquisition capacity",
        "Higher shareholder distribution potential",
        "Lower earnings volatility",
        "Potential valuation re-rating",
    ],

    disconfirming_evidence=[
        "Debt stops declining",
        "Leverage ratios deteriorate",
        "Interest expense remains elevated",
        "New debt-funded expansion offsets repayment",
    ],

    kill_switch=(
        "Deleveraging reverses or financial leverage remains "
        "structurally elevated."
    ),
)


# ==========================================================
# 5. LIQUIDITY INFLECTION
# ==========================================================

LIQUIDITY_INFLECTION = CatalystPattern(
    pattern_id=(
        "PAT-BALANCE-SHEET-CASH-FLOW-"
        "LIQUIDITY-INFLECTION"
    ),

    family=(
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ),

    name="Liquidity Inflection",

    description=(
        "A material improvement in available liquidity that "
        "reduces financial constraints and expands strategic "
        "optionality."
    ),

    trigger_signals=[
        "Cash balance begins increasing",
        "Undrawn liquidity improves",
        "Operating cash generation strengthens",
        "Short-term obligations become easier to service",
        "Liquidity buffers expand",
    ],

    mechanism=(
        "Higher available liquidity reduces financial constraints "
        "and gives management greater flexibility to withstand "
        "shocks or deploy capital."
    ),

    transmission_channels=[
        "Cash balance",
        "Operating cash flow",
        "Debt service capacity",
        "Capital allocation",
        "Financial resilience",
    ],

    leading_indicators=[
        "Cash and equivalents",
        "Operating cash flow",
        "Current liquidity",
        "Debt maturities",
        "Undrawn committed facilities",
    ],

    confirmation_indicators=[
        "Sustained cash accumulation",
        "Improved liquidity coverage",
        "Lower refinancing dependence",
        "Higher internal funding capacity",
    ],

    typical_time_horizon=(
        "1 to 8 quarters"
    ),

    earnings_channels=[
        "Lower financing costs",
        "Reduced liquidity-related losses",
        "Higher capacity for profitable reinvestment",
    ],

    market_mistake=(
        "The market underestimates the strategic value of a stronger "
        "liquidity position and continues to price the company as "
        "financially constrained."
    ),

    second_order_effects=[
        "Greater acquisition flexibility",
        "Higher resilience during downturns",
        "Ability to fund growth internally",
        "Reduced refinancing risk",
    ],

    disconfirming_evidence=[
        "Cash accumulation reverses",
        "Debt maturities increase without funding visibility",
        "Operating cash flow weakens",
        "Liquidity buffer deteriorates",
    ],

    kill_switch=(
        "The liquidity improvement proves temporary or is offset "
        "by new financial obligations."
    ),
)


# ==========================================================
# 6. CASH-FLOW REINVESTMENT CAPACITY
# ==========================================================

CASH_FLOW_REINVESTMENT_CAPACITY = CatalystPattern(
    pattern_id=(
        "PAT-BALANCE-SHEET-CASH-FLOW-"
        "CASH-FLOW-REINVESTMENT-CAPACITY"
    ),

    family=(
        CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ),

    name="Cash-Flow Reinvestment Capacity",

    description=(
        "An increase in internally generated cash that creates "
        "greater capacity to fund productive growth without "
        "material dependence on external capital."
    ),

    trigger_signals=[
        "Free cash flow expands",
        "Internal funding capacity increases",
        "Capital expenditure can be funded from operations",
        "Net debt remains controlled during growth investment",
        "Return on incremental investment remains attractive",
    ],

    mechanism=(
        "Higher internally generated cash allows the business to "
        "reinvest in growth while reducing dependence on debt or "
        "equity issuance."
    ),

    transmission_channels=[
        "Free cash flow",
        "Capital expenditure",
        "Organic growth",
        "Return on invested capital",
        "Balance-sheet strength",
    ],

    leading_indicators=[
        "Free cash flow",
        "Operating cash flow",
        "Capital expenditure coverage",
        "Net debt trajectory",
        "Incremental return on invested capital",
    ],

    confirmation_indicators=[
        "Growth investment funded internally",
        "Free cash flow remains positive after investment",
        "Leverage remains controlled",
        "Incremental returns remain attractive",
    ],

    typical_time_horizon=(
        "2 to 12 quarters"
    ),

    earnings_channels=[
        "Revenue growth",
        "EBITDA growth",
        "Free cash flow growth",
        "Lower financing expense",
    ],

    market_mistake=(
        "The market sees higher cash generation as merely a "
        "financial outcome rather than recognizing the strategic "
        "optionality created by internally funded reinvestment."
    ),

    second_order_effects=[
        "Faster capacity expansion",
        "Reduced external financing dependence",
        "Higher competitive resilience",
        "Greater long-term compounding capacity",
    ],

    disconfirming_evidence=[
        "Free cash flow fails to expand",
        "Growth requires persistent external funding",
        "Incremental returns deteriorate",
        "Leverage rises materially to fund investment",
    ],

    kill_switch=(
        "Internal cash generation proves insufficient to fund "
        "productive reinvestment or incremental returns deteriorate."
    ),
)


# ==========================================================
# CANONICAL FAMILY COLLECTION
# ==========================================================

BALANCE_SHEET_CASH_FLOW_PATTERNS: List[
    CatalystPattern
] = [
    WORKING_CAPITAL_RELEASE,
    FREE_CASH_FLOW_INFLECTION,
    CASH_CONVERSION_IMPROVEMENT,
    BALANCE_SHEET_DELEVERAGING,
    LIQUIDITY_INFLECTION,
    CASH_FLOW_REINVESTMENT_CAPACITY,
]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [
    "WORKING_CAPITAL_RELEASE",
    "FREE_CASH_FLOW_INFLECTION",
    "CASH_CONVERSION_IMPROVEMENT",
    "BALANCE_SHEET_DELEVERAGING",
    "LIQUIDITY_INFLECTION",
    "CASH_FLOW_REINVESTMENT_CAPACITY",
    "BALANCE_SHEET_CASH_FLOW_PATTERNS",
]