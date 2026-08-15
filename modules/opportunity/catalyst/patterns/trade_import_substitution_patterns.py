"""
EIOS
Everest Investment Operating System

Trade / Import Substitution Catalyst Patterns

Purpose:
    Canonical catalyst patterns for the
    Trade / Import Substitution catalyst family.

Design Principles:
    - Pattern definitions only.
    - No scoring.
    - No ranking.
    - No valuation.
    - No company-specific analysis.
    - Evidence must be independently observable.
    - Every pattern contains explicit invalidation logic.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# FAMILY
# ==========================================================

FAMILY = CatalystFamily.TRADE_IMPORT_SUBSTITUTION


# ==========================================================
# PATTERN 1
# ==========================================================

IMPORT_REPLACEMENT = CatalystPattern(
    pattern_id=(
        "PAT-TRADE-IMPORT-SUBSTITUTION-IMPORT-REPLACEMENT"
    ),
    family=FAMILY,
    name="Import Replacement",
    description=(
        "Domestic producers gain share as imported products "
        "are replaced by locally manufactured alternatives."
    ),
    trigger_signals=[
        "Import volumes decline",
        "Domestic order enquiries increase",
        "Customers qualify domestic suppliers",
        "Import lead times or availability deteriorate",
    ],
    mechanism=(
        "Import dependence -> domestic substitution -> "
        "volume/share gain -> revenue and operating leverage."
    ),
    transmission_channels=[
        "Volume",
        "Market Share",
        "Capacity Utilisation",
        "Operating Leverage",
    ],
    leading_indicators=[
        "Import shipment data",
        "Domestic capacity additions",
        "Customer qualification activity",
        "Domestic order book",
    ],
    confirmation_indicators=[
        "Domestic market share gains",
        "Revenue growth above industry growth",
        "Higher domestic utilisation",
        "Repeat customer orders",
    ],
    typical_time_horizon="1-3 years",
    earnings_channels=[
        "Revenue Growth",
        "EBITDA",
        "PAT",
        "Free Cash Flow",
    ],
    market_mistake=(
        "Market treats import substitution as a temporary "
        "trade-flow change rather than a durable customer "
        "qualification and localisation shift."
    ),
    second_order_effects=[
        "Higher domestic utilisation",
        "Supplier ecosystem development",
        "Lower customer switching risk",
        "Greater pricing power after qualification",
    ],
    disconfirming_evidence=[
        "Imports recover without domestic share loss",
        "Domestic products fail qualification",
        "Customer localisation plans are cancelled",
        "Domestic capacity remains uneconomic",
    ],
    kill_switch=[
        "Persistent loss of domestic market share",
        "Structural cost disadvantage",
        "Material quality failure",
        "Customer migration back to imports",
    ],
)


# ==========================================================
# PATTERN 2
# ==========================================================

DOMESTIC_CAPACITY = CatalystPattern(
    pattern_id=(
        "PAT-TRADE-IMPORT-SUBSTITUTION-DOMESTIC-CAPACITY"
    ),
    family=FAMILY,
    name="Domestic Capacity Build-Out",
    description=(
        "New domestic manufacturing capacity enables "
        "previously import-dependent demand to be served locally."
    ),
    trigger_signals=[
        "New plant commissioning",
        "Capacity expansion announcements",
        "Domestic supplier qualification",
        "Import substitution contracts",
    ],
    mechanism=(
        "Capacity creation -> local supply availability -> "
        "customer conversion -> domestic volume growth."
    ),
    transmission_channels=[
        "Capacity",
        "Volume",
        "Market Share",
        "Operating Leverage",
    ],
    leading_indicators=[
        "Capex progress",
        "Capacity commissioning dates",
        "Customer qualification pipeline",
        "Domestic order enquiries",
    ],
    confirmation_indicators=[
        "Commercial production",
        "Utilisation ramp",
        "Revenue contribution",
        "Customer additions",
    ],
    typical_time_horizon="2-4 years",
    earnings_channels=[
        "Revenue Growth",
        "EBITDA Margin",
        "PAT",
        "Free Cash Flow",
    ],
    market_mistake=(
        "Market focuses on near-term capex dilution and "
        "underestimates the earnings ramp from replacing imports."
    ),
    second_order_effects=[
        "Higher domestic supplier density",
        "Lower import dependence",
        "Customer ecosystem localisation",
        "Follow-on capacity expansion",
    ],
    disconfirming_evidence=[
        "Capacity ramp delays",
        "Weak customer qualification",
        "Low utilisation",
        "Import competition remains structurally cheaper",
    ],
    kill_switch=[
        "Material commissioning failure",
        "Persistent underutilisation",
        "Failed customer qualification",
        "Economics below cost of imported supply",
    ],
)


# ==========================================================
# PATTERN 3
# ==========================================================

TARIFF_ADVANTAGE = CatalystPattern(
    pattern_id=(
        "PAT-TRADE-IMPORT-SUBSTITUTION-TARIFF-ADVANTAGE"
    ),
    family=FAMILY,
    name="Tariff Advantage",
    description=(
        "Trade-policy changes improve the relative economics "
        "of domestic production versus imported products."
    ),
    trigger_signals=[
        "Import duty increase",
        "Anti-dumping measures",
        "Trade restrictions",
        "Customs policy changes",
    ],
    mechanism=(
        "Tariff/barrier change -> imported cost increases -> "
        "domestic relative competitiveness improves."
    ),
    transmission_channels=[
        "Pricing",
        "Market Share",
        "Volume",
        "Margins",
    ],
    leading_indicators=[
        "Government notifications",
        "Import duty changes",
        "Import landed-cost changes",
        "Trade-flow shifts",
    ],
    confirmation_indicators=[
        "Domestic price competitiveness improves",
        "Import volumes decline",
        "Domestic orders increase",
        "Domestic market share rises",
    ],
    typical_time_horizon="6-24 months",
    earnings_channels=[
        "Revenue",
        "EBITDA",
        "PAT",
        "Free Cash Flow",
    ],
    market_mistake=(
        "Market assumes tariff protection immediately flows "
        "through to earnings without considering duration, "
        "pass-through and competitive response."
    ),
    second_order_effects=[
        "Domestic capacity investment",
        "Supplier localisation",
        "Higher customer qualification",
        "Industry consolidation",
    ],
    disconfirming_evidence=[
        "Tariff reversal",
        "Importers absorb the cost",
        "Alternative source countries emerge",
        "Domestic producers fail to capture share",
    ],
    kill_switch=[
        "Policy reversal",
        "Trade diversion eliminates advantage",
        "Domestic economics remain uncompetitive",
        "Demand destruction",
    ],
)


# ==========================================================
# PATTERN 4
# ==========================================================

LOCALISATION = CatalystPattern(
    pattern_id=(
        "PAT-TRADE-IMPORT-SUBSTITUTION-LOCALISATION"
    ),
    family=FAMILY,
    name="Supply Chain Localisation",
    description=(
        "Customers deliberately increase domestic sourcing "
        "to reduce dependence on overseas suppliers."
    ),
    trigger_signals=[
        "Customer localisation programmes",
        "Dual-sourcing initiatives",
        "Domestic vendor qualification",
        "Supply-chain diversification",
    ],
    mechanism=(
        "Supply-chain risk -> sourcing diversification -> "
        "domestic qualification -> recurring local demand."
    ),
    transmission_channels=[
        "Customer Addition",
        "Volume",
        "Market Share",
        "Revenue Visibility",
    ],
    leading_indicators=[
        "Vendor audits",
        "Qualification activity",
        "Trial orders",
        "Customer capex localisation",
    ],
    confirmation_indicators=[
        "Recurring domestic orders",
        "Higher domestic sourcing share",
        "Long-term supply agreements",
        "Customer additions",
    ],
    typical_time_horizon="1-4 years",
    earnings_channels=[
        "Revenue Growth",
        "EBITDA",
        "PAT",
        "Free Cash Flow",
    ],
    market_mistake=(
        "Market interprets localisation as temporary risk "
        "mitigation rather than a structural sourcing change."
    ),
    second_order_effects=[
        "Longer customer relationships",
        "Higher switching costs",
        "Domestic supplier ecosystem growth",
        "Follow-on product localisation",
    ],
    disconfirming_evidence=[
        "Customers abandon localisation programmes",
        "Domestic suppliers fail quality requirements",
        "Imports regain cost advantage",
        "No conversion from trials to recurring orders",
    ],
    kill_switch=[
        "Customer programme cancellation",
        "Persistent quality failure",
        "Structural domestic cost disadvantage",
        "Loss of qualified customers",
    ],
)


# ==========================================================
# PATTERN 5
# ==========================================================

CUSTOMER_SHIFT = CatalystPattern(
    pattern_id=(
        "PAT-TRADE-IMPORT-SUBSTITUTION-CUSTOMER-SHIFT"
    ),
    family=FAMILY,
    name="Customer Sourcing Shift",
    description=(
        "Large customers shift procurement from overseas "
        "suppliers toward domestic manufacturers."
    ),
    trigger_signals=[
        "Customer sourcing announcements",
        "Vendor requalification",
        "Domestic sourcing targets",
        "New domestic supplier contracts",
    ],
    mechanism=(
        "Procurement strategy change -> supplier requalification -> "
        "domestic sourcing -> customer volume migration."
    ),
    transmission_channels=[
        "Customer Addition",
        "Volume",
        "Market Share",
        "Revenue Growth",
    ],
    leading_indicators=[
        "Customer RFQs",
        "Qualification wins",
        "Trial production",
        "Purchase-order conversion",
    ],
    confirmation_indicators=[
        "Recurring purchase orders",
        "Customer revenue growth",
        "Higher wallet share",
        "Multi-product adoption",
    ],
    typical_time_horizon="1-3 years",
    earnings_channels=[
        "Revenue",
        "EBITDA",
        "PAT",
        "Free Cash Flow",
    ],
    market_mistake=(
        "Market values the initial contract but misses the "
        "potential for expanding wallet share and additional "
        "product qualification."
    ),
    second_order_effects=[
        "Cross-selling",
        "Higher wallet share",
        "Longer customer duration",
        "Additional product qualification",
    ],
    disconfirming_evidence=[
        "Orders fail to repeat",
        "Customer retains overseas sourcing",
        "Qualification does not expand",
        "Price competition eliminates economics",
    ],
    kill_switch=[
        "Customer loss",
        "Contract cancellation",
        "Failed qualification",
        "No repeat ordering",
    ],
)


# ==========================================================
# PATTERN 6
# ==========================================================

COMPETITIVE_COST_ADVANTAGE = CatalystPattern(
    pattern_id=(
        "PAT-TRADE-IMPORT-SUBSTITUTION-COMPETITIVE-COST-ADVANTAGE"
    ),
    family=FAMILY,
    name="Domestic Competitive Cost Advantage",
    description=(
        "Domestic producers achieve a sustainable cost advantage "
        "versus imported alternatives through scale, logistics, "
        "labour, energy, or supply-chain economics."
    ),
    trigger_signals=[
        "Domestic unit costs decline",
        "Scale benefits emerge",
        "Freight advantage increases",
        "Imported landed costs rise",
    ],
    mechanism=(
        "Domestic cost advantage -> landed-cost advantage -> "
        "customer adoption -> market-share gain."
    ),
    transmission_channels=[
        "Cost Reduction",
        "Pricing",
        "Market Share",
        "Operating Leverage",
    ],
    leading_indicators=[
        "Unit-cost trends",
        "Freight costs",
        "Capacity utilisation",
        "Procurement savings",
    ],
    confirmation_indicators=[
        "Gross-margin improvement",
        "Market-share gains",
        "Higher utilisation",
        "Repeat customer wins",
    ],
    typical_time_horizon="1-3 years",
    earnings_channels=[
        "EBITDA Margin",
        "PAT",
        "Free Cash Flow",
        "ROCE",
    ],
    market_mistake=(
        "Market assumes domestic producers need permanent "
        "policy protection and misses an underlying structural "
        "cost advantage."
    ),
    second_order_effects=[
        "Higher pricing flexibility",
        "Capacity expansion",
        "Competitor displacement",
        "Improved capital returns",
    ],
    disconfirming_evidence=[
        "Cost advantage disappears",
        "Imported landed costs decline",
        "Domestic utilisation weakens",
        "Competitors replicate the advantage",
    ],
    kill_switch=[
        "Loss of structural cost advantage",
        "Persistent margin deterioration",
        "Competitor cost parity",
        "Customer migration to imports",
    ],
)


# ==========================================================
# CANONICAL FAMILY COLLECTION
# ==========================================================

TRADE_IMPORT_SUBSTITUTION_PATTERNS = [
    IMPORT_REPLACEMENT,
    DOMESTIC_CAPACITY,
    TARIFF_ADVANTAGE,
    LOCALISATION,
    CUSTOMER_SHIFT,
    COMPETITIVE_COST_ADVANTAGE,
]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [
    "TRADE_IMPORT_SUBSTITUTION_PATTERNS",
]