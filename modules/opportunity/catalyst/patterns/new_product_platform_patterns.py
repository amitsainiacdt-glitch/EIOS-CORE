"""
EIOS
Everest Investment Operating System

New Product / Platform Catalyst Patterns

Purpose:
Canonical catalyst patterns for new product and platform
launches that can create incremental economic value.

Architecture:

    Catalyst Taxonomy
            ↓
    New Product / Platform Patterns
            ↓
    Catalyst Pattern Registry
            ↓
    Opportunity Engine

Design Principles:

- Patterns are evidence-driven.
- Patterns contain no scoring logic.
- Patterns contain no valuation logic.
- Patterns contain no company-specific assumptions.
- Each pattern has explicit confirmation and
  disconfirming evidence.
"""


from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# CANONICAL PATTERNS
# ==========================================================

NEW_PRODUCT_PLATFORM_PATTERNS = [

    CatalystPattern(
        pattern_id=(
            "PAT-NEW-PRODUCT-PLATFORM-LAUNCH"
        ),
        name=(
            "New Product Launch"
        ),
        description=(
            "A newly launched product creates a "
            "potentially material incremental revenue "
            "stream."
        ),
        mechanism=(
            "Product launch → customer adoption → "
            "incremental revenue → earnings contribution."
        ),
        trigger_signals=[
            "Commercial product launch",
            "Production readiness",
            "Initial customer availability",
        ],
        leading_indicators=[
            "Customer enquiries",
            "Qualification activity",
            "Initial trials",
            "Distributor stocking",
        ],
        confirmation_indicators=[
            "Initial orders",
            "Bookings",
            "Revenue contribution",
            "Repeat customer demand",
        ],
        earnings_channels=[
            "Revenue",
            "Gross Margin",
            "Operating Profit",
        ],
        market_mistake=(
            "Market assumes the new product will remain "
            "immaterial despite early commercial traction."
        ),
        disconfirming_evidence=[
            "Weak customer interest",
            "Delayed commercialisation",
            "Low initial orders",
            "Product quality issues",
        ],
        kill_switch=(
            "The product fails to achieve meaningful "
            "commercial customer adoption."
        ),
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-NEW-PRODUCT-PLATFORM-CUSTOMER-QUALIFICATION"
        ),
        name=(
            "Customer Qualification Inflection"
        ),
        description=(
            "Successful qualification by important customers "
            "converts a product from development status into "
            "a commercially addressable opportunity."
        ),
        mechanism=(
            "Customer qualification → approved supplier status "
            "→ purchase eligibility → order potential."
        ),
        trigger_signals=[
            "Qualification completion",
            "Approved vendor status",
            "Customer certification",
        ],
        leading_indicators=[
            "Testing completion",
            "Technical approval",
            "Pilot acceptance",
            "Supplier onboarding",
        ],
        confirmation_indicators=[
            "Commercial orders",
            "Production schedules",
            "Repeat orders",
            "Multiple customer qualifications",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Capacity Utilisation",
        ],
        market_mistake=(
            "Market treats qualification as administrative "
            "rather than as a gateway to future commercial volumes."
        ),
        disconfirming_evidence=[
            "Qualification failure",
            "Customer delays",
            "No commercial conversion",
            "Competitive replacement",
        ],
        kill_switch=(
            "Customer qualification does not convert into "
            "commercial purchasing activity."
        ),
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-NEW-PRODUCT-PLATFORM-BOOKINGS-INFLECTION"
        ),
        name=(
            "New Product Bookings Inflection"
        ),
        description=(
            "Bookings for a new product accelerate before "
            "reported revenue fully reflects adoption."
        ),
        mechanism=(
            "Bookings acceleration → order conversion → "
            "revenue recognition → earnings growth."
        ),
        trigger_signals=[
            "New product bookings",
            "Purchase commitments",
            "Customer order acceleration",
        ],
        leading_indicators=[
            "Bookings growth",
            "Pipeline growth",
            "Order conversion",
            "Customer commitments",
        ],
        confirmation_indicators=[
            "Order backlog",
            "Revenue conversion",
            "Shipment growth",
            "Repeat bookings",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Operating Leverage",
        ],
        market_mistake=(
            "Market focuses on current reported revenue and "
            "underestimates the forward earnings embedded in bookings."
        ),
        disconfirming_evidence=[
            "Booking cancellations",
            "Weak conversion",
            "Customer deferrals",
            "Declining pipeline",
        ],
        kill_switch=(
            "New product bookings fail to convert into "
            "sustainable shipments and revenue."
        ),
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-NEW-PRODUCT-PLATFORM-REPEAT-ORDER"
        ),
        name=(
            "Repeat Order Validation"
        ),
        description=(
            "Repeat purchases demonstrate that initial product "
            "adoption is becoming durable customer behaviour."
        ),
        mechanism=(
            "Initial adoption → successful customer experience "
            "→ repeat purchase → recurring product economics."
        ),
        trigger_signals=[
            "Second purchase",
            "Repeat customer orders",
            "Expansion within existing accounts",
        ],
        leading_indicators=[
            "Customer reorder intent",
            "Usage expansion",
            "Account penetration",
            "Customer feedback",
        ],
        confirmation_indicators=[
            "Repeat orders",
            "Higher order frequency",
            "Larger order sizes",
            "Additional customer sites",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Customer Lifetime Value",
        ],
        market_mistake=(
            "Market assumes initial product sales are one-off "
            "rather than evidence of repeatable demand."
        ),
        disconfirming_evidence=[
            "No repeat purchases",
            "Customer dissatisfaction",
            "Declining order frequency",
            "Single-customer dependence",
        ],
        kill_switch=(
            "Initial customers fail to reorder at commercially "
            "meaningful rates."
        ),
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-NEW-PRODUCT-PLATFORM-MARGIN-MIX"
        ),
        name=(
            "New Product Margin Mix Inflection"
        ),
        description=(
            "A new product carries superior economics and "
            "increases the company's aggregate margin profile "
            "as adoption scales."
        ),
        mechanism=(
            "Higher-value product mix → gross margin expansion "
            "→ operating profit growth → improved returns."
        ),
        trigger_signals=[
            "Premium product launch",
            "Higher realised pricing",
            "Improved gross margin",
        ],
        leading_indicators=[
            "Product mix improvement",
            "Customer willingness to pay",
            "Unit economics",
            "Contribution margin",
        ],
        confirmation_indicators=[
            "Gross margin expansion",
            "EBIT margin improvement",
            "Higher contribution per unit",
            "Increasing product mix share",
        ],
        earnings_channels=[
            "Gross Margin",
            "EBIT Margin",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market focuses on revenue growth while "
            "underestimating the margin contribution of the new product."
        ),
        disconfirming_evidence=[
            "Margin below expectations",
            "High launch costs",
            "Price discounting",
            "Poor product mix",
        ],
        kill_switch=(
            "The new product fails to generate superior unit "
            "economics as volumes scale."
        ),
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-NEW-PRODUCT-PLATFORM-PLATFORM-ADOPTION"
        ),
        name=(
            "Platform Adoption Inflection"
        ),
        description=(
            "A product platform expands beyond the initial "
            "offering and creates multiple future revenue opportunities."
        ),
        mechanism=(
            "Platform adoption → additional applications/products "
            "→ broader customer base → expanding TAM."
        ),
        trigger_signals=[
            "Platform deployment",
            "Multiple product applications",
            "New customer segments",
        ],
        leading_indicators=[
            "Application pipeline",
            "Customer expansion",
            "New use cases",
            "Cross-selling opportunities",
        ],
        confirmation_indicators=[
            "Multiple products launched",
            "New customer categories",
            "Cross-sell revenue",
            "Platform-based recurring demand",
        ],
        earnings_channels=[
            "Revenue",
            "TAM",
            "Gross Margin",
            "ROIIC",
        ],
        market_mistake=(
            "Market values the platform based only on its initial "
            "product rather than its expanding application opportunity."
        ),
        disconfirming_evidence=[
            "Limited applications",
            "Weak customer expansion",
            "Platform concentration",
            "Technology displacement",
        ],
        kill_switch=(
            "The platform fails to expand beyond its initial "
            "commercial application."
        ),
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
    ),
]


# ==========================================================
# EXPORT
# ==========================================================

__all__ = [
    "NEW_PRODUCT_PLATFORM_PATTERNS",
]