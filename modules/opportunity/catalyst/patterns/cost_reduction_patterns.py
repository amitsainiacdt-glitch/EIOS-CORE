"""
EIOS
Everest Investment Operating System

Cost Reduction Catalyst Patterns

Purpose:
Defines canonical catalyst patterns for the
Cost Reduction catalyst family.

This module contains passive data definitions only.
It performs no scoring, ranking, valuation,
classification, or investment decision.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


COST_REDUCTION_PATTERNS = [

    CatalystPattern(
        pattern_id="PAT-COST-REDUCTION-INPUT-COST-DECLINE",
        family=CatalystFamily.COST_REDUCTION,
        name="Input Cost Decline",
        description=(
            "Sustainable reduction in the cost of key "
            "raw materials, components, energy, or other "
            "critical inputs."
        ),
        trigger_signals=[
            "Commodity price decline",
            "Supplier price reduction",
            "Lower energy cost",
            "Procurement renegotiation",
        ],
        mechanism=(
            "Lower input cost → lower unit cost → "
            "margin expansion → higher earnings."
        ),
        transmission_channels=[
            "Gross margin",
            "EBITDA margin",
            "Operating cash flow",
        ],
        leading_indicators=[
            "Commodity prices",
            "Supplier quotations",
            "Input inventory costs",
            "Procurement commentary",
        ],
        confirmation_indicators=[
            "Gross margin expansion",
            "Lower cost of goods sold",
            "Improved EBITDA margin",
        ],
        typical_time_horizon="1-6 quarters",
        earnings_channels=[
            "Gross profit",
            "EBITDA",
            "PAT",
            "Free cash flow",
        ],
        market_mistake=(
            "Market assumes input-cost pressure is persistent "
            "and underestimates the speed or durability of "
            "cost normalization."
        ),
        second_order_effects=[
            "Higher cash generation",
            "Improved competitive pricing flexibility",
            "Greater reinvestment capacity",
        ],
        disconfirming_evidence=[
            "Input prices reverse upward",
            "Supplier pricing remains elevated",
            "Gross margin fails to improve",
        ],
        kill_switch=(
            "Sustained input-cost inflation prevents the "
            "expected margin improvement."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-COST-REDUCTION-PROCUREMENT-EFFICIENCY",
        family=CatalystFamily.COST_REDUCTION,
        name="Procurement Efficiency",
        description=(
            "Improvement in procurement practices, supplier "
            "terms, sourcing, or purchasing scale that "
            "structurally lowers input costs."
        ),
        trigger_signals=[
            "Supplier consolidation",
            "Volume-based negotiations",
            "Strategic sourcing",
            "Vendor renegotiation",
        ],
        mechanism=(
            "Better procurement terms → lower purchase cost → "
            "lower unit economics → margin improvement."
        ),
        transmission_channels=[
            "COGS",
            "Gross margin",
            "EBITDA",
        ],
        leading_indicators=[
            "New supplier contracts",
            "Vendor consolidation",
            "Procurement savings targets",
            "Purchase price variance",
        ],
        confirmation_indicators=[
            "Lower procurement cost",
            "Gross margin improvement",
            "Reported procurement savings",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "Gross profit",
            "EBITDA",
            "PAT",
            "Free cash flow",
        ],
        market_mistake=(
            "Market treats procurement savings as temporary "
            "rather than recognizing them as structural "
            "operating improvements."
        ),
        second_order_effects=[
            "Improved supplier bargaining power",
            "Higher operating resilience",
            "Greater reinvestment capacity",
        ],
        disconfirming_evidence=[
            "Savings fail to materialize",
            "Supplier costs remain unchanged",
            "Procurement benefits are offset elsewhere",
        ],
        kill_switch=(
            "Expected procurement savings fail to translate "
            "into sustainable unit-cost reduction."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-COST-REDUCTION-AUTOMATION",
        family=CatalystFamily.COST_REDUCTION,
        name="Automation-Driven Cost Reduction",
        description=(
            "Automation or process digitisation reduces "
            "labour, processing, error, or operating costs."
        ),
        trigger_signals=[
            "Automation deployment",
            "Digital workflow adoption",
            "Robotics installation",
            "Process digitisation",
        ],
        mechanism=(
            "Automation → lower labour or processing cost → "
            "higher productivity → margin expansion."
        ),
        transmission_channels=[
            "Employee cost",
            "Operating expenses",
            "EBITDA margin",
            "ROIC",
        ],
        leading_indicators=[
            "Automation investment",
            "Headcount productivity",
            "Output per employee",
            "Process-cycle reduction",
        ],
        confirmation_indicators=[
            "Lower cost per unit",
            "Higher output per employee",
            "Operating margin expansion",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "EBITDA",
            "PAT",
            "Free cash flow",
        ],
        market_mistake=(
            "Market focuses on the upfront automation investment "
            "and underestimates the recurring operating-cost benefit."
        ),
        second_order_effects=[
            "Higher productivity",
            "Lower dependence on labour availability",
            "Improved scalability",
        ],
        disconfirming_evidence=[
            "Automation fails to improve productivity",
            "Operating costs do not decline",
            "Implementation costs remain excessive",
        ],
        kill_switch=(
            "Automation fails to produce measurable recurring "
            "unit-cost or productivity improvement."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-COST-REDUCTION-OPERATING-EFFICIENCY",
        family=CatalystFamily.COST_REDUCTION,
        name="Operating Efficiency Improvement",
        description=(
            "Structural improvement in business processes, "
            "facility utilisation, logistics, or overhead "
            "management reduces operating costs."
        ),
        trigger_signals=[
            "Process redesign",
            "Facility consolidation",
            "Logistics optimisation",
            "Overhead reduction",
        ],
        mechanism=(
            "Operating efficiency → lower cost base → "
            "higher operating margin → stronger cash flow."
        ),
        transmission_channels=[
            "Operating expenses",
            "EBITDA margin",
            "Free cash flow",
        ],
        leading_indicators=[
            "Cost-saving programmes",
            "Facility consolidation",
            "Logistics cost per unit",
            "Employee productivity",
        ],
        confirmation_indicators=[
            "Lower operating expense ratio",
            "Higher EBITDA margin",
            "Improved cash conversion",
        ],
        typical_time_horizon="2-6 quarters",
        earnings_channels=[
            "EBITDA",
            "PAT",
            "Free cash flow",
        ],
        market_mistake=(
            "Market assumes the existing cost structure is fixed "
            "and underestimates management's ability to remove "
            "structural inefficiencies."
        ),
        second_order_effects=[
            "Higher operating resilience",
            "Better asset utilisation",
            "Improved return on capital",
        ],
        disconfirming_evidence=[
            "Cost ratios remain unchanged",
            "Savings are one-off",
            "Operational efficiency does not improve",
        ],
        kill_switch=(
            "Operating efficiency initiatives fail to create "
            "recurring cost reduction."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-COST-REDUCTION-MIX-AND-SOURCING",
        family=CatalystFamily.COST_REDUCTION,
        name="Sourcing and Manufacturing Mix Optimisation",
        description=(
            "Changes in sourcing geography, manufacturing mix, "
            "plant allocation, or production configuration "
            "reduce structural unit costs."
        ),
        trigger_signals=[
            "Production relocation",
            "Low-cost sourcing",
            "Plant optimisation",
            "Manufacturing mix change",
        ],
        mechanism=(
            "Optimised sourcing or production mix → lower "
            "structural unit cost → margin improvement."
        ),
        transmission_channels=[
            "COGS",
            "Gross margin",
            "EBITDA",
            "Working capital",
        ],
        leading_indicators=[
            "New sourcing arrangements",
            "Plant utilisation changes",
            "Production allocation",
            "Import/export mix",
        ],
        confirmation_indicators=[
            "Lower manufacturing cost",
            "Improved gross margin",
            "Improved working-capital efficiency",
        ],
        typical_time_horizon="2-10 quarters",
        earnings_channels=[
            "Gross profit",
            "EBITDA",
            "PAT",
            "Free cash flow",
        ],
        market_mistake=(
            "Market focuses on reported production volumes while "
            "missing the structural improvement in unit economics."
        ),
        second_order_effects=[
            "Improved cost competitiveness",
            "Higher plant utilisation",
            "Better capital efficiency",
        ],
        disconfirming_evidence=[
            "Unit cost does not decline",
            "New sourcing introduces quality problems",
            "Plant utilisation deteriorates",
        ],
        kill_switch=(
            "Sourcing or manufacturing optimisation fails to "
            "produce sustainable unit-cost improvement."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-COST-REDUCTION-HEADCOUNT-PRODUCTIVITY",
        family=CatalystFamily.COST_REDUCTION,
        name="Headcount Productivity Improvement",
        description=(
            "Higher output or revenue generated per employee "
            "reduces the labour cost intensity of the business."
        ),
        trigger_signals=[
            "Revenue per employee improvement",
            "Output per employee improvement",
            "Workforce optimisation",
            "Hiring discipline",
        ],
        mechanism=(
            "Higher employee productivity → lower labour cost "
            "per unit of output → operating margin expansion."
        ),
        transmission_channels=[
            "Employee cost",
            "Revenue per employee",
            "EBITDA margin",
            "Operating leverage",
        ],
        leading_indicators=[
            "Revenue per employee",
            "Output per employee",
            "Headcount growth versus revenue growth",
            "Productivity initiatives",
        ],
        confirmation_indicators=[
            "Lower employee-cost ratio",
            "Higher revenue per employee",
            "EBITDA margin expansion",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "EBITDA",
            "PAT",
            "Free cash flow",
        ],
        market_mistake=(
            "Market assumes employee costs must grow broadly "
            "with revenue and misses productivity-driven "
            "operating leverage."
        ),
        second_order_effects=[
            "Higher operating leverage",
            "Improved scalability",
            "Stronger return on incremental capital",
        ],
        disconfirming_evidence=[
            "Headcount grows faster than revenue",
            "Revenue per employee deteriorates",
            "Employee costs remain structurally elevated",
        ],
        kill_switch=(
            "Employee productivity fails to improve enough to "
            "create measurable labour-cost leverage."
        ),
    ),
]


__all__ = [
    "COST_REDUCTION_PATTERNS",
]