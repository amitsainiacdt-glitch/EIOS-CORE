"""
EIOS
Everest Investment Operating System

Pricing Catalyst Patterns

Purpose:
Canonical catalyst patterns belonging to the
PRICING catalyst family.

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
# PRICING CATALYST PATTERNS
# ==========================================================


PRICING_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. PRICING REALIZATION IMPROVEMENT
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-PRICING-REALIZATION",
        family=CatalystFamily.PRICING,
        name="Pricing Realization Improvement",

        description=(
            "Improvement in realized selling prices as the "
            "company captures a greater portion of its "
            "nominal or quoted pricing."
        ),

        trigger_signals=[
            "higher realized price",
            "improved price realization",
            "better net pricing",
            "lower commercial leakage",
        ],

        mechanism=(
            "Improved commercial discipline, contract terms, "
            "customer segmentation, or reduced leakage increases "
            "the effective price received per unit."
        ),

        transmission_channels=[
            "Realized Price",
            "Revenue",
            "Gross Margin",
            "EBITDA",
        ],

        leading_indicators=[
            "Quotation discipline",
            "Lower discounting",
            "Improved contract terms",
            "Reduced rebates",
        ],

        confirmation_indicators=[
            "Higher realized price per unit",
            "Improved net pricing",
            "Stable or improving volumes",
            "Revenue growth above volume growth",
        ],

        typical_time_horizon="3-18 months",

        earnings_channels=[
            "Revenue",
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market treats pricing improvement as temporary "
            "or fails to recognize the durability of improved "
            "realized prices."
        ),

        second_order_effects=[
            "Margin expansion",
            "Improved cash generation",
            "Higher return on incremental capital",
        ],

        disconfirming_evidence=[
            "Realized prices fail to improve",
            "Discounting increases",
            "Customer resistance",
            "Volume deterioration caused by pricing actions",
        ],

        kill_switch=(
            "Improved headline pricing fails to translate into "
            "sustained higher realized economic price."
        ),
    ),


    # ======================================================
    # 2. LIST PRICE INCREASE
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-PRICING-LIST-PRICE-INCREASE",
        family=CatalystFamily.PRICING,
        name="List Price Increase",

        description=(
            "A formal increase in the company's published or "
            "contractual base prices creates higher revenue per unit."
        ),

        trigger_signals=[
            "price increase",
            "list price revision",
            "price hike",
            "new pricing schedule",
        ],

        mechanism=(
            "The company raises the nominal price charged for "
            "existing products or services."
        ),

        transmission_channels=[
            "Average Selling Price",
            "Revenue",
            "Gross Margin",
            "EBITDA",
        ],

        leading_indicators=[
            "Pricing announcements",
            "Contract renewal discussions",
            "Customer notifications",
            "Competitor pricing actions",
        ],

        confirmation_indicators=[
            "Higher invoice prices",
            "Higher average selling price",
            "Revenue growth ahead of volume growth",
            "Stable customer retention",
        ],

        typical_time_horizon="1-12 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the percentage of the "
            "price increase that will stick or the duration of "
            "the higher pricing."
        ),

        second_order_effects=[
            "Margin expansion",
            "Industry price reset",
            "Higher reinvestment capacity",
        ],

        disconfirming_evidence=[
            "Price increase withdrawn",
            "Heavy customer pushback",
            "Material volume loss",
            "Competitor price undercutting",
        ],

        kill_switch=(
            "The announced price increase fails to persist in "
            "actual realized customer pricing."
        ),
    ),


    # ======================================================
    # 3. COST PASS-THROUGH
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-PRICING-PASS-THROUGH",
        family=CatalystFamily.PRICING,
        name="Cost Pass-Through",

        description=(
            "The company successfully transfers higher input or "
            "operating costs to customers through pricing."
        ),

        trigger_signals=[
            "cost pass-through",
            "raw material price increase",
            "input cost recovery",
            "fuel surcharge",
            "contractual escalation",
        ],

        mechanism=(
            "Customer pricing is adjusted sufficiently to offset "
            "higher input costs, protecting unit economics."
        ),

        transmission_channels=[
            "Realized Price",
            "Gross Margin",
            "EBITDA",
            "Cash Flow",
        ],

        leading_indicators=[
            "Input-cost inflation",
            "Contract escalation clauses",
            "Customer price negotiations",
            "Industry pricing announcements",
        ],

        confirmation_indicators=[
            "Price increase tracks input-cost increase",
            "Gross margin stability",
            "Improved price-cost spread",
            "Successful contract renewals",
        ],

        typical_time_horizon="3-18 months",

        earnings_channels=[
            "Revenue",
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market assumes input-cost inflation will permanently "
            "compress margins despite evidence of successful pass-through."
        ),

        second_order_effects=[
            "Margin protection",
            "Improved cash conversion",
            "Stronger customer contract discipline",
        ],

        disconfirming_evidence=[
            "Input costs rise faster than prices",
            "Delayed pass-through",
            "Customer resistance",
            "Gross margin compression",
        ],

        kill_switch=(
            "The company cannot recover a material portion of "
            "structural input-cost increases through customer pricing."
        ),
    ),


    # ======================================================
    # 4. PREMIUM PRICING ADOPTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-PRICING-PREMIUM-ADOPTION",
        family=CatalystFamily.PRICING,
        name="Premium Pricing Adoption",

        description=(
            "Customers increasingly accept higher-priced versions, "
            "service tiers, specifications, or configurations."
        ),

        trigger_signals=[
            "premium product adoption",
            "higher-tier adoption",
            "premium pricing",
            "customer upgrade",
            "premiumization",
        ],

        mechanism=(
            "Customers demonstrate willingness to pay more for "
            "superior performance, reliability, service, or features."
        ),

        transmission_channels=[
            "Average Selling Price",
            "Revenue",
            "Gross Margin",
            "Customer Value",
        ],

        leading_indicators=[
            "Premium product inquiries",
            "Upgrade rates",
            "Premium order pipeline",
            "Customer willingness-to-pay evidence",
        ],

        confirmation_indicators=[
            "Premium product share increases",
            "Higher average selling price",
            "Stable premium-product retention",
            "Improved gross margin",
        ],

        typical_time_horizon="6-24 months",

        earnings_channels=[
            "Revenue",
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market attributes higher realization solely to "
            "product mix and misses the underlying increase in "
            "customer willingness to pay."
        ),

        second_order_effects=[
            "Brand strengthening",
            "Higher customer lifetime value",
            "Improved reinvestment economics",
        ],

        disconfirming_evidence=[
            "Premium adoption stalls",
            "Customers trade down",
            "Premium discounting increases",
            "No improvement in realized pricing",
        ],

        kill_switch=(
            "Premium adoption fails to produce a durable increase "
            "in realized price and economic value."
        ),
    ),


    # ======================================================
    # 5. DISCOUNT REDUCTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-PRICING-DISCOUNT-REDUCTION",
        family=CatalystFamily.PRICING,
        name="Discount Reduction",

        description=(
            "Reduction in discounts, rebates, incentives, or "
            "commercial concessions increases the net realized price."
        ),

        trigger_signals=[
            "lower discounts",
            "rebate reduction",
            "incentive reduction",
            "commercial discipline",
            "reduced promotional pricing",
        ],

        mechanism=(
            "The company reduces unnecessary commercial concessions "
            "while retaining sufficient customer demand."
        ),

        transmission_channels=[
            "Net Realized Price",
            "Revenue",
            "Gross Margin",
            "EBITDA",
        ],

        leading_indicators=[
            "Lower promotional intensity",
            "Reduced rebates",
            "Improved sales discipline",
            "Customer retention despite lower concessions",
        ],

        confirmation_indicators=[
            "Higher net realization",
            "Stable volume",
            "Improved gross margin",
            "Lower discount-to-sales ratio",
        ],

        typical_time_horizon="3-12 months",

        earnings_channels=[
            "Revenue",
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market focuses on headline list prices and misses "
            "the earnings impact of reduced commercial leakage."
        ),

        second_order_effects=[
            "Better sales discipline",
            "Higher customer quality",
            "Improved cash generation",
        ],

        disconfirming_evidence=[
            "Volume falls materially",
            "Discounts return",
            "Competitors increase incentives",
            "Net realization does not improve",
        ],

        kill_switch=(
            "Discount reduction cannot be sustained without "
            "materially damaging customer demand."
        ),
    ),


    # ======================================================
    # 6. VALUE-BASED PRICING
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-PRICING-VALUE-BASED",
        family=CatalystFamily.PRICING,
        name="Value-Based Pricing",

        description=(
            "The company captures a higher price because customers "
            "recognize greater economic value from its product or service."
        ),

        trigger_signals=[
            "value-based pricing",
            "willingness to pay",
            "customer ROI improvement",
            "pricing power",
            "value capture",
        ],

        mechanism=(
            "Improved customer economics or differentiated value "
            "allows the company to capture a larger share of the "
            "economic value created."
        ),

        transmission_channels=[
            "Realized Price",
            "Customer ROI",
            "Revenue",
            "Margin",
            "Cash Flow",
        ],

        leading_indicators=[
            "Customer ROI evidence",
            "Reduced price sensitivity",
            "Successful price negotiations",
            "Competitive differentiation",
        ],

        confirmation_indicators=[
            "Higher realized pricing",
            "Low customer churn",
            "Sustained price increases",
            "Stable or improving demand",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "Gross Profit",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market values the business using historical pricing "
            "and fails to recognize an emerging structural increase "
            "in willingness to pay."
        ),

        second_order_effects=[
            "Stronger competitive moat",
            "Higher ROIIC",
            "Greater reinvestment capacity",
            "Higher customer lifetime value",
        ],

        disconfirming_evidence=[
            "Customer price sensitivity increases",
            "Competitors replicate the offering",
            "Price increases cause demand destruction",
            "Customer ROI does not support higher pricing",
        ],

        kill_switch=(
            "The company cannot sustainably capture additional "
            "customer value through higher realized pricing."
        ),
    ),
]


__all__ = [
    "PRICING_PATTERNS",
]