"""
EIOS
Everest Investment Operating System

Catalyst Pattern Module

Family:
    CORPORATE_ACTION_MA

Purpose:
    Canonical catalyst patterns describing corporate actions,
    mergers, acquisitions, demergers, strategic combinations,
    and related changes in corporate structure.

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

ACQUISITION_VALUE_REALISATION = CatalystPattern(
    pattern_id=(
        "PAT-CORPORATE-ACTION-MA-"
        "ACQUISITION-VALUE-REALISATION"
    ),

    family=(
        CatalystFamily.CORPORATE_ACTION_MA
    ),

    name=(
        "Acquisition Value Realisation"
    ),

    description=(
        "An acquisition creates a measurable opportunity for "
        "the acquirer to improve growth, capabilities, market "
        "position, distribution, technology, or earnings."
    ),

    mechanism=(
        "The acquirer combines its existing platform with the "
        "target's assets, customers, technology, capabilities, "
        "or distribution network, potentially creating incremental "
        "economic value."
    ),

    trigger_signals=[
        "Acquisition announcement",
        "Strategic acquisition rationale",
        "Target capability disclosure",
        "Management integration plan",
        "Synergy guidance",
    ],

    leading_indicators=[
        "Integration milestones",
        "Customer cross-selling",
        "Distribution expansion",
        "Cost integration",
        "Product or technology integration",
    ],

    confirmation_indicators=[
        "Revenue synergies",
        "Cost synergies",
        "Margin improvement",
        "Higher growth",
        "Improved return on capital",
    ],

    transmission_channels=[
        "Revenue synergies",
        "Cost synergies",
        "Cross-selling",
        "Capability expansion",
        "Market expansion",
    ],

    typical_time_horizon=(
        "12-48 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "Margin expansion",
        "Operating leverage",
        "Earnings growth",
    ],

    market_mistake=(
        "The market focuses on acquisition price and near-term "
        "integration costs while underestimating the potential "
        "economic value of the acquired capabilities."
    ),

    second_order_effects=[
        "Customer cross-selling",
        "Distribution expansion",
        "Technology transfer",
        "Higher entry barriers",
        "Improved competitive position",
    ],

    disconfirming_evidence=[
        "Integration delays",
        "Synergies fail to materialise",
        "Customer losses",
        "Margin deterioration",
        "Capital returns remain below expectations",
    ],

    kill_switch=(
        "The acquisition fails to produce measurable strategic "
        "or economic benefits within the expected integration period."
    ),
)


# ==========================================================
# PATTERN 2
# ==========================================================

MERGER_SYNERGY_REALISATION = CatalystPattern(
    pattern_id=(
        "PAT-CORPORATE-ACTION-MA-"
        "MERGER-SYNERGY-REALISATION"
    ),

    family=(
        CatalystFamily.CORPORATE_ACTION_MA
    ),

    name=(
        "Merger Synergy Realisation"
    ),

    description=(
        "A merger creates operating, financial, commercial, "
        "or strategic synergies that progressively improve "
        "the economics of the combined business."
    ),

    mechanism=(
        "The combined entity removes duplicated costs, combines "
        "capabilities, increases purchasing power, broadens "
        "distribution, or improves asset utilisation."
    ),

    trigger_signals=[
        "Merger announcement",
        "Synergy targets",
        "Integration roadmap",
        "Cost restructuring",
        "Combined operating plan",
    ],

    leading_indicators=[
        "Duplicate cost removal",
        "Procurement savings",
        "Branch or facility consolidation",
        "Cross-selling",
        "Shared infrastructure",
    ],

    confirmation_indicators=[
        "Cost savings",
        "Margin expansion",
        "Higher cash flow",
        "Improved asset utilisation",
        "Earnings accretion",
    ],

    transmission_channels=[
        "Cost reduction",
        "Revenue synergy",
        "Procurement leverage",
        "Asset utilisation",
        "Operating leverage",
    ],

    typical_time_horizon=(
        "12-36 months"
    ),

    earnings_channels=[
        "Margin expansion",
        "Operating leverage",
        "Free cash flow",
        "Earnings growth",
    ],

    market_mistake=(
        "The market discounts merger synergies because "
        "integration appears complex, even when the underlying "
        "cost and revenue opportunities are identifiable."
    ),

    second_order_effects=[
        "Higher margins",
        "Improved capital efficiency",
        "Stronger competitive position",
        "Lower cost base",
        "Higher free cash flow",
    ],

    disconfirming_evidence=[
        "Synergy targets repeatedly reduced",
        "Integration disruption",
        "Unexpected restructuring costs",
        "Customer attrition",
        "No margin improvement",
    ],

    kill_switch=(
        "The combined business fails to demonstrate measurable "
        "synergy capture."
    ),
)


# ==========================================================
# PATTERN 3
# ==========================================================

DEMERGER_VALUE_UNLOCK = CatalystPattern(
    pattern_id=(
        "PAT-CORPORATE-ACTION-MA-"
        "DEMERGER-VALUE-UNLOCK"
    ),

    family=(
        CatalystFamily.CORPORATE_ACTION_MA
    ),

    name=(
        "Demerger Value Unlock"
    ),

    description=(
        "A demerger separates businesses with different economics, "
        "capital requirements, growth profiles, or valuation "
        "characteristics, potentially allowing each business "
        "to be independently valued and managed."
    ),

    mechanism=(
        "Corporate separation reduces conglomerate complexity "
        "and allows management, capital allocation, investors, "
        "and operating teams to focus on distinct businesses."
    ),

    trigger_signals=[
        "Demerger announcement",
        "Scheme approval",
        "Separate business disclosures",
        "Independent management structures",
        "Standalone financial reporting",
    ],

    leading_indicators=[
        "Regulatory approvals",
        "Shareholder approvals",
        "Standalone reporting",
        "Management appointments",
        "Capital allocation plans",
    ],

    confirmation_indicators=[
        "Separate financial reporting",
        "Improved operating focus",
        "Independent valuation",
        "Better capital allocation",
        "Improved return metrics",
    ],

    transmission_channels=[
        "Valuation re-rating",
        "Management focus",
        "Capital allocation",
        "Business simplification",
        "Investor base separation",
    ],

    typical_time_horizon=(
        "6-36 months"
    ),

    earnings_channels=[
        "Capital efficiency",
        "Margin improvement",
        "Growth acceleration",
        "Free cash flow improvement",
    ],

    market_mistake=(
        "The market fails to recognise the value created by "
        "separating businesses with different economic profiles "
        "inside a conglomerate structure."
    ),

    second_order_effects=[
        "Specialist investor ownership",
        "Improved capital allocation",
        "Strategic optionality",
        "Higher management accountability",
        "Independent M&A flexibility",
    ],

    disconfirming_evidence=[
        "Demerger delays",
        "Regulatory rejection",
        "Weak standalone economics",
        "Capital allocation remains poor",
        "No improvement in business focus",
    ],

    kill_switch=(
        "The separation does not occur or fails to improve "
        "the economic and strategic characteristics of the businesses."
    ),
)


# ==========================================================
# PATTERN 4
# ==========================================================

STRATEGIC_STAKE_SALE = CatalystPattern(
    pattern_id=(
        "PAT-CORPORATE-ACTION-MA-"
        "STRATEGIC-STAKE-SALE"
    ),

    family=(
        CatalystFamily.CORPORATE_ACTION_MA
    ),

    name=(
        "Strategic Stake Sale"
    ),

    description=(
        "A company sells a strategic stake or non-core business, "
        "releasing capital and potentially simplifying its "
        "corporate structure."
    ),

    mechanism=(
        "The transaction converts a non-core or underutilised "
        "asset into capital that can be deployed toward debt "
        "reduction, core expansion, acquisitions, or shareholder returns."
    ),

    trigger_signals=[
        "Stake-sale announcement",
        "Strategic review",
        "Non-core asset classification",
        "Buyer discussions",
        "Divestment process",
    ],

    leading_indicators=[
        "Strategic alternatives review",
        "Valuation discussions",
        "Potential buyer interest",
        "Transaction documentation",
        "Board approval",
    ],

    confirmation_indicators=[
        "Transaction completion",
        "Debt reduction",
        "Core-business investment",
        "Capital return",
        "Improved return on capital",
    ],

    transmission_channels=[
        "Capital recycling",
        "Debt reduction",
        "Core investment",
        "Shareholder returns",
        "Portfolio simplification",
    ],

    typical_time_horizon=(
        "6-24 months"
    ),

    earnings_channels=[
        "Interest-cost reduction",
        "Return on capital",
        "Core-business growth",
        "Free cash flow",
    ],

    market_mistake=(
        "The market treats divestment proceeds as a one-time "
        "balance-sheet event rather than recognising the value "
        "of disciplined capital recycling."
    ),

    second_order_effects=[
        "Lower leverage",
        "Improved capital efficiency",
        "Higher core-business focus",
        "Reduced complexity",
        "Greater strategic flexibility",
    ],

    disconfirming_evidence=[
        "Transaction cancellation",
        "Low sale proceeds",
        "Proceeds used inefficiently",
        "Debt remains elevated",
        "Core returns do not improve",
    ],

    kill_switch=(
        "The divestment fails to release meaningful capital or "
        "management does not redeploy proceeds productively."
    ),
)


# ==========================================================
# PATTERN 5
# ==========================================================

ACQUISITION_CAPABILITY_EXPANSION = CatalystPattern(
    pattern_id=(
        "PAT-CORPORATE-ACTION-MA-"
        "CAPABILITY-EXPANSION"
    ),

    family=(
        CatalystFamily.CORPORATE_ACTION_MA
    ),

    name=(
        "Acquisition-Led Capability Expansion"
    ),

    description=(
        "An acquisition gives a company access to technology, "
        "talent, intellectual property, manufacturing capability, "
        "distribution, or market access that would be difficult "
        "or slow to develop internally."
    ),

    mechanism=(
        "The acquisition compresses the time required to obtain "
        "strategic capabilities and allows the acquirer to "
        "accelerate entry into new products or markets."
    ),

    trigger_signals=[
        "Technology acquisition",
        "Capability acquisition",
        "New product entry",
        "Geographic expansion",
        "Specialist talent acquisition",
    ],

    leading_indicators=[
        "Product integration",
        "New customer qualification",
        "Technology deployment",
        "New-market entry",
        "Capacity integration",
    ],

    confirmation_indicators=[
        "New product revenue",
        "Customer additions",
        "Market share gains",
        "Higher growth",
        "Improved competitive position",
    ],

    transmission_channels=[
        "Technology",
        "Distribution",
        "Talent",
        "Product expansion",
        "Market entry",
    ],

    typical_time_horizon=(
        "12-60 months"
    ),

    earnings_channels=[
        "Revenue growth",
        "Market share",
        "Product mix",
        "Operating leverage",
    ],

    market_mistake=(
        "The market values the transaction primarily on near-term "
        "earnings contribution and misses the strategic value of "
        "accelerated capability development."
    ),

    second_order_effects=[
        "New product platforms",
        "Higher customer stickiness",
        "Technology moat",
        "Market expansion",
        "Faster innovation",
    ],

    disconfirming_evidence=[
        "Technology integration fails",
        "Customers reject new offerings",
        "Capability remains underutilised",
        "Key employees leave",
        "Expected market entry fails",
    ],

    kill_switch=(
        "The acquired capability does not become commercially "
        "useful or strategically differentiated."
    ),
)


# ==========================================================
# PATTERN 6
# ==========================================================

RELATED_PARTY_RESTRUCTURING = CatalystPattern(
    pattern_id=(
        "PAT-CORPORATE-ACTION-MA-"
        "CORPORATE-RESTRUCTURING"
    ),

    family=(
        CatalystFamily.CORPORATE_ACTION_MA
    ),

    name=(
        "Corporate Structure Restructuring"
    ),

    description=(
        "A restructuring of subsidiaries, ownership structures, "
        "business divisions, or corporate entities simplifies "
        "the group and can improve transparency and capital allocation."
    ),

    mechanism=(
        "The company reorganises assets or subsidiaries to reduce "
        "structural complexity, improve accountability, separate "
        "businesses, or align capital with operating requirements."
    ),

    trigger_signals=[
        "Corporate restructuring announcement",
        "Subsidiary consolidation",
        "Business transfer",
        "Group simplification",
        "Strategic restructuring",
    ],

    leading_indicators=[
        "Board approvals",
        "Regulatory filings",
        "Standalone reporting",
        "Management changes",
        "Capital allocation changes",
    ],

    confirmation_indicators=[
        "Simplified structure",
        "Lower overhead",
        "Improved disclosure",
        "Better capital allocation",
        "Higher return metrics",
    ],

    transmission_channels=[
        "Cost reduction",
        "Capital allocation",
        "Transparency",
        "Management accountability",
        "Business simplification",
    ],

    typical_time_horizon=(
        "6-36 months"
    ),

    earnings_channels=[
        "Cost reduction",
        "Margin improvement",
        "Capital efficiency",
        "Free cash flow",
    ],

    market_mistake=(
        "The market ignores structural simplification because "
        "the immediate earnings impact appears small, while the "
        "long-term improvement in capital allocation can be meaningful."
    ),

    second_order_effects=[
        "Improved disclosure",
        "Lower corporate overhead",
        "Better accountability",
        "Strategic flexibility",
        "Potential future asset monetisation",
    ],

    disconfirming_evidence=[
        "Restructuring remains incomplete",
        "Complexity persists",
        "Costs increase",
        "Capital allocation does not improve",
        "No measurable operating benefit",
    ],

    kill_switch=(
        "Corporate restructuring fails to produce measurable "
        "improvements in transparency, capital allocation, "
        "or operating efficiency."
    ),
)


# ==========================================================
# CANONICAL FAMILY COLLECTION
# ==========================================================

CORPORATE_ACTION_MA_PATTERNS: List[
    CatalystPattern
] = [

    ACQUISITION_VALUE_REALISATION,

    MERGER_SYNERGY_REALISATION,

    DEMERGER_VALUE_UNLOCK,

    STRATEGIC_STAKE_SALE,

    ACQUISITION_CAPABILITY_EXPANSION,

    RELATED_PARTY_RESTRUCTURING,
]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "ACQUISITION_VALUE_REALISATION",

    "MERGER_SYNERGY_REALISATION",

    "DEMERGER_VALUE_UNLOCK",

    "STRATEGIC_STAKE_SALE",

    "ACQUISITION_CAPABILITY_EXPANSION",

    "RELATED_PARTY_RESTRUCTURING",

    "CORPORATE_ACTION_MA_PATTERNS",
]