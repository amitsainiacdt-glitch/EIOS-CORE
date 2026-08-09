"""
EIOS
Everest Investment Operating System

Regulatory Catalyst Patterns

Purpose:
    Canonical catalyst patterns belonging to the
    REGULATORY_CHANGE catalyst family.

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
# REGULATORY CATALYST PATTERNS
# ==========================================================

REGULATORY_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. PRODUCT APPROVAL
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REGULATORY-PRODUCT-APPROVAL",
        family=CatalystFamily.REGULATORY_CHANGE,
        name="Product Approval",

        description=(
            "Regulatory approval allows a product or service "
            "to enter or expand within a regulated market."
        ),

        trigger_signals=[
            "product approval",
            "regulatory approval",
            "product clearance",
            "market approval",
        ],

        mechanism=(
            "Approval removes a regulatory barrier and "
            "creates or expands commercial market access."
        ),

        transmission_channels=[
            "Market Access",
            "Revenue",
            "TAM",
            "Market Share",
        ],

        leading_indicators=[
            "Regulatory filing",
            "Application acceptance",
            "Regulatory review",
            "Inspection",
        ],

        confirmation_indicators=[
            "Approval granted",
            "Commercial launch",
            "Initial customer orders",
            "Sales ramp",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the probability, "
            "speed, or commercial value of approval."
        ),

        second_order_effects=[
            "Customer additions",
            "Reference customers",
            "Capacity expansion",
            "Market-share gains",
        ],

        disconfirming_evidence=[
            "Approval delay",
            "Regulatory rejection",
            "Weak customer adoption",
            "Commercial launch delay",
        ],

        kill_switch=(
            "Required approval is rejected or approval "
            "fails to produce commercially meaningful demand."
        ),
    ),

    # ======================================================
    # 2. LICENCE / PERMIT APPROVAL
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REGULATORY-LICENCE-APPROVAL",
        family=CatalystFamily.REGULATORY_CHANGE,
        name="Licence / Permit Approval",

        description=(
            "Granting or renewal of a licence or permit "
            "enables a company to undertake previously "
            "restricted commercial activity."
        ),

        trigger_signals=[
            "licence approval",
            "license approval",
            "permit approval",
            "operating licence",
            "operating permit",
        ],

        mechanism=(
            "Regulatory permission removes an operating "
            "constraint and enables commercial activity."
        ),

        transmission_channels=[
            "Operating Capacity",
            "Market Access",
            "Revenue",
        ],

        leading_indicators=[
            "Licence application",
            "Regulatory inspection",
            "Compliance submission",
        ],

        confirmation_indicators=[
            "Licence granted",
            "Permit issued",
            "Operations commenced",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the economic value "
            "of newly permitted operating capacity."
        ),

        second_order_effects=[
            "Capacity expansion",
            "Customer acquisition",
            "Higher asset utilisation",
        ],

        disconfirming_evidence=[
            "Approval delay",
            "Licence rejection",
            "Operating restrictions",
        ],

        kill_switch=(
            "Required licence or permit is not obtained "
            "within the economically relevant timeframe."
        ),
    ),

    # ======================================================
    # 3. REGULATORY RELAXATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REGULATORY-RELAXATION",
        family=CatalystFamily.REGULATORY_CHANGE,
        name="Regulatory Relaxation",

        description=(
            "Removal or reduction of regulatory restrictions "
            "increases the economic freedom of an industry "
            "or company."
        ),

        trigger_signals=[
            "regulatory relaxation",
            "deregulation",
            "rules relaxed",
            "regulatory easing",
            "restriction removed",
        ],

        mechanism=(
            "Reduced regulatory friction lowers barriers "
            "or costs and expands the feasible economic opportunity."
        ),

        transmission_channels=[
            "TAM",
            "Cost",
            "Market Access",
            "Capacity",
        ],

        leading_indicators=[
            "Policy consultation",
            "Draft regulation",
            "Industry representation",
        ],

        confirmation_indicators=[
            "Final regulation",
            "Restriction removal",
            "Implementation notification",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market fails to incorporate the second-order "
            "economic effects of reduced regulatory friction."
        ),

        second_order_effects=[
            "New entrants",
            "Higher industry investment",
            "Market expansion",
            "Lower compliance costs",
        ],

        disconfirming_evidence=[
            "Implementation delay",
            "Partial relaxation",
            "Offsetting regulation",
        ],

        kill_switch=(
            "Regulatory change fails to produce a material "
            "improvement in industry economics."
        ),
    ),

    # ======================================================
    # 4. IMPORT RESTRICTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REGULATORY-IMPORT-RESTRICTION",
        family=CatalystFamily.REGULATORY_CHANGE,
        name="Import Restriction",

        description=(
            "Regulatory restrictions on imports increase "
            "the relative competitiveness of domestic suppliers."
        ),

        trigger_signals=[
            "import restriction",
            "import curbs",
            "import controls",
            "higher import duty",
            "customs restriction",
        ],

        mechanism=(
            "Restricted imports reduce foreign competitive "
            "supply and may increase domestic sourcing."
        ),

        transmission_channels=[
            "Market Share",
            "Pricing",
            "Volume",
            "Domestic Demand",
        ],

        leading_indicators=[
            "Policy proposals",
            "Tariff discussions",
            "Industry lobbying",
            "Import-volume changes",
        ],

        confirmation_indicators=[
            "Restriction implemented",
            "Import volumes decline",
            "Domestic orders increase",
            "Domestic utilisation rises",
        ],

        typical_time_horizon="6-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the ability of "
            "domestic producers to capture displaced imports."
        ),

        second_order_effects=[
            "Capacity expansion",
            "Pricing power",
            "Customer migration",
            "Domestic investment",
        ],

        disconfirming_evidence=[
            "Import substitution fails",
            "Alternative foreign suppliers emerge",
            "Domestic capacity is insufficient",
            "Policy reversal",
        ],

        kill_switch=(
            "Import restrictions fail to create sustainable "
            "economic advantage for the domestic company."
        ),
    ),

    # ======================================================
    # 5. EXPORT PERMISSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REGULATORY-EXPORT-PERMISSION",
        family=CatalystFamily.REGULATORY_CHANGE,
        name="Export Permission",

        description=(
            "Removal of export restrictions opens access "
            "to international markets."
        ),

        trigger_signals=[
            "export permission",
            "export approval",
            "export restrictions lifted",
            "export ban lifted",
            "export licence",
        ],

        mechanism=(
            "Export access expands the addressable market "
            "and enables additional sales channels."
        ),

        transmission_channels=[
            "TAM",
            "Volume",
            "Revenue",
            "Geographic Expansion",
        ],

        leading_indicators=[
            "Policy review",
            "Export application",
            "Government consultation",
        ],

        confirmation_indicators=[
            "Export permission granted",
            "Export orders",
            "New international customers",
            "Shipment growth",
        ],

        typical_time_horizon="3-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the incremental "
            "market opportunity created by export access."
        ),

        second_order_effects=[
            "Capacity expansion",
            "International customer relationships",
            "Product certification",
            "Geographic diversification",
        ],

        disconfirming_evidence=[
            "Weak export demand",
            "Logistics constraints",
            "Export restrictions remain",
            "Poor international economics",
        ],

        kill_switch=(
            "New export access fails to generate "
            "economically meaningful incremental demand."
        ),
    ),

    # ======================================================
    # 6. COMPLIANCE-DRIVEN DEMAND
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-REGULATORY-COMPLIANCE-DEMAND",
        family=CatalystFamily.REGULATORY_CHANGE,
        name="Compliance-Driven Demand",

        description=(
            "New or stricter regulation forces customers "
            "to purchase products or services required for compliance."
        ),

        trigger_signals=[
            "new compliance requirement",
            "mandatory standards",
            "new safety regulation",
            "environmental regulation",
            "emission standards",
            "compliance requirement",
        ],

        mechanism=(
            "Mandatory compliance creates non-discretionary "
            "customer spending and expands demand for compliant solutions."
        ),

        transmission_channels=[
            "Demand",
            "TAM",
            "Pricing",
            "Market Share",
        ],

        leading_indicators=[
            "Draft standards",
            "Regulatory consultation",
            "Implementation timelines",
            "Customer compliance planning",
        ],

        confirmation_indicators=[
            "Regulation becomes effective",
            "Customer orders",
            "Industry compliance spending",
            "Revenue acceleration",
        ],

        typical_time_horizon="6-48 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market treats compliance spending as "
            "discretionary rather than structurally mandatory."
        ),

        second_order_effects=[
            "Higher industry adoption",
            "New product development",
            "Customer switching",
            "Pricing power",
        ],

        disconfirming_evidence=[
            "Implementation delay",
            "Regulation weakened",
            "Compliance exemption",
            "Customer spending below expectations",
        ],

        kill_switch=(
            "Regulation does not create sustained mandatory "
            "demand at the expected economic scale."
        ),
    ),
]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [
    "REGULATORY_PATTERNS",
]