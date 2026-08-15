"""
EIOS
Everest Investment Operating System

Commodity Catalyst Patterns

Purpose:
Defines canonical catalyst patterns beneath the
COMMODITY catalyst family.

This module contains passive data only.
It performs no scoring, ranking, valuation,
classification, or investment decision.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# COMMODITY PATTERNS
# ==========================================================

COMMODITY_PATTERNS = [

    # ------------------------------------------------------
    # 1. COMMODITY PRICE INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMMODITY-PRICE-INFLECTION"
        ),

        family=CatalystFamily.COMMODITY,

        name=(
            "Commodity Price Inflection"
        ),

        description=(
            "A sustained change in the price of a key "
            "commodity materially changes company economics."
        ),

        trigger_signals=[
            "Commodity price moves materially",
            "Supply-demand balance changes",
            "Forward commodity curve changes",
            "Industry commentary confirms price movement",
        ],

        mechanism=(
            "Commodity price change → input/output economics "
            "→ realisation or input-cost change → margins/FCF."
        ),

        transmission_channels=[
            "Realisation",
            "Input Costs",
            "Gross Margin",
            "EBITDA",
            "Free Cash Flow",
        ],

        leading_indicators=[
            "Spot commodity prices",
            "Futures curve",
            "Inventory levels",
            "Production changes",
            "Supply-demand balance",
        ],

        confirmation_indicators=[
            "Company realisations",
            "Gross margin movement",
            "Management commentary",
            "Industry pricing data",
        ],

        typical_time_horizon=(
            "3–18 months"
        ),

        earnings_channels=[
            "Revenue",
            "Realisation",
            "Input Costs",
            "Margins",
            "FCF",
        ],

        market_mistake=(
            "Market extrapolates the previous commodity "
            "price regime instead of recognising a new cycle."
        ),

        second_order_effects=[
            "Capacity response",
            "Inventory gains/losses",
            "Competitor behaviour",
            "Capital expenditure changes",
            "Working-capital changes",
        ],

        disconfirming_evidence=[
            "Commodity price reverses",
            "Supply response is faster than expected",
            "Company does not capture price movement",
        ],

        kill_switch=(
            "The commodity-price change fails to transmit "
            "into company realisations, costs, or cash flow."
        ),
    ),


    # ------------------------------------------------------
    # 2. COMMODITY SUPPLY CONSTRAINT
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMMODITY-SUPPLY-CONSTRAINT"
        ),

        family=CatalystFamily.COMMODITY,

        name=(
            "Commodity Supply Constraint"
        ),

        description=(
            "A structural or cyclical restriction in commodity "
            "supply creates sustained pricing support."
        ),

        trigger_signals=[
            "Production disruptions",
            "Capacity closures",
            "Project delays",
            "Lower industry investment",
            "Supply-side restrictions",
        ],

        mechanism=(
            "Supply constraint → tighter market balance "
            "→ commodity price support → improved economics."
        ),

        transmission_channels=[
            "Commodity Price",
            "Realisation",
            "Margins",
            "FCF",
        ],

        leading_indicators=[
            "Mine/plant closures",
            "Capex reductions",
            "Production guidance cuts",
            "Project delays",
            "Inventory drawdown",
        ],

        confirmation_indicators=[
            "Lower industry supply",
            "Sustained inventory decline",
            "Higher realised prices",
            "Improved company margins",
        ],

        typical_time_horizon=(
            "6–24 months"
        ),

        earnings_channels=[
            "Realisation",
            "Revenue",
            "Margins",
            "FCF",
        ],

        market_mistake=(
            "Market assumes additional supply will arrive "
            "quickly despite structural constraints."
        ),

        second_order_effects=[
            "Higher industry profitability",
            "New capacity incentives",
            "Customer substitution",
            "Competitor investment",
        ],

        disconfirming_evidence=[
            "New capacity arrives early",
            "Demand weakens materially",
            "Inventories rebuild rapidly",
        ],

        kill_switch=(
            "Expected supply tightness disappears because "
            "new supply arrives or demand contracts materially."
        ),
    ),


    # ------------------------------------------------------
    # 3. COMMODITY DEMAND INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMMODITY-DEMAND-INFLECTION"
        ),

        family=CatalystFamily.COMMODITY,

        name=(
            "Commodity Demand Inflection"
        ),

        description=(
            "A structural or cyclical acceleration in commodity "
            "demand materially tightens the market."
        ),

        trigger_signals=[
            "End-market demand acceleration",
            "Industrial production increase",
            "Infrastructure spending",
            "New application demand",
            "Capacity utilisation increase",
        ],

        mechanism=(
            "Demand acceleration → tighter commodity balance "
            "→ price/realisation improvement → earnings impact."
        ),

        transmission_channels=[
            "Demand",
            "Commodity Price",
            "Realisation",
            "Margins",
        ],

        leading_indicators=[
            "Industrial production",
            "Infrastructure activity",
            "Customer orders",
            "Capacity utilisation",
            "Consumption data",
        ],

        confirmation_indicators=[
            "Commodity consumption growth",
            "Higher realised prices",
            "Lower inventories",
            "Improved company revenue",
        ],

        typical_time_horizon=(
            "3–18 months"
        ),

        earnings_channels=[
            "Revenue",
            "Realisation",
            "Margins",
            "FCF",
        ],

        market_mistake=(
            "Market treats demand acceleration as temporary "
            "when it is actually part of a broader structural cycle."
        ),

        second_order_effects=[
            "Capacity additions",
            "Inventory changes",
            "Higher industry utilisation",
            "Supplier bargaining power",
        ],

        disconfirming_evidence=[
            "Demand growth reverses",
            "End-market weakness emerges",
            "Commodity inventories rise materially",
        ],

        kill_switch=(
            "Demand acceleration fails to persist and the "
            "commodity market returns to oversupply."
        ),
    ),


    # ------------------------------------------------------
    # 4. COMMODITY REALISATION INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMMODITY-REALISATION-INFLECTION"
        ),

        family=CatalystFamily.COMMODITY,

        name=(
            "Commodity Realisation Inflection"
        ),

        description=(
            "Company realised commodity prices improve materially "
            "relative to the previous period or benchmark."
        ),

        trigger_signals=[
            "Benchmark price increase",
            "Premium product mix",
            "Improved customer pricing",
            "Higher contract realisations",
        ],

        mechanism=(
            "Benchmark/contract price improvement → "
            "higher company realisation → revenue and margin expansion."
        ),

        transmission_channels=[
            "Realisation",
            "Revenue",
            "Gross Margin",
            "EBITDA",
            "FCF",
        ],

        leading_indicators=[
            "Benchmark prices",
            "Contract pricing",
            "Customer negotiations",
            "Product premium",
        ],

        confirmation_indicators=[
            "Reported realisation",
            "Revenue per unit",
            "Gross margin",
            "EBITDA per unit",
        ],

        typical_time_horizon=(
            "1–12 months"
        ),

        earnings_channels=[
            "Revenue",
            "Realisation",
            "EBITDA",
            "FCF",
        ],

        market_mistake=(
            "Market focuses on volume while underestimating "
            "the earnings impact of higher realisations."
        ),

        second_order_effects=[
            "Operating leverage",
            "Working-capital generation",
            "Debt reduction",
            "Higher ROIC",
        ],

        disconfirming_evidence=[
            "Realisation remains below benchmark",
            "Premium disappears",
            "Customer pricing pressure increases",
        ],

        kill_switch=(
            "Reported realisation fails to improve despite "
            "supportive commodity benchmarks."
        ),
    ),


    # ------------------------------------------------------
    # 5. COMMODITY INVENTORY CYCLE
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMMODITY-INVENTORY-CYCLE"
        ),

        family=CatalystFamily.COMMODITY,

        name=(
            "Commodity Inventory Cycle"
        ),

        description=(
            "A material inventory build or draw changes the "
            "near-term commodity supply-demand balance."
        ),

        trigger_signals=[
            "Inventory drawdown",
            "Inventory build",
            "Warehouse stock changes",
            "Producer inventory changes",
            "Customer destocking/restocking",
        ],

        mechanism=(
            "Inventory change → perceived market tightness/oversupply "
            "→ commodity price response → earnings impact."
        ),

        transmission_channels=[
            "Commodity Price",
            "Realisation",
            "Input Costs",
            "Margins",
        ],

        leading_indicators=[
            "Exchange inventories",
            "Producer inventories",
            "Customer inventories",
            "Import/export data",
        ],

        confirmation_indicators=[
            "Sustained inventory trend",
            "Price response",
            "Company commentary",
            "Industry utilisation",
        ],

        typical_time_horizon=(
            "1–12 months"
        ),

        earnings_channels=[
            "Revenue",
            "Realisation",
            "Input Costs",
            "Margins",
            "FCF",
        ],

        market_mistake=(
            "Market ignores inventory changes until they become "
            "visible through reported earnings."
        ),

        second_order_effects=[
            "Restocking cycle",
            "Destocking cycle",
            "Production response",
            "Working-capital impact",
        ],

        disconfirming_evidence=[
            "Inventory signal reverses",
            "Demand weakens",
            "Supply increases materially",
        ],

        kill_switch=(
            "Inventory movements fail to produce a sustained "
            "change in commodity-market tightness."
        ),
    ),


    # ------------------------------------------------------
    # 6. COMMODITY SPREAD / COST ADVANTAGE
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMMODITY-SPREAD-COST-ADVANTAGE"
        ),

        family=CatalystFamily.COMMODITY,

        name=(
            "Commodity Spread / Cost Advantage"
        ),

        description=(
            "A favourable change between output commodity prices "
            "and input commodity costs creates a structural margin advantage."
        ),

        trigger_signals=[
            "Output-input spread widens",
            "Input commodity prices decline",
            "Output realisation improves",
            "Competitor cost disadvantage increases",
        ],

        mechanism=(
            "Output price minus input cost → wider spread "
            "→ margin expansion → higher FCF and ROIC."
        ),

        transmission_channels=[
            "Gross Margin",
            "EBITDA Margin",
            "FCF",
            "ROIC",
        ],

        leading_indicators=[
            "Input commodity prices",
            "Output commodity prices",
            "Industry spreads",
            "Competitor cost curves",
        ],

        confirmation_indicators=[
            "Reported gross margin",
            "EBITDA margin",
            "Cash conversion",
            "ROIC",
        ],

        typical_time_horizon=(
            "3–18 months"
        ),

        earnings_channels=[
            "Margins",
            "EBITDA",
            "FCF",
            "ROIC",
        ],

        market_mistake=(
            "Market focuses on absolute commodity prices "
            "instead of the spread between output prices and input costs."
        ),

        second_order_effects=[
            "Higher free cash flow",
            "Debt reduction",
            "Capacity expansion",
            "Market-share gains",
            "Higher incremental returns",
        ],

        disconfirming_evidence=[
            "Input costs rise faster than output prices",
            "Spread normalises",
            "Competitors regain cost advantage",
        ],

        kill_switch=(
            "The output-input spread fails to remain favourable "
            "and the expected margin advantage disappears."
        ),
    ),
]


# ==========================================================
# EXPORT
# ==========================================================

__all__ = [
    "COMMODITY_PATTERNS",
]