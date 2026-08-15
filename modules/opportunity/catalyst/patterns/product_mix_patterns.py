"""
EIOS
Everest Investment Operating System

Product Mix Catalyst Patterns

Passive definitions only.
No scoring.
No ranking.
No valuation.
No investment decision logic.
"""

from typing import List

from modules.opportunity.catalyst.catalyst_patterns import CatalystPattern
from modules.opportunity.catalyst.catalyst_taxonomy import CatalystFamily


PRODUCT_MIX_PATTERNS: List[CatalystPattern] = [

    CatalystPattern(
        pattern_id="PAT-PRODUCT-MIX-PREMIUM-TIER-MIGRATION",
        family=CatalystFamily.PRODUCT_MIX,
        name="Premium Tier Migration",
        description=(
            "Customers migrate from lower-value products toward "
            "premium or higher-value products within the portfolio."
        ),
        trigger_signals=[
            "premium product demand acceleration",
            "higher-value SKU migration",
            "premium segment share increase",
        ],
        mechanism=(
            "Customer preference shifts toward higher-value products, "
            "changing the composition of products sold."
        ),
        transmission_channels=[
            "Product Mix",
            "Revenue Composition",
            "Gross Margin",
        ],
        leading_indicators=[
            "premium SKU enquiries",
            "premium product bookings",
            "premium order mix",
        ],
        confirmation_indicators=[
            "premium revenue share",
            "higher-value SKU contribution",
            "sustained premiumisation",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "Revenue per unit",
            "Gross Profit",
            "EBITDA",
            "EPS",
        ],
        market_mistake=(
            "The market focuses on aggregate volume or revenue and "
            "underestimates the effect of premiumisation."
        ),
        second_order_effects=[
            "higher customer lifetime value",
            "stronger brand positioning",
            "greater reinvestment capacity",
        ],
        disconfirming_evidence=[
            "premium share fails to increase",
            "premium demand proves temporary",
            "premium products lack superior economics",
        ],
        kill_switch=(
            "Premium products fail to achieve a sustained increase "
            "in portfolio mix."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-PRODUCT-MIX-CATEGORY-MIGRATION",
        family=CatalystFamily.PRODUCT_MIX,
        name="Product Category Migration",
        description=(
            "Revenue composition shifts from weaker product categories "
            "toward structurally more attractive categories."
        ),
        trigger_signals=[
            "strategic category growth",
            "weak category decline",
            "customer preference migration",
            "category demand divergence",
        ],
        mechanism=(
            "Demand migrates between categories, changing the composition "
            "of sales toward more attractive products."
        ),
        transmission_channels=[
            "Category Mix",
            "Revenue Composition",
            "Gross Margin",
            "Capital Efficiency",
        ],
        leading_indicators=[
            "category order trends",
            "channel sell-through",
            "category enquiries",
            "category market-share movement",
        ],
        confirmation_indicators=[
            "category revenue mix",
            "category contribution margins",
            "sustained category migration",
        ],
        typical_time_horizon="2-12 quarters",
        earnings_channels=[
            "Revenue Quality",
            "Gross Margin",
            "EBITDA",
            "ROCE",
        ],
        market_mistake=(
            "The market evaluates aggregate growth and misses "
            "a structural improvement in revenue composition."
        ),
        second_order_effects=[
            "longer growth runway",
            "better capital allocation",
            "lower exposure to weak categories",
        ],
        disconfirming_evidence=[
            "category migration reverses",
            "higher-value category fails to scale",
            "category economics are not superior",
        ],
        kill_switch=(
            "Category migration fails to persist across multiple periods."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-PRODUCT-MIX-NEW-PRODUCT-INFLECTION",
        family=CatalystFamily.PRODUCT_MIX,
        name="New Product Mix Inflection",
        description=(
            "A newly introduced product becomes material enough to "
            "change the company's product revenue composition."
        ),
        trigger_signals=[
            "new product launch",
            "customer qualification",
            "initial commercial orders",
            "repeat orders",
        ],
        mechanism=(
            "A new product moves from initial adoption to material "
            "commercial contribution."
        ),
        transmission_channels=[
            "New Product Revenue",
            "Product Mix",
            "Gross Margin",
        ],
        leading_indicators=[
            "customer qualifications",
            "pilot conversions",
            "bookings",
            "initial repeat orders",
        ],
        confirmation_indicators=[
            "material revenue contribution",
            "repeat customer adoption",
            "increasing product-family share",
        ],
        typical_time_horizon="3-12 quarters",
        earnings_channels=[
            "Revenue",
            "Gross Margin",
            "EBITDA",
            "EPS",
        ],
        market_mistake=(
            "The market treats the new product as immaterial and "
            "underestimates its potential mix contribution."
        ),
        second_order_effects=[
            "new customer acquisition",
            "adjacent product opportunities",
            "longer growth runway",
        ],
        disconfirming_evidence=[
            "weak customer adoption",
            "low repeat orders",
            "product economics disappoint",
            "revenue remains immaterial",
        ],
        kill_switch=(
            "The new product fails to achieve sustained commercial adoption."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-PRODUCT-MIX-PRODUCT-RATIONALISATION",
        family=CatalystFamily.PRODUCT_MIX,
        name="Product Rationalisation",
        description=(
            "The company reduces low-value or strategically unattractive "
            "products, improving the composition of the remaining portfolio."
        ),
        trigger_signals=[
            "SKU rationalisation",
            "product discontinuation",
            "portfolio simplification",
            "core-product focus",
        ],
        mechanism=(
            "Low-quality products are removed or deprioritised, causing "
            "the remaining sales mix to become more attractive."
        ),
        transmission_channels=[
            "SKU Mix",
            "Gross Margin",
            "Working Capital",
            "ROCE",
        ],
        leading_indicators=[
            "SKU reductions",
            "product discontinuations",
            "inventory rationalisation",
            "portfolio focus changes",
        ],
        confirmation_indicators=[
            "lower low-margin contribution",
            "improved product margins",
            "better inventory turns",
            "higher portfolio profitability",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "Gross Margin",
            "EBITDA",
            "Working Capital",
            "FCF",
        ],
        market_mistake=(
            "The market interprets declining low-quality product sales "
            "as weak growth rather than portfolio improvement."
        ),
        second_order_effects=[
            "lower working-capital intensity",
            "simpler operations",
            "better capital allocation",
        ],
        disconfirming_evidence=[
            "rationalisation fails to improve economics",
            "customers are lost without replacement",
            "portfolio profitability does not improve",
        ],
        kill_switch=(
            "Rationalisation produces no sustainable improvement "
            "in portfolio economics."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-PRODUCT-MIX-SOLUTION-BUNDLE-MIGRATION",
        family=CatalystFamily.PRODUCT_MIX,
        name="Solution Bundle Mix Migration",
        description=(
            "Customers migrate from individual products toward "
            "integrated solutions, bundles, or multi-product configurations."
        ),
        trigger_signals=[
            "bundle adoption",
            "cross-selling acceleration",
            "multi-product penetration",
            "integrated solution demand",
        ],
        mechanism=(
            "Customers increasingly purchase combinations of products, "
            "changing portfolio composition and value per relationship."
        ),
        transmission_channels=[
            "Average Transaction Value",
            "Product Mix",
            "Customer Retention",
            "Gross Margin",
        ],
        leading_indicators=[
            "bundle enquiries",
            "cross-sell rate",
            "multi-product customers",
            "average order configuration",
        ],
        confirmation_indicators=[
            "bundle revenue share",
            "revenue per customer",
            "repeat purchase rates",
            "customer retention",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "Revenue per Customer",
            "Gross Margin",
            "Recurring Revenue",
            "EPS",
        ],
        market_mistake=(
            "The market evaluates individual products separately and "
            "misses the benefit of increasing solution penetration."
        ),
        second_order_effects=[
            "higher switching costs",
            "greater customer lifetime value",
            "lower customer acquisition cost",
        ],
        disconfirming_evidence=[
            "bundle adoption stagnates",
            "cross-selling fails",
            "customers prefer standalone products",
            "bundle economics are not superior",
        ],
        kill_switch=(
            "Integrated solution penetration fails to increase "
            "despite adequate product availability."
        ),
    ),

    CatalystPattern(
        pattern_id="PAT-PRODUCT-MIX-WINNER-CONCENTRATION",
        family=CatalystFamily.PRODUCT_MIX,
        name="Product Winner Concentration",
        description=(
            "One or more economically superior products gain a "
            "disproportionately larger share of the portfolio."
        ),
        trigger_signals=[
            "strategic product outperformance",
            "portfolio share gain",
            "repeat orders for winning products",
            "customer concentration around winners",
        ],
        mechanism=(
            "A superior product family gains disproportionate portfolio "
            "share, increasing the weight of superior economics."
        ),
        transmission_channels=[
            "Product Mix",
            "Revenue Concentration",
            "Gross Margin",
            "Capital Allocation",
        ],
        leading_indicators=[
            "product-level order growth",
            "repeat purchase rates",
            "customer adoption",
            "capacity allocation",
        ],
        confirmation_indicators=[
            "increasing winner revenue share",
            "higher portfolio margin",
            "sustained customer retention",
            "increased production allocation",
        ],
        typical_time_horizon="3-12 quarters",
        earnings_channels=[
            "Revenue",
            "Gross Margin",
            "EBITDA",
            "ROCE",
        ],
        market_mistake=(
            "The market treats product-level outperformance as temporary "
            "rather than recognising a durable portfolio shift."
        ),
        second_order_effects=[
            "capacity reallocation",
            "R&D concentration",
            "stronger competitive position",
            "improved incremental returns",
        ],
        disconfirming_evidence=[
            "product winner loses momentum",
            "competitive substitution",
            "capacity prevents scaling",
            "superior economics fail to persist",
        ],
        kill_switch=(
            "The leading product fails to sustain its portfolio share "
            "gain or loses its economic advantage."
        ),
    ),
]


__all__ = [
    "PRODUCT_MIX_PATTERNS",
]
