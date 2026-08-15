"""
EIOS
Everest Investment Operating System

TAM Expansion Catalyst Patterns

Purpose:
Canonical catalyst patterns for expansion of the
Total Addressable Market.

Family:
CatalystFamily.TAM_EXPANSION

Design Principles:

- Six canonical patterns
- Evidence-driven
- Passive data definitions
- No scoring
- No ranking
- No valuation
- No company-specific logic
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


TAM_EXPANSION_PATTERNS = [

    # ======================================================
    # 1. NEW APPLICATION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-TAM-EXPANSION-NEW-APPLICATION"
        ),
        family=CatalystFamily.TAM_EXPANSION,
        name=(
            "New Application TAM Expansion"
        ),
        description=(
            "A company enters a new application or use case "
            "that materially expands the addressable market."
        ),
        trigger_signals=[
            "New application identified",
            "New use case development",
            "Customer trials",
            "Application-specific demand",
        ],
        mechanism=(
            "New application → incremental demand pool → "
            "larger TAM → longer growth runway."
        ),
        transmission_channels=[
            "New application",
            "Customer adoption",
            "Market expansion",
            "Revenue growth",
        ],
        leading_indicators=[
            "Pilot projects",
            "Customer enquiries",
            "Design wins",
            "Qualification activity",
        ],
        confirmation_indicators=[
            "Commercial adoption",
            "Repeat orders",
            "Revenue contribution",
            "Application expansion",
        ],
        typical_time_horizon=(
            "12-36 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        market_mistake=(
            "Market continues valuing the company using "
            "the legacy application market size."
        ),
        second_order_effects=[
            "Higher reinvestment runway",
            "Longer growth duration",
            "Potential operating leverage",
        ],
        disconfirming_evidence=[
            "Customer adoption fails",
            "Application economics remain unattractive",
            "Trials do not convert commercially",
        ],
        kill_switch=(
            "New application fails to develop or "
            "commercial adoption remains negligible."
        ),
    ),

    # ======================================================
    # 2. GEOGRAPHIC EXPANSION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-TAM-EXPANSION-GEOGRAPHIC"
        ),
        family=CatalystFamily.TAM_EXPANSION,
        name=(
            "Geographic TAM Expansion"
        ),
        description=(
            "Expansion into new geographies materially "
            "increases the company's addressable market."
        ),
        trigger_signals=[
            "Entry into new geography",
            "New regional approvals",
            "Distributor appointment",
            "Local customer development",
        ],
        mechanism=(
            "New geography → incremental customer pool → "
            "larger TAM → additional growth runway."
        ),
        transmission_channels=[
            "Geographic expansion",
            "Customer acquisition",
            "Market penetration",
            "Revenue growth",
        ],
        leading_indicators=[
            "Regional qualification",
            "Distributor onboarding",
            "Customer enquiries",
            "Initial bookings",
        ],
        confirmation_indicators=[
            "Commercial sales",
            "Repeat regional orders",
            "Regional revenue growth",
            "Increasing customer penetration",
        ],
        typical_time_horizon=(
            "12-36 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        market_mistake=(
            "Market values the business primarily on "
            "its existing geographic footprint."
        ),
        second_order_effects=[
            "Diversification of revenue",
            "Higher addressable market",
            "Longer growth runway",
        ],
        disconfirming_evidence=[
            "Weak regional demand",
            "Regulatory barriers",
            "Poor unit economics",
        ],
        kill_switch=(
            "Geographic expansion fails commercially "
            "or the target market does not develop."
        ),
    ),

    # ======================================================
    # 3. NEW CUSTOMER CLASS
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-TAM-EXPANSION-NEW-CUSTOMER-CLASS"
        ),
        family=CatalystFamily.TAM_EXPANSION,
        name=(
            "New Customer Class TAM Expansion"
        ),
        description=(
            "A previously unserved customer class becomes "
            "addressable and creates incremental demand."
        ),
        trigger_signals=[
            "New customer segment identified",
            "Product qualification",
            "Customer trials",
            "Segment-specific demand",
        ],
        mechanism=(
            "New customer class → incremental demand pool → "
            "larger TAM → broader growth opportunity."
        ),
        transmission_channels=[
            "Customer expansion",
            "Market segmentation",
            "Product adoption",
            "Revenue growth",
        ],
        leading_indicators=[
            "Pilot programmes",
            "Customer qualification",
            "Initial enquiries",
            "Design wins",
        ],
        confirmation_indicators=[
            "Commercial orders",
            "Repeat purchases",
            "Segment revenue growth",
            "Customer expansion",
        ],
        typical_time_horizon=(
            "12-36 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        market_mistake=(
            "Market assumes the historical customer base "
            "represents the company's maximum opportunity."
        ),
        second_order_effects=[
            "Broader customer diversification",
            "Higher utilization of existing capabilities",
            "Longer growth duration",
        ],
        disconfirming_evidence=[
            "Customer class fails to adopt",
            "Product economics unsuitable",
            "Qualification does not convert",
        ],
        kill_switch=(
            "New customer class fails to develop "
            "or commercial adoption remains negligible."
        ),
    ),

    # ======================================================
    # 4. MARKET PENETRATION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-TAM-EXPANSION-MARKET-PENETRATION"
        ),
        family=CatalystFamily.TAM_EXPANSION,
        name=(
            "Market Penetration TAM Expansion"
        ),
        description=(
            "A previously low-penetration market develops "
            "toward substantially higher adoption."
        ),
        trigger_signals=[
            "Low existing penetration",
            "Adoption barriers declining",
            "Customer awareness increasing",
            "Infrastructure development",
        ],
        mechanism=(
            "Low penetration → adoption increases → "
            "effective market expands → sustained growth runway."
        ),
        transmission_channels=[
            "Market adoption",
            "Penetration increase",
            "Demand growth",
            "Revenue growth",
        ],
        leading_indicators=[
            "Customer enquiries",
            "Pilot deployments",
            "Capacity additions",
            "Increasing adoption rates",
        ],
        confirmation_indicators=[
            "Accelerating customer additions",
            "Higher penetration",
            "Repeat demand",
            "Sustained volume growth",
        ],
        typical_time_horizon=(
            "12-48 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        market_mistake=(
            "Market extrapolates historical low penetration "
            "and underestimates the achievable market size."
        ),
        second_order_effects=[
            "Operating leverage",
            "Higher capacity utilization",
            "Longer duration of growth",
        ],
        disconfirming_evidence=[
            "Adoption remains stagnant",
            "Structural barriers persist",
            "Customer economics remain unattractive",
        ],
        kill_switch=(
            "Market penetration fails to increase "
            "or the adoption curve structurally stalls."
        ),
    ),

    # ======================================================
    # 5. MARKET REASSESSMENT
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-TAM-EXPANSION-MARKET-REASSESSMENT"
        ),
        family=CatalystFamily.TAM_EXPANSION,
        name=(
            "TAM Reassessment"
        ),
        description=(
            "New evidence demonstrates that the addressable "
            "market is materially larger than previously understood."
        ),
        trigger_signals=[
            "New market study",
            "Industry data revision",
            "Customer surveys",
            "New demand evidence",
        ],
        mechanism=(
            "New evidence → revised market opportunity → "
            "larger TAM → higher long-term growth expectations."
        ),
        transmission_channels=[
            "Market intelligence",
            "Expectation revision",
            "Growth estimates",
            "Valuation expectations",
        ],
        leading_indicators=[
            "Third-party market research",
            "Industry forecasts",
            "Customer adoption data",
            "Application data",
        ],
        confirmation_indicators=[
            "Actual demand exceeds prior expectations",
            "Market growth outperforms estimates",
            "Company expands addressable opportunity",
            "Revenue opportunity increases",
        ],
        typical_time_horizon=(
            "6-24 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        market_mistake=(
            "Market anchors valuation to an outdated "
            "estimate of the addressable market."
        ),
        second_order_effects=[
            "Higher long-term growth expectations",
            "Longer duration assumptions",
            "Potential valuation re-rating",
        ],
        disconfirming_evidence=[
            "Market study proves unreliable",
            "Demand remains below revised estimates",
            "TAM expansion is theoretical only",
        ],
        kill_switch=(
            "Revised TAM fails to translate into actual "
            "demand or the underlying evidence is invalidated."
        ),
    ),

    # ======================================================
    # 6. PLATFORM / ADJACENCY
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-TAM-EXPANSION-PLATFORM-ADJACENCY"
        ),
        family=CatalystFamily.TAM_EXPANSION,
        name=(
            "Platform Adjacency TAM Expansion"
        ),
        description=(
            "Existing capabilities allow the company to "
            "address adjacent markets without rebuilding "
            "its business model from scratch."
        ),
        trigger_signals=[
            "Adjacent market opportunity",
            "Existing technology applicability",
            "Customer overlap",
            "Capability reuse",
        ],
        mechanism=(
            "Existing capability → adjacent application → "
            "incremental TAM → broader growth runway."
        ),
        transmission_channels=[
            "Capability reuse",
            "Cross-selling",
            "Adjacent market entry",
            "Revenue growth",
        ],
        leading_indicators=[
            "Adjacent product development",
            "Customer trials",
            "Cross-selling",
            "New application qualification",
        ],
        confirmation_indicators=[
            "Adjacent-market revenue",
            "Repeat orders",
            "Cross-selling success",
            "Increasing addressable opportunity",
        ],
        typical_time_horizon=(
            "12-36 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        market_mistake=(
            "Market values the company only on its existing "
            "core market and ignores adjacent opportunities."
        ),
        second_order_effects=[
            "Higher asset utilization",
            "Lower incremental entry costs",
            "Longer growth runway",
        ],
        disconfirming_evidence=[
            "Capabilities do not transfer",
            "Adjacent market economics are weak",
            "Customer overlap is limited",
        ],
        kill_switch=(
            "Adjacency fails commercially or capability "
            "reuse does not create economic value."
        ),
    ),
]


__all__ = [
    "TAM_EXPANSION_PATTERNS",
]