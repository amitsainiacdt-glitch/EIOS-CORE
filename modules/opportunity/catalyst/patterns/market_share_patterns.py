"""
EIOS
Everest Investment Operating System

Market Share Catalyst Patterns

Purpose:
Canonical catalyst pattern definitions for situations where
a company gains market share within an existing market.

Design Principles:

- Definitions only.
- No scoring.
- No valuation.
- No ranking.
- No company-specific logic.
- No investment decision logic.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


MARKET_SHARE_PATTERNS = [

    # ======================================================
    # 1. ORGANIC MARKET-SHARE GAIN
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-SHARE-ORGANIC-SHARE-GAIN",
        family=CatalystFamily.MARKET_SHARE,
        name="Organic Market-Share Gain",

        description=(
            "The company consistently gains share within an "
            "existing market through superior execution, product "
            "competitiveness, distribution, or customer preference."
        ),

        trigger_signals=[
            "market-share gain",
            "share gains",
            "competitive win rate",
            "customer preference improvement",
            "competitor share loss",
        ],

        mechanism=(
            "Competitive advantage and superior execution "
            "increase customer wins relative to competitors, "
            "causing the company to capture a larger portion "
            "of existing market demand."
        ),

        transmission_channels=[
            "Market Share",
            "Volume",
            "Revenue",
            "Operating Leverage",
        ],

        leading_indicators=[
            "Customer win rate",
            "Order conversion",
            "New customer additions",
            "Dealer or distribution additions",
            "Competitor share loss",
        ],

        confirmation_indicators=[
            "Reported market-share increase",
            "Volume growth above industry growth",
            "Revenue growth above industry growth",
            "Higher customer retention",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "ROIC",
            "FCF",
        ],

        market_mistake=(
            "The market attributes growth primarily to industry "
            "expansion and underestimates the contribution from "
            "company-specific share gains."
        ),

        second_order_effects=[
            "Higher operating leverage",
            "Improved competitive position",
            "Greater customer scale",
            "Higher bargaining power",
        ],

        disconfirming_evidence=[
            "Market-share decline",
            "Volume growth below industry growth",
            "Customer losses",
            "Competitive win rate deterioration",
        ],

        kill_switch=(
            "The company fails to sustain or demonstrate measurable "
            "market-share gains despite continued industry demand."
        ),
    ),

    # ======================================================
    # 2. COMPETITOR SHARE CAPTURE
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-SHARE-COMPETITOR-SHARE-CAPTURE",
        family=CatalystFamily.MARKET_SHARE,
        name="Competitor Share Capture",

        description=(
            "The company captures customers and volume from "
            "specific competitors whose products, execution, "
            "capacity, or economics have weakened."
        ),

        trigger_signals=[
            "competitor weakness",
            "competitor capacity disruption",
            "competitor service deterioration",
            "competitor product issues",
            "customer migration",
        ],

        mechanism=(
            "A competitor becomes less competitive, allowing "
            "the company to win displaced customers and convert "
            "competitor volume into incremental market share."
        ),

        transmission_channels=[
            "Competitor Share",
            "Customer Wins",
            "Volume",
            "Revenue",
        ],

        leading_indicators=[
            "Competitor capacity reduction",
            "Competitor delivery delays",
            "Customer enquiries",
            "Higher conversion rates",
            "Customer migration activity",
        ],

        confirmation_indicators=[
            "New customer wins from competitors",
            "Incremental volume",
            "Share gains in affected segments",
            "Higher utilisation",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market treats competitor weakness as temporary "
            "and fails to recognize the permanence of customer "
            "migration and newly captured share."
        ),

        second_order_effects=[
            "Customer retention",
            "Higher utilisation",
            "Improved scale economics",
            "Stronger competitive position",
        ],

        disconfirming_evidence=[
            "Competitor recovery",
            "Customer reversals",
            "Low customer retention",
            "No measurable incremental volume",
        ],

        kill_switch=(
            "Captured customers do not remain with the company "
            "or competitor weakness fails to translate into "
            "sustainable incremental share."
        ),
    ),

    # ======================================================
    # 3. DISTRIBUTION-LED SHARE GAIN
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-SHARE-DISTRIBUTION-LED-GAIN",
        family=CatalystFamily.MARKET_SHARE,
        name="Distribution-Led Share Gain",

        description=(
            "Expansion or improvement of the company's distribution "
            "network increases product availability and enables "
            "market-share gains."
        ),

        trigger_signals=[
            "distribution expansion",
            "dealer additions",
            "channel expansion",
            "geographic distribution expansion",
            "retail penetration",
        ],

        mechanism=(
            "Broader and more effective distribution increases "
            "product availability and customer reach, allowing "
            "the company to capture demand that was previously "
            "served by competitors or remained inaccessible."
        ),

        transmission_channels=[
            "Distribution Reach",
            "Customer Acquisition",
            "Market Share",
            "Revenue",
        ],

        leading_indicators=[
            "Dealer onboarding",
            "Distributor additions",
            "New geographic coverage",
            "Channel productivity",
            "Retail availability",
        ],

        confirmation_indicators=[
            "Higher sell-through",
            "Regional share gains",
            "Higher channel revenue",
            "Increasing customer additions",
        ],

        typical_time_horizon="6-30 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market focuses on the existing distribution base "
            "and underestimates the economic impact of improved "
            "availability and incremental geographic reach."
        ),

        second_order_effects=[
            "Higher brand visibility",
            "Customer additions",
            "Improved fixed-cost absorption",
            "Higher channel bargaining power",
        ],

        disconfirming_evidence=[
            "Weak sell-through",
            "Dealer attrition",
            "Channel inventory build",
            "Low conversion of new outlets",
        ],

        kill_switch=(
            "Distribution expansion fails to produce sustainable "
            "incremental sell-through or market-share gains."
        ),
    ),

    # ======================================================
    # 4. PRODUCT-LED SHARE GAIN
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-SHARE-PRODUCT-LED-GAIN",
        family=CatalystFamily.MARKET_SHARE,
        name="Product-Led Share Gain",

        description=(
            "A superior or newly differentiated product enables "
            "the company to win customers and gain share within "
            "an established market."
        ),

        trigger_signals=[
            "new product launch",
            "product superiority",
            "feature advantage",
            "performance improvement",
            "customer adoption",
        ],

        mechanism=(
            "Product differentiation improves customer preference "
            "and conversion, allowing the company to win share "
            "without relying solely on overall industry growth."
        ),

        transmission_channels=[
            "Product Competitiveness",
            "Customer Wins",
            "Market Share",
            "Volume",
        ],

        leading_indicators=[
            "Product qualification",
            "Customer trials",
            "Design wins",
            "New product enquiries",
            "Higher conversion rates",
        ],

        confirmation_indicators=[
            "Product adoption",
            "Incremental customer wins",
            "Volume growth above industry",
            "Market-share increase",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "ROIC",
        ],

        market_mistake=(
            "The market focuses on the current revenue contribution "
            "of the product and underestimates the share-gain runway "
            "created by superior product economics."
        ),

        second_order_effects=[
            "Customer retention",
            "Pricing power",
            "Product mix improvement",
            "Higher return on incremental capital",
        ],

        disconfirming_evidence=[
            "Weak customer adoption",
            "Competitive product response",
            "Low conversion",
            "Product differentiation erosion",
        ],

        kill_switch=(
            "The product fails to generate sustained customer "
            "preference or measurable market-share gains."
        ),
    ),

    # ======================================================
    # 5. CAPACITY-CONSTRAINED SHARE GAIN
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-SHARE-CAPACITY-CONSTRAINED-GAIN",
        family=CatalystFamily.MARKET_SHARE,
        name="Capacity-Constrained Share Gain",

        description=(
            "The company gains or is positioned to gain market share "
            "because competitors cannot supply sufficient capacity "
            "to meet market demand."
        ),

        trigger_signals=[
            "industry capacity shortage",
            "competitor capacity constraints",
            "supply shortage",
            "customer allocation",
            "long delivery lead times",
        ],

        mechanism=(
            "Limited industry supply creates an opportunity for "
            "companies with available or expandable capacity to "
            "capture unmet demand and increase market share."
        ),

        transmission_channels=[
            "Capacity",
            "Volume",
            "Market Share",
            "Utilisation",
            "Pricing",
        ],

        leading_indicators=[
            "Competitor utilisation",
            "Industry lead times",
            "Customer allocation requests",
            "Capacity expansion",
            "Order backlog",
        ],

        confirmation_indicators=[
            "Higher utilisation",
            "Incremental customer wins",
            "Volume growth above industry",
            "Market-share gains",
            "Order backlog growth",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "ROIC",
            "FCF",
        ],

        market_mistake=(
            "The market treats supply constraints as a broad "
            "industry phenomenon and fails to identify which "
            "companies can convert scarcity into durable share gains."
        ),

        second_order_effects=[
            "Higher utilisation",
            "Operating leverage",
            "Pricing power",
            "Customer lock-in",
        ],

        disconfirming_evidence=[
            "Industry capacity expansion",
            "Demand deterioration",
            "Competitor supply recovery",
            "Utilisation decline",
        ],

        kill_switch=(
            "Supply scarcity disappears before the company converts "
            "the opportunity into durable market-share gains."
        ),
    ),

    # ======================================================
    # 6. SHARE-GAIN COMPOUNDING
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-SHARE-SHARE-GAIN-COMPOUNDING",
        family=CatalystFamily.MARKET_SHARE,
        name="Share-Gain Compounding",

        description=(
            "Initial market-share gains create reinforcing economic "
            "advantages that allow the company to continue gaining "
            "share over multiple periods."
        ),

        trigger_signals=[
            "sustained share gains",
            "scale advantage",
            "customer retention improvement",
            "network effects",
            "cost advantage",
        ],

        mechanism=(
            "Initial share gains increase scale, customer density, "
            "brand strength, operating efficiency, or purchasing "
            "power, which strengthens competitiveness and enables "
            "further share gains."
        ),

        transmission_channels=[
            "Market Share",
            "Scale",
            "Operating Efficiency",
            "Customer Retention",
            "ROIC",
        ],

        leading_indicators=[
            "Sequential share gains",
            "Improving unit economics",
            "Customer retention",
            "Increasing scale",
            "Improving cost position",
        ],

        confirmation_indicators=[
            "Multi-period share gains",
            "Higher ROIC",
            "Improved margins",
            "Lower customer acquisition cost",
            "Increasing competitive advantage",
        ],

        typical_time_horizon="12-60 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "ROIC",
            "FCF",
        ],

        market_mistake=(
            "The market views individual share gains as isolated "
            "events and fails to recognize the reinforcing feedback "
            "loop between scale, competitiveness, and further share gains."
        ),

        second_order_effects=[
            "Operating leverage",
            "Higher ROIC",
            "Improved pricing power",
            "Stronger competitive moat",
            "Higher customer retention",
        ],

        disconfirming_evidence=[
            "Share gains reverse",
            "Scale economics fail to improve",
            "ROIC stagnates",
            "Customer retention deteriorates",
            "Competitive advantage weakens",
        ],

        kill_switch=(
            "Market-share gains fail to create improving economic "
            "advantages and the expected reinforcing feedback loop "
            "does not emerge."
        ),
    ),
]


__all__ = [
    "MARKET_SHARE_PATTERNS",
]