"""
EIOS
Everest Investment Operating System

Revenue Growth Catalyst Patterns

Purpose:
    Canonical catalyst patterns belonging to the
    REVENUE_GROWTH catalyst family.

Design:
    Passive data definitions only.

    No scoring.
    No ranking.
    No valuation.
    No investment decision.

Pattern Boundary:
    These patterns describe identifiable mechanisms through
    which company revenue can accelerate.

    They do not attempt to replace the more specific
    catalyst families such as:
        - Volume Growth
        - Pricing
        - Customer Addition
        - New Product / Platform
        - Capacity Expansion
"""


from typing import List

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# REVENUE GROWTH CATALYST PATTERNS
# ==========================================================


REVENUE_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. REVENUE ACCELERATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REVENUE-ACCELERATION",
        family=CatalystFamily.REVENUE_GROWTH,
        name="Revenue Growth Acceleration",

        description=(
            "A measurable acceleration in the company's "
            "revenue growth rate creates a positive change "
            "in forward earnings expectations."
        ),

        trigger_signals=[
            "revenue growth acceleration",
            "growth rate inflection",
            "accelerating sales",
            "improving revenue trajectory",
        ],

        mechanism=(
            "A change in underlying business momentum causes "
            "the forward revenue trajectory to rise faster "
            "than previously expected."
        ),

        transmission_channels=[
            "Revenue",
            "Operating Leverage",
            "Earnings Expectations",
            "Valuation Expectations",
        ],

        leading_indicators=[
            "Monthly sales trend",
            "Booking trajectory",
            "Customer activity",
            "Channel throughput",
            "Management growth commentary",
        ],

        confirmation_indicators=[
            "Sequential revenue acceleration",
            "Year-on-year growth acceleration",
            "Improved forward guidance",
            "Higher order conversion",
        ],

        typical_time_horizon="2-12 quarters",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market treats accelerating growth as "
            "temporary or fails to recognize a change in "
            "the underlying growth trajectory."
        ),

        second_order_effects=[
            "Operating leverage",
            "Higher capacity utilisation",
            "Improved return on capital",
            "Higher valuation expectations",
        ],

        disconfirming_evidence=[
            "Growth deceleration",
            "Weakening leading indicators",
            "Customer demand deterioration",
            "Guidance reduction",
        ],

        kill_switch=(
            "Forward revenue indicators fail to confirm "
            "the expected acceleration in growth."
        ),
    ),

    # ======================================================
    # 2. CUSTOMER COHORT RAMP
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REVENUE-CUSTOMER-COHORT-RAMP",
        family=CatalystFamily.REVENUE_GROWTH,
        name="Customer Cohort Revenue Ramp",

        description=(
            "Previously acquired customers move through "
            "a predictable adoption or spending curve, "
            "causing revenue per customer cohort to rise."
        ),

        trigger_signals=[
            "customer ramp",
            "cohort maturation",
            "higher revenue per customer",
            "increasing customer spend",
        ],

        mechanism=(
            "Existing customer cohorts increase their "
            "economic contribution as adoption, usage, "
            "or spending deepens over time."
        ),

        transmission_channels=[
            "Revenue",
            "Customer Lifetime Value",
            "Recurring Revenue",
            "Operating Leverage",
        ],

        leading_indicators=[
            "Customer activation",
            "Usage growth",
            "Repeat purchase behaviour",
            "Revenue per customer",
            "Customer retention",
        ],

        confirmation_indicators=[
            "Higher cohort revenue",
            "Improving net revenue retention",
            "Rising customer lifetime value",
            "Increasing recurring revenue",
        ],

        typical_time_horizon="4-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market values newly acquired customers "
            "at current revenue levels and underestimates "
            "the future contribution of maturing cohorts."
        ),

        second_order_effects=[
            "Higher customer lifetime value",
            "Lower acquisition payback period",
            "Improved operating leverage",
            "Higher recurring revenue mix",
        ],

        disconfirming_evidence=[
            "Cohort revenue stagnation",
            "Customer churn acceleration",
            "Falling usage",
            "Lower repeat purchases",
        ],

        kill_switch=(
            "Maturing customer cohorts fail to generate "
            "the expected increase in economic contribution."
        ),
    ),

    # ======================================================
    # 3. CROSS-SELL REVENUE EXPANSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REVENUE-CROSS-SELL",
        family=CatalystFamily.REVENUE_GROWTH,
        name="Cross-Sell Revenue Expansion",

        description=(
            "An established customer base begins purchasing "
            "additional products or services, increasing "
            "revenue without requiring equivalent customer "
            "acquisition."
        ),

        trigger_signals=[
            "cross-sell opportunity",
            "additional product adoption",
            "multi-product customers",
            "higher wallet share",
        ],

        mechanism=(
            "Existing customer relationships provide a lower-"
            "friction route to additional revenue through "
            "adjacent products or services."
        ),

        transmission_channels=[
            "Revenue",
            "Customer Wallet Share",
            "Customer Lifetime Value",
            "Margin",
        ],

        leading_indicators=[
            "Product penetration",
            "Cross-sell conversion",
            "Multi-product adoption",
            "Salesforce cross-sell activity",
        ],

        confirmation_indicators=[
            "Higher revenue per customer",
            "Increasing multi-product customers",
            "Cross-sell contribution to growth",
            "Higher customer wallet share",
        ],

        typical_time_horizon="2-18 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market values the existing customer base "
            "using current revenue and underestimates the "
            "latent revenue opportunity."
        ),

        second_order_effects=[
            "Higher customer retention",
            "Higher lifetime value",
            "Lower incremental acquisition cost",
            "Improved revenue visibility",
        ],

        disconfirming_evidence=[
            "Low cross-sell conversion",
            "Customer resistance",
            "Product overlap",
            "Declining customer engagement",
        ],

        kill_switch=(
            "Existing customers fail to adopt additional "
            "products at economically attractive rates."
        ),
    ),

    # ======================================================
    # 4. CHANNEL EXPANSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REVENUE-CHANNEL-EXPANSION",
        family=CatalystFamily.REVENUE_GROWTH,
        name="Distribution Channel Expansion",

        description=(
            "Expansion into new distribution channels increases "
            "the company's addressable revenue opportunity."
        ),

        trigger_signals=[
            "new distribution channel",
            "channel partnership",
            "new dealer network",
            "online channel expansion",
            "marketplace expansion",
        ],

        mechanism=(
            "Access to additional distribution infrastructure "
            "increases product availability and customer reach."
        ),

        transmission_channels=[
            "Revenue",
            "Market Reach",
            "Customer Acquisition",
            "Market Share",
        ],

        leading_indicators=[
            "Channel additions",
            "Dealer onboarding",
            "Distribution agreements",
            "Channel inventory",
            "Channel traffic",
        ],

        confirmation_indicators=[
            "Channel revenue growth",
            "Higher geographic reach",
            "Increased sell-through",
            "Improved distribution penetration",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market focuses on the existing distribution "
            "base and fails to recognize the revenue potential "
            "of newly opened channels."
        ),

        second_order_effects=[
            "Customer additions",
            "Market-share gains",
            "Higher asset utilisation",
            "Improved brand visibility",
        ],

        disconfirming_evidence=[
            "Weak channel sell-through",
            "Channel inventory build",
            "Dealer attrition",
            "Low customer conversion",
        ],

        kill_switch=(
            "New distribution channels fail to generate "
            "sustainable incremental revenue."
        ),
    ),

    # ======================================================
    # 5. GEOGRAPHIC REVENUE EXPANSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REVENUE-GEOGRAPHIC-EXPANSION",
        family=CatalystFamily.REVENUE_GROWTH,
        name="Geographic Revenue Expansion",

        description=(
            "Entry into underpenetrated geographic markets "
            "creates an incremental revenue growth runway."
        ),

        trigger_signals=[
            "new geography",
            "regional expansion",
            "international expansion",
            "export market entry",
            "new market launch",
        ],

        mechanism=(
            "The company replicates an established business "
            "model in a new geographic market where customer "
            "penetration remains low."
        ),

        transmission_channels=[
            "Revenue",
            "TAM",
            "Market Share",
            "Operating Leverage",
        ],

        leading_indicators=[
            "New market launches",
            "Local distribution additions",
            "Regional customer wins",
            "Export enquiries",
            "International partnerships",
        ],

        confirmation_indicators=[
            "Geographic revenue growth",
            "New-market customer additions",
            "Increasing export contribution",
            "Regional market-share gains",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market extrapolates historical geographic "
            "penetration and underestimates the runway available "
            "from new territories."
        ),

        second_order_effects=[
            "TAM expansion",
            "Higher capacity utilisation",
            "Brand strengthening",
            "Operating leverage",
        ],

        disconfirming_evidence=[
            "Weak market acceptance",
            "Regulatory barriers",
            "Distribution failure",
            "Unattractive unit economics",
        ],

        kill_switch=(
            "New geographic markets fail to achieve "
            "economically viable customer adoption."
        ),
    ),

    # ======================================================
    # 6. RECURRING REVENUE MIX SHIFT
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REVENUE-RECURRING-MIX",
        family=CatalystFamily.REVENUE_GROWTH,
        name="Recurring Revenue Mix Expansion",

        description=(
            "A rising proportion of recurring or contracted "
            "revenue improves revenue visibility and creates "
            "a more durable growth trajectory."
        ),

        trigger_signals=[
            "recurring revenue growth",
            "subscription growth",
            "annuity revenue",
            "contracted revenue",
            "renewal revenue",
        ],

        mechanism=(
            "Migration toward recurring revenue increases "
            "the predictability and durability of future "
            "revenue generation."
        ),

        transmission_channels=[
            "Revenue Visibility",
            "Recurring Revenue",
            "Customer Retention",
            "Valuation Expectations",
        ],

        leading_indicators=[
            "Annual recurring revenue",
            "Renewal rates",
            "Subscription additions",
            "Contract duration",
            "Retention metrics",
        ],

        confirmation_indicators=[
            "Recurring revenue growth",
            "Higher recurring revenue mix",
            "Improved renewal rates",
            "Higher contracted backlog",
        ],

        typical_time_horizon="4-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market focuses on current revenue growth "
            "rather than recognizing the improvement in "
            "future revenue visibility and quality."
        ),

        second_order_effects=[
            "Lower revenue volatility",
            "Higher customer retention",
            "Improved cash-flow visibility",
            "Potential valuation re-rating",
        ],

        disconfirming_evidence=[
            "Renewal deterioration",
            "Higher churn",
            "Contract cancellations",
            "Declining recurring revenue",
        ],

        kill_switch=(
            "Recurring revenue growth fails to produce "
            "the expected improvement in durability and visibility."
        ),
    ),
]


__all__ = [
    "REVENUE_PATTERNS",
]