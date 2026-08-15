"""
EIOS
Everest Investment Operating System

Catalyst Pattern Module

Family:
    MANAGEMENT_CAPITAL_ALLOCATION

Purpose:
    Canonical catalyst patterns describing changes in management
    capital allocation behaviour that can alter future business
    economics, cash generation, balance-sheet quality, and
    shareholder value creation.

Design Principles:
    - Pattern definitions only.
    - No scoring.
    - No ranking.
    - No valuation.
    - No investment decision.
    - No company-specific assumptions.
    - No external data access.
"""


from typing import List


from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)


from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# PATTERN 1
# ==========================================================

CAPITAL_DEPLOYMENT_INFLECTION = CatalystPattern(

    pattern_id=(
        "PAT-MANAGEMENT-CAPITAL-ALLOCATION-"
        "CAPITAL-DEPLOYMENT-INFLECTION"
    ),

    family=(
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ),

    name=(
        "Capital Deployment Inflection"
    ),

    description=(
        "A meaningful change in management's capital deployment "
        "behaviour redirects capital toward higher-return internal "
        "opportunities, productive assets, or clearly defined "
        "strategic priorities."
    ),

    mechanism=(
        "Management changes the allocation of internally generated "
        "capital toward opportunities with superior expected "
        "economic returns, potentially improving future growth "
        "and capital efficiency."
    ),

    trigger_signals=[
        "Change in capital allocation policy",
        "New investment programme",
        "Management capital deployment guidance",
        "Increase in productive capital expenditure",
        "Clear strategic capital priorities",
    ],

    leading_indicators=[
        "Capital expenditure initiation",
        "Project approvals",
        "Investment milestones",
        "Capacity or capability deployment",
        "Management allocation commentary",
    ],

    confirmation_indicators=[
        "Higher incremental returns",
        "Improved cash generation",
        "Revenue growth from deployed capital",
        "Improved return on capital",
        "Sustained capital productivity",
    ],

    transmission_channels=[
        "Reinvestment",
        "Capacity expansion",
        "Productivity improvement",
        "Growth acceleration",
        "Capital efficiency",
    ],

    typical_time_horizon=(
        "12-60 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "EBITDA growth",
        "Free cash flow growth",
        "Return on invested capital",
    ],

    market_mistake=(
        "The market may focus on the immediate cash outflow from "
        "new investment while underestimating the economic value "
        "created if the newly deployed capital earns attractive "
        "incremental returns."
    ),

    second_order_effects=[
        "Higher productive capacity",
        "Improved competitive position",
        "Higher future free cash flow",
        "Stronger growth runway",
        "Improved capital allocation credibility",
    ],

    disconfirming_evidence=[
        "Projects remain delayed",
        "Capital productivity deteriorates",
        "Expected returns are not achieved",
        "Investment fails to generate incremental growth",
        "Management repeatedly changes allocation priorities",
    ],

    kill_switch=(
        "New capital deployment fails to demonstrate measurable "
        "economic productivity or management abandons the stated "
        "allocation framework."
    ),
)


# ==========================================================
# PATTERN 2
# ==========================================================

HIGH_RETURN_REINVESTMENT = CatalystPattern(

    pattern_id=(
        "PAT-MANAGEMENT-CAPITAL-ALLOCATION-"
        "HIGH-RETURN-REINVESTMENT"
    ),

    family=(
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ),

    name=(
        "High-Return Reinvestment"
    ),

    description=(
        "Management systematically reinvests internally generated "
        "cash into opportunities capable of generating attractive "
        "incremental returns while maintaining disciplined capital "
        "allocation."
    ),

    mechanism=(
        "A high-return business retains and reinvests capital into "
        "productive opportunities, allowing compounding of earnings "
        "and free cash flow without requiring proportional external "
        "capital."
    ),

    trigger_signals=[
        "Increasing reinvestment rate",
        "Expansion of high-return operations",
        "Management reinvestment commentary",
        "Internal growth opportunities",
        "Evidence of attractive incremental returns",
    ],

    leading_indicators=[
        "Reinvestment rate",
        "New capacity",
        "New customers",
        "Product expansion",
        "Geographic expansion",
    ],

    confirmation_indicators=[
        "Sustained incremental ROIC",
        "Organic revenue growth",
        "Free cash flow growth",
        "Stable or improving margins",
        "Higher earnings generated from retained capital",
    ],

    transmission_channels=[
        "Internal compounding",
        "Revenue growth",
        "Capacity expansion",
        "Market share",
        "Free cash flow growth",
    ],

    typical_time_horizon=(
        "24-84 months"
    ),

    earnings_channels=[
        "Organic revenue growth",
        "EBITDA growth",
        "PAT growth",
        "Free cash flow growth",
    ],

    market_mistake=(
        "The market may underestimate the compounding effect of "
        "retaining capital inside a business that can consistently "
        "reinvest at attractive incremental returns."
    ),

    second_order_effects=[
        "Compounding earnings",
        "Higher intrinsic economic capacity",
        "Stronger competitive position",
        "Reduced dependence on external capital",
        "Higher long-term free cash flow",
    ],

    disconfirming_evidence=[
        "Incremental returns decline materially",
        "Growth requires excessive capital",
        "Free cash flow conversion deteriorates",
        "Reinvestment opportunities weaken",
        "Capital intensity rises without corresponding returns",
    ],

    kill_switch=(
        "Reinvestment no longer produces attractive incremental "
        "economic returns on a sustained basis."
    ),
)


# ==========================================================
# PATTERN 3
# ==========================================================

SHAREHOLDER_DISTRIBUTION_INFLECTION = CatalystPattern(

    pattern_id=(
        "PAT-MANAGEMENT-CAPITAL-ALLOCATION-"
        "SHAREHOLDER-DISTRIBUTION-INFLECTION"
    ),

    family=(
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ),

    name=(
        "Shareholder Distribution Inflection"
    ),

    description=(
        "Management shifts from retaining excess capital toward "
        "greater shareholder distributions through dividends, "
        "buybacks, or other disciplined capital-return mechanisms."
    ),

    mechanism=(
        "When internal reinvestment opportunities are insufficient "
        "to justify retaining excess cash, management returns capital "
        "to shareholders, potentially improving capital efficiency "
        "and reducing value-destructive cash accumulation."
    ),

    trigger_signals=[
        "Dividend policy change",
        "Share buyback programme",
        "Higher payout guidance",
        "Capital return framework",
        "Management excess-cash commentary",
    ],

    leading_indicators=[
        "Dividend declaration",
        "Buyback authorisation",
        "Payout-ratio change",
        "Cash balance trend",
        "Capital-return announcements",
    ],

    confirmation_indicators=[
        "Completed buybacks",
        "Sustained dividend growth",
        "Reduced excess cash",
        "Stable balance sheet",
        "Improved per-share metrics",
    ],

    transmission_channels=[
        "Dividends",
        "Share repurchases",
        "Per-share earnings",
        "Capital efficiency",
        "Cash deployment",
    ],

    typical_time_horizon=(
        "6-36 months"
    ),

    earnings_channels=[
        "EPS improvement",
        "Per-share free cash flow",
        "Lower idle capital",
        "Share-count reduction",
    ],

    market_mistake=(
        "The market may treat shareholder distributions as a "
        "short-term financial event while overlooking the improvement "
        "in capital efficiency from removing excess or low-return capital."
    ),

    second_order_effects=[
        "Lower share count",
        "Higher per-share cash flow",
        "Improved capital discipline",
        "Reduced excess cash",
        "Greater shareholder alignment",
    ],

    disconfirming_evidence=[
        "Distributions are funded by excessive debt",
        "Buybacks occur at unattractive prices",
        "Core investment requirements are neglected",
        "Cash generation weakens",
        "Distribution policy is repeatedly reversed",
    ],

    kill_switch=(
        "Capital distributions materially weaken the balance sheet "
        "or compromise the company's ability to fund productive "
        "internal opportunities."
    ),
)


# ==========================================================
# PATTERN 4
# ==========================================================

DEBT_REDUCTION_BALANCE_SHEET_REPAIR = CatalystPattern(

    pattern_id=(
        "PAT-MANAGEMENT-CAPITAL-ALLOCATION-"
        "DEBT-REDUCTION-BALANCE-SHEET-REPAIR"
    ),

    family=(
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ),

    name=(
        "Debt Reduction / Balance-Sheet Repair"
    ),

    description=(
        "Management redirects cash generation toward debt reduction "
        "and balance-sheet repair, reducing financial risk and "
        "potentially increasing future capital flexibility."
    ),

    mechanism=(
        "Debt repayment reduces interest burden, refinancing risk, "
        "and financial leverage, allowing a greater proportion of "
        "future cash generation to support productive investment "
        "or shareholder returns."
    ),

    trigger_signals=[
        "Debt repayment programme",
        "Deleveraging target",
        "Asset monetisation for debt reduction",
        "Free cash flow prioritised for debt repayment",
        "Management leverage guidance",
    ],

    leading_indicators=[
        "Net debt reduction",
        "Debt maturity reduction",
        "Interest expense trend",
        "Debt-to-EBITDA improvement",
        "Cash flow allocation",
    ],

    confirmation_indicators=[
        "Lower net debt",
        "Lower interest expense",
        "Improved credit profile",
        "Higher financial flexibility",
        "Improved free cash flow after interest",
    ],

    transmission_channels=[
        "Interest-cost reduction",
        "Balance-sheet repair",
        "Financial-risk reduction",
        "Free cash flow improvement",
        "Capital flexibility",
    ],

    typical_time_horizon=(
        "12-48 months"
    ),

    earnings_channels=[
        "Lower interest expense",
        "PAT growth",
        "Free cash flow growth",
        "Reduced financial drag",
    ],

    market_mistake=(
        "The market may focus on current leverage and overlook the "
        "speed at which disciplined cash allocation can repair the "
        "balance sheet and improve future financial economics."
    ),

    second_order_effects=[
        "Lower refinancing risk",
        "Lower interest burden",
        "Improved investment flexibility",
        "Improved credit access",
        "Potential future shareholder distributions",
    ],

    disconfirming_evidence=[
        "Debt does not decline",
        "Cash flow remains insufficient",
        "New debt is repeatedly added",
        "Interest burden remains elevated",
        "Asset sales fail to improve leverage",
    ],

    kill_switch=(
        "Management fails to reduce financial leverage despite "
        "sufficient operating cash generation, or deleveraging "
        "is offset by renewed debt accumulation."
    ),
)


# ==========================================================
# PATTERN 5
# ==========================================================

ACCRETIVE_ACQUISITION_CAPITAL_ALLOCATION = CatalystPattern(

    pattern_id=(
        "PAT-MANAGEMENT-CAPITAL-ALLOCATION-"
        "ACCRETIVE-ACQUISITION"
    ),

    family=(
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ),

    name=(
        "Accretive Acquisition Capital Allocation"
    ),

    description=(
        "Management deploys capital into acquisitions where the "
        "target business provides strategic or economic benefits "
        "and the transaction has the potential to improve long-term "
        "per-share economics."
    ),

    mechanism=(
        "Capital is transferred into an external business or asset "
        "that can add earnings, capabilities, customers, technology, "
        "distribution, or strategic positioning at an acceptable "
        "economic cost."
    ),

    trigger_signals=[
        "Acquisition announcement",
        "Management acquisition rationale",
        "Target strategic fit",
        "Transaction funding plan",
        "Synergy guidance",
    ],

    leading_indicators=[
        "Transaction completion",
        "Integration milestones",
        "Customer cross-selling",
        "Synergy capture",
        "Target business performance",
    ],

    confirmation_indicators=[
        "Earnings accretion",
        "Free cash flow accretion",
        "Synergy realisation",
        "Return on acquisition capital",
        "Improved competitive position",
    ],

    transmission_channels=[
        "Revenue synergies",
        "Cost synergies",
        "Capability acquisition",
        "Market expansion",
        "Earnings accretion",
    ],

    typical_time_horizon=(
        "12-48 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "EBITDA growth",
        "EPS accretion",
        "Free cash flow growth",
    ],

    market_mistake=(
        "The market may apply a blanket acquisition discount and "
        "underestimate the value of disciplined acquisitions when "
        "management has a demonstrable record of selecting and "
        "integrating productive assets."
    ),

    second_order_effects=[
        "Market-share expansion",
        "Capability expansion",
        "Distribution expansion",
        "Higher operating leverage",
        "Strategic moat strengthening",
    ],

    disconfirming_evidence=[
        "Acquisition integration fails",
        "Synergies do not materialise",
        "Target performance deteriorates",
        "Leverage becomes excessive",
        "Returns remain below acquisition cost",
    ],

    kill_switch=(
        "Acquisitions repeatedly destroy capital, fail to integrate, "
        "or generate returns below the economic cost of capital."
    ),
)


# ==========================================================
# PATTERN 6
# ==========================================================

DIVESTMENT_CAPITAL_RECYCLING = CatalystPattern(

    pattern_id=(
        "PAT-MANAGEMENT-CAPITAL-ALLOCATION-"
        "DIVESTMENT-CAPITAL-RECYCLING"
    ),

    family=(
        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ),

    name=(
        "Divestment / Capital Recycling"
    ),

    description=(
        "Management exits non-core, low-return, or strategically "
        "misaligned assets and redeploys the released capital toward "
        "higher-return opportunities or shareholder distributions."
    ),

    mechanism=(
        "Capital is released from lower-productivity assets and "
        "redirected toward businesses, projects, debt reduction, "
        "or shareholder returns with better expected economics."
    ),

    trigger_signals=[
        "Strategic review",
        "Non-core asset classification",
        "Divestment announcement",
        "Asset monetisation",
        "Capital recycling programme",
    ],

    leading_indicators=[
        "Potential buyer interest",
        "Transaction approvals",
        "Asset-sale negotiations",
        "Debt repayment",
        "Redeployment guidance",
    ],

    confirmation_indicators=[
        "Transaction completion",
        "Capital released",
        "Higher-return reinvestment",
        "Debt reduction",
        "Improved return on capital",
    ],

    transmission_channels=[
        "Capital recycling",
        "Portfolio simplification",
        "Debt reduction",
        "Core-business investment",
        "Shareholder returns",
    ],

    typical_time_horizon=(
        "6-36 months"
    ),

    earnings_channels=[
        "Interest-cost reduction",
        "Core revenue growth",
        "Margin improvement",
        "Free cash flow improvement",
    ],

    market_mistake=(
        "The market may treat asset sales as isolated transactions "
        "without recognising the potential improvement in portfolio "
        "quality and capital productivity from redeploying capital."
    ),

    second_order_effects=[
        "Higher capital efficiency",
        "Simpler corporate structure",
        "Greater core-business focus",
        "Lower leverage",
        "Improved strategic flexibility",
    ],

    disconfirming_evidence=[
        "Asset sale fails",
        "Assets are sold at unattractive economics",
        "Capital is not productively redeployed",
        "Debt remains elevated",
        "Core returns fail to improve",
    ],

    kill_switch=(
        "Divestment proceeds are not redeployed productively, "
        "or management repeatedly destroys value through poor "
        "capital recycling decisions."
    ),
)


# ==========================================================
# CANONICAL FAMILY COLLECTION
# ==========================================================

MANAGEMENT_CAPITAL_ALLOCATION_PATTERNS: List[
    CatalystPattern
] = [

    CAPTIAL_DEPLOYMENT_INFLECTION
    if False
    else CAPITAL_DEPLOYMENT_INFLECTION,

    HIGH_RETURN_REINVESTMENT,

    SHAREHOLDER_DISTRIBUTION_INFLECTION,

    DEBT_REDUCTION_BALANCE_SHEET_REPAIR,

    ACCRETIVE_ACQUISITION_CAPITAL_ALLOCATION,

    DIVESTMENT_CAPITAL_RECYCLING,
]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "CAPITAL_DEPLOYMENT_INFLECTION",

    "HIGH_RETURN_REINVESTMENT",

    "SHAREHOLDER_DISTRIBUTION_INFLECTION",

    "DEBT_REDUCTION_BALANCE_SHEET_REPAIR",

    "ACCRETIVE_ACQUISITION_CAPITAL_ALLOCATION",

    "DIVESTMENT_CAPITAL_RECYCLING",

    "MANAGEMENT_CAPITAL_ALLOCATION_PATTERNS",
]
