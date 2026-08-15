"""
EIOS
Everest Investment Operating System

Margin Expansion Catalyst Patterns

Purpose:
Canonical catalyst patterns belonging to the
MARGIN_EXPANSION catalyst family.

Design:
Passive data definitions only.

No scoring.
No ranking.
No valuation.
No investment decision.
"""

from typing import List

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# MARGIN EXPANSION CATALYST PATTERNS
# ==========================================================


MARGIN_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. OPERATING LEVERAGE
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARGIN-OPERATING-LEVERAGE",
        family=CatalystFamily.MARGIN_EXPANSION,
        name="Operating Leverage",

        description=(
            "Revenue growth causes fixed operating costs to be "
            "spread across a larger revenue base, producing "
            "disproportionate operating profit growth."
        ),

        trigger_signals=[
            "revenue acceleration",
            "fixed-cost absorption",
            "operating leverage",
            "incremental margin improvement",
        ],

        mechanism=(
            "A relatively fixed operating-cost base grows more "
            "slowly than revenue, allowing incremental revenue "
            "to convert into operating profit at a higher margin."
        ),

        transmission_channels=[
            "Revenue",
            "Operating Cost",
            "EBITDA Margin",
            "EBIT Margin",
        ],

        leading_indicators=[
            "Revenue growth",
            "Stable fixed-cost base",
            "Improving employee productivity",
            "Higher asset utilisation",
        ],

        confirmation_indicators=[
            "Incremental EBITDA margin expansion",
            "Operating margin improvement",
            "Operating expenses growing slower than revenue",
            "Higher operating profit conversion",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "EBITDA",
            "EBIT",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market models operating expenses as growing "
            "proportionally with revenue and underestimates "
            "incremental operating margins."
        ),

        second_order_effects=[
            "Higher free cash flow",
            "Improved ROIC",
            "Greater reinvestment capacity",
            "Higher earnings visibility",
        ],

        disconfirming_evidence=[
            "Operating costs rise in line with revenue",
            "Employee or overhead costs accelerate",
            "Incremental margins fail to improve",
            "Growth requires proportional operating investment",
        ],

        kill_switch=(
            "Incremental revenue fails to generate sustainably "
            "higher operating profit conversion."
        ),
    ),


    # ======================================================
    # 2. GROSS MARGIN RECOVERY
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARGIN-GROSS-MARGIN-RECOVERY",
        family=CatalystFamily.MARGIN_EXPANSION,
        name="Gross Margin Recovery",

        description=(
            "Gross margins recover after temporary pressure from "
            "input costs, supply disruption, customer mix, or "
            "other reversible factors."
        ),

        trigger_signals=[
            "input-cost normalization",
            "gross margin recovery",
            "raw material correction",
            "supply normalization",
        ],

        mechanism=(
            "A temporary source of gross-margin pressure reverses, "
            "allowing gross profit per unit of revenue to recover."
        ),

        transmission_channels=[
            "Input Costs",
            "Gross Profit",
            "Gross Margin",
            "EBITDA",
        ],

        leading_indicators=[
            "Input commodity prices",
            "Freight normalization",
            "Supplier pricing",
            "Inventory cost normalization",
        ],

        confirmation_indicators=[
            "Sequential gross margin improvement",
            "Year-on-year gross margin recovery",
            "Improved gross profit per unit",
            "Stable customer pricing",
        ],

        typical_time_horizon="3-18 months",

        earnings_channels=[
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market extrapolates temporarily depressed gross "
            "margins and fails to recognize mean reversion."
        ),

        second_order_effects=[
            "Earnings recovery",
            "Cash-flow improvement",
            "Improved return on capital",
        ],

        disconfirming_evidence=[
            "Input costs remain structurally elevated",
            "Customer pricing deteriorates",
            "Gross margins fail to recover",
            "Competitive intensity increases",
        ],

        kill_switch=(
            "The apparent gross-margin pressure proves structural "
            "rather than temporary."
        ),
    ),


    # ======================================================
    # 3. PROCUREMENT IMPROVEMENT
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARGIN-PROCUREMENT-IMPROVEMENT",
        family=CatalystFamily.MARGIN_EXPANSION,
        name="Procurement Improvement",

        description=(
            "Improved sourcing, supplier negotiation, purchasing "
            "scale, or procurement discipline lowers input costs."
        ),

        trigger_signals=[
            "supplier renegotiation",
            "procurement savings",
            "sourcing optimisation",
            "vendor consolidation",
        ],

        mechanism=(
            "The company reduces the cost of purchased inputs "
            "without proportionately reducing product quality "
            "or customer value."
        ),

        transmission_channels=[
            "Input Cost",
            "Cost of Goods Sold",
            "Gross Margin",
            "EBITDA",
        ],

        leading_indicators=[
            "Supplier negotiations",
            "Vendor consolidation",
            "Procurement initiatives",
            "Purchase-price variance",
        ],

        confirmation_indicators=[
            "Lower unit input cost",
            "Gross margin improvement",
            "Procurement savings realised",
            "Stable product quality",
        ],

        typical_time_horizon="6-24 months",

        earnings_channels=[
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market assumes the historical procurement cost "
            "structure will persist and underestimates achievable "
            "structural savings."
        ),

        second_order_effects=[
            "Higher free cash flow",
            "Improved competitive pricing flexibility",
            "Higher return on incremental capital",
        ],

        disconfirming_evidence=[
            "Supplier costs increase",
            "Savings fail to materialize",
            "Quality deteriorates",
            "Procurement gains are one-time only",
        ],

        kill_switch=(
            "Procurement initiatives fail to produce durable "
            "unit-cost improvement."
        ),
    ),


    # ======================================================
    # 4. MANUFACTURING EFFICIENCY
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARGIN-MANUFACTURING-EFFICIENCY",
        family=CatalystFamily.MARGIN_EXPANSION,
        name="Manufacturing Efficiency",

        description=(
            "Process improvement, productivity gains, yield "
            "improvement, reduced waste, or better throughput "
            "lowers manufacturing cost per unit."
        ),

        trigger_signals=[
            "yield improvement",
            "productivity improvement",
            "lower scrap",
            "process optimisation",
            "manufacturing efficiency",
        ],

        mechanism=(
            "Operational improvements increase output or reduce "
            "resource consumption for the same manufacturing base."
        ),

        transmission_channels=[
            "Unit Cost",
            "Yield",
            "Manufacturing Overhead",
            "Gross Margin",
            "EBITDA",
        ],

        leading_indicators=[
            "Higher production yield",
            "Lower rejection rates",
            "Reduced scrap",
            "Higher labour productivity",
        ],

        confirmation_indicators=[
            "Lower cost per unit",
            "Higher manufacturing margin",
            "Improved yield",
            "Sustained productivity gains",
        ],

        typical_time_horizon="6-24 months",

        earnings_channels=[
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market treats operational efficiency as "
            "incremental and fails to recognize its cumulative "
            "effect on unit economics."
        ),

        second_order_effects=[
            "Higher capacity economics",
            "Improved ROIC",
            "Stronger competitive position",
            "Greater cash generation",
        ],

        disconfirming_evidence=[
            "Yield fails to improve",
            "Productivity gains reverse",
            "Quality problems increase",
            "Cost per unit remains unchanged",
        ],

        kill_switch=(
            "Operational improvements fail to produce sustained "
            "unit-cost or productivity gains."
        ),
    ),


    # ======================================================
    # 5. AUTOMATION-LED MARGIN EXPANSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARGIN-AUTOMATION",
        family=CatalystFamily.MARGIN_EXPANSION,
        name="Automation-Led Margin Expansion",

        description=(
            "Automation reduces repetitive labour or process costs "
            "while increasing consistency, throughput, or scalability."
        ),

        trigger_signals=[
            "automation deployment",
            "robotics adoption",
            "process automation",
            "labour productivity",
            "digital workflow automation",
        ],

        mechanism=(
            "Technology replaces or augments repetitive processes, "
            "reducing recurring operating cost per unit of output."
        ),

        transmission_channels=[
            "Labour Cost",
            "Operating Cost",
            "Unit Cost",
            "EBITDA Margin",
        ],

        leading_indicators=[
            "Automation capex",
            "Deployment milestones",
            "Lower labour intensity",
            "Higher throughput per employee",
        ],

        confirmation_indicators=[
            "Lower recurring labour cost",
            "Higher output per employee",
            "Improved operating margin",
            "Stable or improving quality",
        ],

        typical_time_horizon="12-36 months",

        earnings_channels=[
            "EBITDA",
            "EBIT",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market focuses on upfront automation investment "
            "and underestimates the recurring margin benefit."
        ),

        second_order_effects=[
            "Higher scalability",
            "Reduced labour dependency",
            "Improved consistency",
            "Higher return on capital",
        ],

        disconfirming_evidence=[
            "Automation investment fails to reduce recurring costs",
            "Implementation delays",
            "Quality deteriorates",
            "Maintenance costs offset savings",
        ],

        kill_switch=(
            "Automation fails to generate sustainable recurring "
            "operating-cost savings."
        ),
    ),


    # ======================================================
    # 6. COST-STRUCTURE RESET
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARGIN-COST-STRUCTURE-RESET",
        family=CatalystFamily.MARGIN_EXPANSION,
        name="Cost Structure Reset",

        description=(
            "A durable restructuring of the operating cost base "
            "creates a lower sustainable cost structure."
        ),

        trigger_signals=[
            "restructuring",
            "cost-base reset",
            "organizational simplification",
            "facility consolidation",
            "structural cost reduction",
        ],

        mechanism=(
            "The company permanently removes or redesigns "
            "structural costs through organizational, geographic, "
            "facility, process, or operating-model changes."
        ),

        transmission_channels=[
            "Operating Expenses",
            "Fixed Costs",
            "EBITDA Margin",
            "Free Cash Flow",
        ],

        leading_indicators=[
            "Restructuring announcements",
            "Facility consolidation",
            "Headcount rationalisation",
            "Organizational redesign",
        ],

        confirmation_indicators=[
            "Lower recurring operating expenses",
            "Higher operating margin",
            "Reduced fixed-cost base",
            "Improved cash generation",
        ],

        typical_time_horizon="6-24 months",

        earnings_channels=[
            "EBITDA",
            "EBIT",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market treats restructuring benefits as temporary "
            "and fails to recognize the permanence of the lower "
            "cost base."
        ),

        second_order_effects=[
            "Higher operating leverage",
            "Improved resilience",
            "Higher free cash flow",
            "Improved ROIC",
        ],

        disconfirming_evidence=[
            "Costs return after restructuring",
            "Savings are offset elsewhere",
            "Restructuring disrupts operations",
            "No sustained margin improvement",
        ],

        kill_switch=(
            "The lower cost structure cannot be sustained after "
            "the initial restructuring period."
        ),
    ),
]


__all__ = [
    "MARGIN_PATTERNS",
]