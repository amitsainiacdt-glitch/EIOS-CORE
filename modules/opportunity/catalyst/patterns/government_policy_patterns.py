"""
EIOS
Everest Investment Operating System

Government Policy Catalyst Patterns

Family:
    CatalystFamily.GOVERNMENT_POLICY

Purpose:
    Canonical machine-readable patterns beneath the
    Government Policy catalyst family.

Design:
    Passive data only.
    No scoring.
    No ranking.
    No valuation.
    No investment decisions.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


GOVERNMENT_POLICY_PATTERNS = [

    # ======================================================
    # 1. POLICY INCENTIVE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-GOVERNMENT-POLICY-INCENTIVE"
        ),
        family=CatalystFamily.GOVERNMENT_POLICY,
        name=(
            "Policy Incentive"
        ),
        description=(
            "A government incentive materially improves "
            "the economics of a target industry or activity."
        ),
        trigger_signals=[
            "Policy announcement",
            "Incentive notification",
            "Government programme",
        ],
        mechanism=(
            "Policy incentive → improved economics → "
            "higher demand/investment → earnings impact."
        ),
        transmission_channels=[
            "Demand",
            "Capacity",
            "Margins",
            "Capital expenditure",
        ],
        leading_indicators=[
            "Policy notification",
            "Industry applications",
            "Project announcements",
        ],
        confirmation_indicators=[
            "Order growth",
            "Capacity additions",
            "Customer adoption",
            "Revenue acceleration",
        ],
        typical_time_horizon=(
            "6-36 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Operating Margin",
            "ROIIC",
        ],
        market_mistake=(
            "Market underestimates the duration and "
            "economic impact of the incentive."
        ),
        second_order_effects=[
            "Supplier investment",
            "Capacity expansion",
            "Industry consolidation",
        ],
        disconfirming_evidence=[
            "Low incentive utilisation",
            "Weak customer response",
            "Policy withdrawal",
        ],
        kill_switch=(
            "The incentive is materially reduced, withdrawn, "
            "or fails to generate measurable economic activity."
        ),
    ),

    # ======================================================
    # 2. GOVERNMENT PROGRAMME
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-GOVERNMENT-POLICY-PROGRAMME"
        ),
        family=CatalystFamily.GOVERNMENT_POLICY,
        name=(
            "Government Programme"
        ),
        description=(
            "A government programme creates sustained demand "
            "for products or services in a defined industry."
        ),
        trigger_signals=[
            "Programme announcement",
            "Budget allocation",
            "Government tenders",
            "Implementation guidelines",
        ],
        mechanism=(
            "Government programme → funded demand → "
            "industry orders → revenue and capacity utilisation."
        ),
        transmission_channels=[
            "Demand",
            "Orders",
            "Capacity Utilisation",
            "Revenue",
        ],
        leading_indicators=[
            "Budget allocation",
            "Tender issuance",
            "Project approvals",
        ],
        confirmation_indicators=[
            "Order wins",
            "Execution growth",
            "Government spending",
            "Revenue growth",
        ],
        typical_time_horizon=(
            "6-48 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Operating Leverage",
            "Cash Flow",
        ],
        market_mistake=(
            "Market treats the programme as announcement-only "
            "and underestimates actual implementation."
        ),
        second_order_effects=[
            "Private investment",
            "Supplier expansion",
            "Employment growth",
        ],
        disconfirming_evidence=[
            "Budget under-utilisation",
            "Tender delays",
            "Weak execution",
        ],
        kill_switch=(
            "Programme funding or implementation fails to "
            "translate into measurable industry demand."
        ),
    ),

    # ======================================================
    # 3. POLICY RESTRICTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-GOVERNMENT-POLICY-RESTRICTION"
        ),
        family=CatalystFamily.GOVERNMENT_POLICY,
        name=(
            "Policy Restriction"
        ),
        description=(
            "A government restriction changes competitive "
            "economics by limiting undesirable supply or activity."
        ),
        trigger_signals=[
            "Restriction notification",
            "Licensing changes",
            "Import restrictions",
            "Environmental restrictions",
        ],
        mechanism=(
            "Restriction → supply limitation → "
            "industry rationalisation → pricing/share opportunity."
        ),
        transmission_channels=[
            "Supply",
            "Pricing",
            "Market Share",
            "Margins",
        ],
        leading_indicators=[
            "Regulatory implementation",
            "Licence approvals",
            "Industry closures",
        ],
        confirmation_indicators=[
            "Supply reduction",
            "Pricing improvement",
            "Market share gains",
            "Margin expansion",
        ],
        typical_time_horizon=(
            "6-36 months"
        ),
        earnings_channels=[
            "Pricing",
            "Market Share",
            "Margins",
        ],
        market_mistake=(
            "Market focuses on compliance costs and "
            "underestimates structural supply rationalisation."
        ),
        second_order_effects=[
            "Competitor exits",
            "Capacity rationalisation",
            "Industry consolidation",
        ],
        disconfirming_evidence=[
            "Weak enforcement",
            "New competing supply",
            "Policy reversal",
        ],
        kill_switch=(
            "The restriction is not enforced sufficiently "
            "to alter industry economics."
        ),
    ),

    # ======================================================
    # 4. POLICY IMPLEMENTATION ACCELERATION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-GOVERNMENT-POLICY-IMPLEMENTATION"
        ),
        family=CatalystFamily.GOVERNMENT_POLICY,
        name=(
            "Policy Implementation Acceleration"
        ),
        description=(
            "A previously announced government policy "
            "moves rapidly from announcement to execution."
        ),
        trigger_signals=[
            "Implementation guidelines",
            "Administrative approvals",
            "Tender acceleration",
            "Funding release",
        ],
        mechanism=(
            "Implementation acceleration → faster economic "
            "activity → earlier earnings impact."
        ),
        transmission_channels=[
            "Orders",
            "Revenue",
            "Capacity Utilisation",
            "Cash Flow",
        ],
        leading_indicators=[
            "Funding release",
            "Tender activity",
            "Approval velocity",
        ],
        confirmation_indicators=[
            "Order inflow",
            "Execution",
            "Revenue acceleration",
        ],
        typical_time_horizon=(
            "3-24 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "Operating Leverage",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market anchors to historical implementation delays "
            "and misses an acceleration in execution."
        ),
        second_order_effects=[
            "Supplier orders",
            "Capacity expansion",
            "Working-capital acceleration",
        ],
        disconfirming_evidence=[
            "Repeated implementation delays",
            "Funding bottlenecks",
            "Administrative obstruction",
        ],
        kill_switch=(
            "Implementation does not accelerate and the "
            "expected earnings timing remains structurally delayed."
        ),
    ),

    # ======================================================
    # 5. POLICY BENEFICIARY RE-RATING
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-GOVERNMENT-POLICY-BENEFICIARY-RERATING"
        ),
        family=CatalystFamily.GOVERNMENT_POLICY,
        name=(
            "Policy Beneficiary Re-rating"
        ),
        description=(
            "A policy change causes the market to recognise "
            "a previously underappreciated beneficiary."
        ),
        trigger_signals=[
            "Policy announcement",
            "Analyst estimate revisions",
            "Management commentary",
            "Industry response",
        ],
        mechanism=(
            "Policy change → earnings expectations rise → "
            "market recognition → valuation re-rating."
        ),
        transmission_channels=[
            "Earnings expectations",
            "Sentiment",
            "Valuation",
            "Capital allocation",
        ],
        leading_indicators=[
            "Estimate revisions",
            "Management guidance",
            "Peer commentary",
        ],
        confirmation_indicators=[
            "Consensus upgrades",
            "Revenue revisions",
            "Earnings upgrades",
        ],
        typical_time_horizon=(
            "3-24 months"
        ),
        earnings_channels=[
            "Revenue Growth",
            "EPS Growth",
            "Valuation Multiple",
        ],
        market_mistake=(
            "Market initially treats the policy as macro news "
            "and fails to identify the specific beneficiaries."
        ),
        second_order_effects=[
            "Multiple expansion",
            "Institutional buying",
            "Capacity investment",
        ],
        disconfirming_evidence=[
            "No earnings transmission",
            "Weak beneficiary economics",
            "Consensus downgrade",
        ],
        kill_switch=(
            "The policy produces no material incremental "
            "economic benefit for the identified beneficiary."
        ),
    ),

    # ======================================================
    # 6. POLICY DURABILITY
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-GOVERNMENT-POLICY-DURABILITY"
        ),
        family=CatalystFamily.GOVERNMENT_POLICY,
        name=(
            "Policy Durability"
        ),
        description=(
            "A government policy proves durable enough to "
            "create a multi-year change in industry economics."
        ),
        trigger_signals=[
            "Multi-year policy framework",
            "Repeated budget allocation",
            "Long-term implementation",
            "Cross-government support",
        ],
        mechanism=(
            "Policy durability → persistent demand/investment "
            "signal → long-duration earnings opportunity."
        ),
        transmission_channels=[
            "Demand",
            "Capital expenditure",
            "Capacity",
            "ROIIC",
        ],
        leading_indicators=[
            "Multi-year funding",
            "Repeated programme execution",
            "Industry investment",
        ],
        confirmation_indicators=[
            "Sustained revenue growth",
            "Capacity expansion",
            "Long-term order visibility",
            "Incremental returns",
        ],
        typical_time_horizon=(
            "2-7 years"
        ),
        earnings_channels=[
            "Revenue Growth",
            "ROIIC",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market assumes the policy is temporary and "
            "underestimates its duration."
        ),
        second_order_effects=[
            "New entrants",
            "Supplier ecosystems",
            "Industry capacity expansion",
            "Technology investment",
        ],
        disconfirming_evidence=[
            "Budget withdrawal",
            "Political reversal",
            "Weak programme execution",
            "Poor industry economics",
        ],
        kill_switch=(
            "The policy framework loses durability or "
            "fails to produce sustained economic activity."
        ),
    ),
]


__all__ = [
    "GOVERNMENT_POLICY_PATTERNS",
]