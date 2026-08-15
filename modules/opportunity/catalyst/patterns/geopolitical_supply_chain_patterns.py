"""
EIOS
Everest Investment Operating System

Catalyst Pattern Module
Family: GEOPOLITICAL_SUPPLY_CHAIN

Purpose:
    Canonical catalyst patterns describing situations where
    geopolitical developments alter supply chains, sourcing,
    logistics, trade routes, production footprints, or
    strategic inventory requirements.

Design Principles:
    - Pattern definitions only.
    - No scoring.
    - No ranking.
    - No valuation.
    - No investment decision.
    - Canonical CatalystPattern objects only.
"""

from typing import List

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# PATTERN 1
# ==========================================================

SUPPLY_CHAIN_RELOCATION = CatalystPattern(
    pattern_id=(
        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "RELOCATION"
    ),

    family=(
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ),

    name=(
        "Geopolitical Supply Chain Relocation"
    ),

    description=(
        "Geopolitical tensions, sanctions, trade restrictions, "
        "or strategic de-risking cause manufacturers or supply "
        "chain participants to relocate sourcing or production "
        "toward alternative countries or regions."
    ),

    mechanism=(
        "A geopolitical shock increases the perceived risk of "
        "concentrated production or sourcing, causing customers "
        "to redesign supply chains and allocate business to "
        "alternative manufacturing or sourcing ecosystems."
    ),

    trigger_signals=[
        "Geopolitical escalation",
        "Sanctions or export restrictions",
        "Customer de-risking announcements",
        "Supplier diversification initiatives",
        "Production relocation announcements",
    ],

    leading_indicators=[
        "New supplier qualification activity",
        "Customer audits",
        "Factory transfer discussions",
        "Tooling relocation",
        "Dual-sourcing initiatives",
    ],

    confirmation_indicators=[
        "New customer wins",
        "Volume migration",
        "Capacity additions",
        "Higher utilisation",
        "Long-term supply agreements",
    ],

    transmission_channels=[
        "Customer sourcing shift",
        "Production relocation",
        "Supplier diversification",
        "Capacity migration",
        "Regional manufacturing expansion",
    ],

    typical_time_horizon=(
        "12-60 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "Volume growth",
        "Capacity utilisation",
        "Market share gains",
    ],

    market_mistake=(
        "The market treats geopolitical supply-chain shifts "
        "as temporary disruption rather than a structural "
        "migration of production and sourcing."
    ),

    second_order_effects=[
        "Supplier ecosystem development",
        "Local manufacturing investment",
        "Customer concentration changes",
        "Higher switching costs",
        "Longer-duration contracts",
    ],

    disconfirming_evidence=[
        "Geopolitical tensions de-escalate",
        "Customers retain existing suppliers",
        "Relocation projects are cancelled",
        "Alternative suppliers remain uneconomic",
        "No measurable volume migration",
    ],

    kill_switch=(
        "No sustained customer or production migration occurs "
        "despite the geopolitical catalyst."
    ),
)


# ==========================================================
# PATTERN 2
# ==========================================================

STRATEGIC_SOURCING_DIVERSIFICATION = CatalystPattern(
    pattern_id=(
        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "SOURCING-DIVERSIFICATION"
    ),

    family=(
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ),

    name=(
        "Strategic Sourcing Diversification"
    ),

    description=(
        "Geopolitical concentration risk causes customers to "
        "move from single-source procurement toward diversified "
        "supplier networks."
    ),

    mechanism=(
        "Customers assign greater economic value to supply "
        "security and qualify additional suppliers, creating "
        "incremental opportunities for capable alternative "
        "producers."
    ),

    trigger_signals=[
        "Single-source risk reduction",
        "Supplier diversification mandates",
        "Geopolitical risk disclosures",
        "Dual-sourcing programs",
        "Procurement restructuring",
    ],

    leading_indicators=[
        "Supplier qualification",
        "Trial orders",
        "Technical approvals",
        "Customer audits",
        "Prototype or sample activity",
    ],

    confirmation_indicators=[
        "Commercial orders",
        "Recurring volumes",
        "Customer additions",
        "Higher wallet share",
        "Long-term contracts",
    ],

    transmission_channels=[
        "Procurement diversification",
        "Supplier qualification",
        "Customer addition",
        "Volume migration",
        "Contract wins",
    ],

    typical_time_horizon=(
        "6-36 months"
    ),

    earnings_channels=[
        "Customer additions",
        "Revenue growth",
        "Volume growth",
        "Capacity utilisation",
    ],

    market_mistake=(
        "The market underestimates the persistence of supplier "
        "diversification once customers incur qualification and "
        "switching costs."
    ),

    second_order_effects=[
        "Reduced customer concentration",
        "Higher supplier stickiness",
        "Longer customer relationships",
        "Higher qualification barriers",
        "Broader export opportunities",
    ],

    disconfirming_evidence=[
        "Customers return to concentrated sourcing",
        "Qualification programs stop",
        "Alternative suppliers fail quality requirements",
        "No recurring commercial volumes",
        "Cost dominates supply-security considerations",
    ],

    kill_switch=(
        "Supplier diversification fails to convert into "
        "sustained commercial volumes."
    ),
)


# ==========================================================
# PATTERN 3
# ==========================================================

TRADE_ROUTE_DISRUPTION = CatalystPattern(
    pattern_id=(
        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "TRADE-ROUTE-DISRUPTION"
    ),

    family=(
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ),

    name=(
        "Geopolitical Trade Route Disruption"
    ),

    description=(
        "Conflict, sanctions, blockades, or geopolitical "
        "instability disrupt established shipping and trade "
        "routes, forcing companies to alter logistics networks "
        "or sourcing arrangements."
    ),

    mechanism=(
        "Higher transit risk, longer routes, insurance costs, "
        "and delivery uncertainty force supply-chain redesign "
        "and can redirect business toward alternative logistics "
        "or regional production networks."
    ),

    trigger_signals=[
        "Shipping route disruption",
        "Port restrictions",
        "Regional conflict",
        "Insurance cost escalation",
        "Freight route changes",
    ],

    leading_indicators=[
        "Freight rerouting",
        "Transit-time increases",
        "Inventory build-up",
        "Alternative port usage",
        "Emergency sourcing",
    ],

    confirmation_indicators=[
        "Persistent route changes",
        "Regional sourcing increases",
        "Higher inventory requirements",
        "New logistics contracts",
        "Customer sourcing shifts",
    ],

    transmission_channels=[
        "Logistics rerouting",
        "Inventory requirements",
        "Regional sourcing",
        "Freight economics",
        "Customer supply-chain redesign",
    ],

    typical_time_horizon=(
        "3-24 months"
    ),

    earnings_channels=[
        "Logistics revenue",
        "Regional sourcing",
        "Inventory-related demand",
        "Pricing",
    ],

    market_mistake=(
        "The market assumes trade-route disruption is temporary "
        "and fails to recognise when companies permanently "
        "redesign logistics and sourcing networks."
    ),

    second_order_effects=[
        "Regional inventory hubs",
        "Alternative port development",
        "Supplier diversification",
        "Higher logistics resilience spending",
        "Permanent route redesign",
    ],

    disconfirming_evidence=[
        "Trade routes normalise rapidly",
        "Freight economics revert",
        "Customers do not change sourcing",
        "Inventory requirements normalise",
        "No structural supply-chain redesign",
    ],

    kill_switch=(
        "Trade routes normalise without creating persistent "
        "changes in sourcing or logistics architecture."
    ),
)


# ==========================================================
# PATTERN 4
# ==========================================================

SANCTIONS_EXPORT_CONTROL_SHIFT = CatalystPattern(
    pattern_id=(
        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "SANCTIONS-EXPORT-CONTROL"
    ),

    family=(
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ),

    name=(
        "Sanctions and Export-Control Supply Shift"
    ),

    description=(
        "Sanctions, export controls, technology restrictions, "
        "or licensing changes prevent existing suppliers from "
        "serving customers and create openings for alternative "
        "suppliers."
    ),

    mechanism=(
        "Restricted access to products, components, technologies, "
        "or raw materials forces customers to identify compliant "
        "alternative suppliers."
    ),

    trigger_signals=[
        "New sanctions",
        "Export-control restrictions",
        "Technology bans",
        "Licensing restrictions",
        "Restricted-country sourcing rules",
    ],

    leading_indicators=[
        "Alternative supplier qualification",
        "Regulatory compliance reviews",
        "Customer sourcing enquiries",
        "Technology substitution",
        "Inventory precautionary builds",
    ],

    confirmation_indicators=[
        "Replacement orders",
        "New customer contracts",
        "Volume migration",
        "Capacity expansion",
        "Recurring demand",
    ],

    transmission_channels=[
        "Supplier exclusion",
        "Technology substitution",
        "Customer qualification",
        "Compliance-driven sourcing",
        "Volume migration",
    ],

    typical_time_horizon=(
        "6-48 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "Market share gains",
        "Volume growth",
        "Capacity utilisation",
    ],

    market_mistake=(
        "The market treats sanctions and export controls as "
        "temporary restrictions instead of recognising the "
        "potential for permanent supplier displacement."
    ),

    second_order_effects=[
        "New qualification barriers",
        "Longer customer relationships",
        "Domestic capability development",
        "Higher strategic inventory",
        "Supplier concentration changes",
    ],

    disconfirming_evidence=[
        "Restrictions are removed",
        "Customers maintain incumbent suppliers",
        "Alternative suppliers fail qualification",
        "Substitution proves uneconomic",
        "Orders do not persist",
    ],

    kill_switch=(
        "Regulatory restrictions fail to produce sustained "
        "supplier displacement."
    ),
)


# ==========================================================
# PATTERN 5
# ==========================================================

STRATEGIC_INVENTORY_BUILD = CatalystPattern(
    pattern_id=(
        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "STRATEGIC-INVENTORY"
    ),

    family=(
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ),

    name=(
        "Geopolitical Strategic Inventory Build"
    ),

    description=(
        "Geopolitical uncertainty causes companies or governments "
        "to build strategic inventories of critical materials, "
        "components, or products to reduce supply interruption risk."
    ),

    mechanism=(
        "The economic cost of stockouts increases relative to "
        "inventory carrying costs, resulting in structurally "
        "higher safety-stock requirements."
    ),

    trigger_signals=[
        "Strategic stockpile announcements",
        "Supply-security concerns",
        "Geopolitical escalation",
        "Inventory policy changes",
        "Critical-material shortages",
    ],

    leading_indicators=[
        "Inventory days increasing",
        "Procurement acceleration",
        "Government stockpile programs",
        "Long-term purchase commitments",
        "Warehouse capacity expansion",
    ],

    confirmation_indicators=[
        "Higher order volumes",
        "Persistent inventory demand",
        "Strategic procurement contracts",
        "Stockpile expansion",
        "Longer supply commitments",
    ],

    transmission_channels=[
        "Inventory accumulation",
        "Procurement acceleration",
        "Strategic stockpiling",
        "Long-term contracts",
        "Demand pull-forward",
    ],

    typical_time_horizon=(
        "6-36 months"
    ),

    earnings_channels=[
        "Volume growth",
        "Revenue growth",
        "Pricing",
        "Capacity utilisation",
    ],

    market_mistake=(
        "The market assumes inventory accumulation is merely "
        "temporary destocking or stocking activity rather than "
        "a structural increase in supply-security requirements."
    ),

    second_order_effects=[
        "Higher safety-stock norms",
        "Expanded storage infrastructure",
        "Longer supplier contracts",
        "Greater demand visibility",
        "Strategic procurement relationships",
    ],

    disconfirming_evidence=[
        "Inventory policies normalise",
        "Geopolitical risk declines",
        "Strategic stockpiles are released",
        "Procurement volumes revert",
        "No persistent demand increase",
    ],

    kill_switch=(
        "Strategic inventory requirements revert to historical "
        "levels without persistent geopolitical risk."
    ),
)


# ==========================================================
# PATTERN 6
# ==========================================================

REGIONAL_SUPPLY_CHAIN_LOCALISATION = CatalystPattern(
    pattern_id=(
        "PAT-GEOPOLITICAL-SUPPLY-CHAIN-"
        "REGIONAL-LOCALISATION"
    ),

    family=(
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ),

    name=(
        "Regional Supply Chain Localisation"
    ),

    description=(
        "Geopolitical risk encourages customers to build "
        "regionalised production and supplier ecosystems, "
        "creating durable demand for local manufacturing capacity."
    ),

    mechanism=(
        "Companies value proximity, resilience, and political "
        "alignment alongside cost, resulting in a structural "
        "shift toward regional production and sourcing."
    ),

    trigger_signals=[
        "Regional manufacturing strategies",
        "Localisation targets",
        "Supply-chain resilience programs",
        "Government industrial policies",
        "Regional sourcing mandates",
    ],

    leading_indicators=[
        "Local supplier qualification",
        "Regional factory investments",
        "Local procurement programs",
        "New manufacturing partnerships",
        "Technology transfer activity",
    ],

    confirmation_indicators=[
        "Commercial production",
        "Recurring local orders",
        "Capacity expansion",
        "Customer additions",
        "Long-term supply agreements",
    ],

    transmission_channels=[
        "Local manufacturing",
        "Supplier ecosystem development",
        "Regional procurement",
        "Customer localisation",
        "Capacity investment",
    ],

    typical_time_horizon=(
        "24-84 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "Market share gains",
        "Capacity utilisation",
        "Customer additions",
    ],

    market_mistake=(
        "The market underestimates the duration of regionalisation "
        "because individual localisation announcements appear "
        "incremental rather than representing a structural supply-chain shift."
    ),

    second_order_effects=[
        "Domestic supplier ecosystems",
        "Higher entry barriers",
        "Customer stickiness",
        "Regional capacity creation",
        "Technology localisation",
    ],

    disconfirming_evidence=[
        "Regionalisation projects are cancelled",
        "Customers return to global sourcing",
        "Local production remains uneconomic",
        "Government support disappears",
        "No sustained commercial volumes",
    ],

    kill_switch=(
        "Regional localisation fails to translate into sustained "
        "production, sourcing, or customer-volume migration."
    ),
)


# ==========================================================
# CANONICAL FAMILY COLLECTION
# ==========================================================

GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS: List[
    CatalystPattern
] = [

    SUPPLY_CHAIN_RELOCATION,

    STRATEGIC_SOURCING_DIVERSIFICATION,

    TRADE_ROUTE_DISRUPTION,

    SANCTIONS_EXPORT_CONTROL_SHIFT,

    STRATEGIC_INVENTORY_BUILD,

    REGIONAL_SUPPLY_CHAIN_LOCALISATION,
]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [
    "SUPPLY_CHAIN_RELOCATION",
    "STRATEGIC_SOURCING_DIVERSIFICATION",
    "TRADE_ROUTE_DISRUPTION",
    "SANCTIONS_EXPORT_CONTROL_SHIFT",
    "STRATEGIC_INVENTORY_BUILD",
    "REGIONAL_SUPPLY_CHAIN_LOCALISATION",
    "GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS",
]