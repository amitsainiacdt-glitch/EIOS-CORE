"""
EIOS
Everest Investment Operating System

Order / Contract Catalyst Patterns

Purpose:
    Canonical catalyst patterns belonging to the
    ORDER_CONTRACT catalyst family.

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
# ORDER / CONTRACT CATALYST PATTERNS
# ==========================================================

ORDER_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. LARGE ORDER WIN
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-ORDER-LARGE-WIN",
        family=CatalystFamily.ORDER_CONTRACT,
        name="Large Order Win",

        description=(
            "A material contract creates visibility into "
            "future revenue and execution."
        ),

        trigger_signals=[
            "large order",
            "major order win",
            "contract win",
            "order booking",
        ],

        mechanism=(
            "Order acquisition increases backlog and creates "
            "future revenue visibility."
        ),

        transmission_channels=[
            "Order Book",
            "Revenue Visibility",
            "Capacity Utilisation",
        ],

        leading_indicators=[
            "Tender participation",
            "Bid pipeline",
            "Customer discussions",
        ],

        confirmation_indicators=[
            "Order announcement",
            "Backlog growth",
            "Execution milestones",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the duration or "
            "conversion of the order book."
        ),

        second_order_effects=[
            "Capacity expansion",
            "Customer additions",
            "Operating leverage",
        ],

        disconfirming_evidence=[
            "Order cancellation",
            "Execution delays",
            "Margin deterioration",
        ],

        kill_switch=(
            "Material order book fails to convert into "
            "economically attractive revenue."
        ),
    ),

    # ======================================================
    # 2. TENDER WIN
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-ORDER-TENDER-WIN",
        family=CatalystFamily.ORDER_CONTRACT,
        name="Tender Win",

        description=(
            "Successful competitive tender creates a "
            "contractual pipeline for future execution."
        ),

        trigger_signals=[
            "tender win",
            "tender awarded",
            "project awarded",
            "lowest bidder",
            "L1 bidder",
        ],

        mechanism=(
            "Tender success converts bidding activity into "
            "potential contracted revenue."
        ),

        transmission_channels=[
            "Order Book",
            "Revenue Visibility",
            "Market Share",
        ],

        leading_indicators=[
            "Tender pipeline",
            "Bid submission",
            "L1 status",
        ],

        confirmation_indicators=[
            "Letter of award",
            "Contract signing",
            "Work order",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market fails to appreciate the probability "
            "or scale of tender conversion."
        ),

        second_order_effects=[
            "Reference projects",
            "Future tender eligibility",
            "Market-share gains",
        ],

        disconfirming_evidence=[
            "Tender cancellation",
            "Contract dispute",
            "Poor project economics",
        ],

        kill_switch=(
            "Tender win does not convert into an economically "
            "viable executable contract."
        ),
    ),

    # ======================================================
    # 3. MULTI-YEAR CONTRACT
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-ORDER-MULTIYEAR-CONTRACT",
        family=CatalystFamily.ORDER_CONTRACT,
        name="Multi-Year Contract",

        description=(
            "A long-duration customer contract provides "
            "multi-period revenue visibility."
        ),

        trigger_signals=[
            "multi-year contract",
            "long-term contract",
            "long duration agreement",
            "framework contract",
        ],

        mechanism=(
            "Long-duration commitment improves revenue "
            "visibility and can support capacity planning."
        ),

        transmission_channels=[
            "Revenue Visibility",
            "Backlog",
            "Capacity Planning",
        ],

        leading_indicators=[
            "Contract negotiation",
            "Customer qualification",
            "Framework agreement",
        ],

        confirmation_indicators=[
            "Signed contract",
            "Minimum commitment",
            "Scheduled deliveries",
        ],

        typical_time_horizon="12-60 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market values the contract as a one-time "
            "order rather than a multi-period earnings stream."
        ),

        second_order_effects=[
            "Capacity investment",
            "Customer stickiness",
            "Planning efficiency",
        ],

        disconfirming_evidence=[
            "Contract termination",
            "Volume shortfall",
            "Pricing deterioration",
        ],

        kill_switch=(
            "The contractual commitment does not provide "
            "the expected economic revenue visibility."
        ),
    ),

    # ======================================================
    # 4. REPEAT ORDER ACCELERATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-ORDER-REPEAT-ACCELERATION",
        family=CatalystFamily.ORDER_CONTRACT,
        name="Repeat Order Acceleration",

        description=(
            "Existing customers increase order frequency "
            "or order size."
        ),

        trigger_signals=[
            "repeat order",
            "repeat orders",
            "reorder growth",
            "order frequency increase",
        ],

        mechanism=(
            "Increasing repeat demand validates product-market "
            "fit and can accelerate revenue growth."
        ),

        transmission_channels=[
            "Volume",
            "Customer Retention",
            "Revenue Growth",
        ],

        leading_indicators=[
            "Customer enquiries",
            "Repeat quotations",
            "Purchase frequency",
        ],

        confirmation_indicators=[
            "Higher repeat orders",
            "Higher customer revenue",
            "Improved order frequency",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market assumes order growth is temporary "
            "rather than evidence of durable customer demand."
        ),

        second_order_effects=[
            "Customer lifetime value",
            "Cross-selling",
            "Capacity expansion",
        ],

        disconfirming_evidence=[
            "Order frequency reversal",
            "Customer churn",
            "One-off order concentration",
        ],

        kill_switch=(
            "Repeat demand fails to persist across "
            "successive ordering periods."
        ),
    ),

    # ======================================================
    # 5. CUSTOMER QUALIFICATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-ORDER-CUSTOMER-QUALIFICATION",
        family=CatalystFamily.ORDER_CONTRACT,
        name="Customer Qualification",

        description=(
            "A company becomes an approved supplier for a "
            "significant customer or industry."
        ),

        trigger_signals=[
            "customer qualification",
            "approved supplier",
            "vendor qualification",
            "supplier approval",
        ],

        mechanism=(
            "Qualification removes a commercial barrier and "
            "creates access to future customer demand."
        ),

        transmission_channels=[
            "Market Access",
            "Customer Acquisition",
            "Revenue",
        ],

        leading_indicators=[
            "Trial orders",
            "Product testing",
            "Vendor audits",
        ],

        confirmation_indicators=[
            "Qualification approval",
            "Initial commercial order",
            "Repeat orders",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market ignores the option value created "
            "by access to a high-quality customer."
        ),

        second_order_effects=[
            "Reference customer",
            "Additional customer wins",
            "Capacity expansion",
        ],

        disconfirming_evidence=[
            "Qualification failure",
            "No commercial orders",
            "Customer concentration risk",
        ],

        kill_switch=(
            "Qualification fails to generate meaningful "
            "commercial demand within the expected period."
        ),
    ),

    # ======================================================
    # 6. ORDER-BOOK ACCELERATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-ORDER-BOOK-ACCELERATION",
        family=CatalystFamily.ORDER_CONTRACT,
        name="Order-Book Acceleration",

        description=(
            "Order intake grows materially faster than "
            "the existing execution base."
        ),

        trigger_signals=[
            "order book growth",
            "order intake acceleration",
            "backlog acceleration",
            "order inflow growth",
        ],

        mechanism=(
            "Accelerating order intake increases future "
            "revenue visibility and may create operating leverage."
        ),

        transmission_channels=[
            "Order Book",
            "Revenue Visibility",
            "Capacity Utilisation",
            "Operating Leverage",
        ],

        leading_indicators=[
            "Tender pipeline",
            "Customer capex",
            "Order enquiries",
            "Bid activity",
        ],

        confirmation_indicators=[
            "Quarterly order intake",
            "Backlog growth",
            "Book-to-bill improvement",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market extrapolates historical order intake "
            "rather than recognising a new order-cycle inflection."
        ),

        second_order_effects=[
            "Capacity expansion",
            "Hiring",
            "Working-capital investment",
            "Market-share gains",
        ],

        disconfirming_evidence=[
            "Order intake slowdown",
            "Backlog cancellation",
            "Execution bottlenecks",
            "Margin compression",
        ],

        kill_switch=(
            "Order intake fails to remain above the level "
            "required to sustain the expected growth trajectory."
        ),
    ),
]


__all__ = [
    "ORDER_PATTERNS",
]