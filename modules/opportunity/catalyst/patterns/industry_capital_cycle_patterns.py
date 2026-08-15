"""
EIOS
Everest Investment Operating System

Industry Capital Cycle Catalyst Patterns

Purpose:
Canonical passive catalyst pattern definitions for
Industry Capital Cycle.

Design Principles:

- Pattern definitions are passive data.
- No analysis.
- No scoring.
- No ranking.
- No valuation.
- No company-specific logic.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


INDUSTRY_CAPITAL_CYCLE_PATTERNS = [

    # ======================================================
    # 1. CAPACITY DISCIPLINE INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPITAL-CYCLE-CAPACITY-DISCIPLINE-INFLECTION"
        ),
        name=(
            "Capacity Discipline Inflection"
        ),
        family=(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ),
        description=(
            "Industry capacity additions moderate or become "
            "more disciplined after a period of excess investment."
        ),
        mechanism=(
            "Lower incremental capacity additions "
            "→ supply discipline "
            "→ utilisation improvement "
            "→ pricing power "
            "→ margin recovery."
        ),
        trigger_signals=[
            "Industry capex moderation",
            "Capacity addition delays",
            "Competitor capex cancellations",
            "Lower new project announcements",
        ],
        leading_indicators=[
            "Industry project pipeline",
            "Competitor capex plans",
            "Capacity commissioning delays",
            "New project approvals",
        ],
        confirmation_indicators=[
            "Industry utilisation improvement",
            "Firming pricing",
            "Improving margins",
            "Improving ROCE",
        ],
        earnings_channels=[
            "Utilisation",
            "Pricing",
            "Margins",
            "ROCE",
        ],
        market_mistake=(
            "Market assumes historical excess-capacity conditions "
            "will persist despite improving supply discipline."
        ),
        disconfirming_evidence=[
            "Unexpected capacity announcements",
            "Aggressive competitor expansion",
            "Demand deterioration",
            "Renewed industry overinvestment",
        ],
        kill_switch=(
            "Industry capacity additions reaccelerate materially "
            "faster than underlying demand."
        ),
    ),

    # ======================================================
    # 2. DEMAND-LED CAPACITY ABSORPTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPITAL-CYCLE-DEMAND-LED-CAPACITY-ABSORPTION"
        ),
        name=(
            "Demand-Led Capacity Absorption"
        ),
        family=(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ),
        description=(
            "Demand growth absorbs previously available industry "
            "capacity faster than the market expects."
        ),
        mechanism=(
            "Demand acceleration "
            "→ excess capacity absorption "
            "→ utilisation increase "
            "→ fixed-cost absorption "
            "→ earnings and return inflection."
        ),
        trigger_signals=[
            "Demand acceleration",
            "Order growth",
            "Inventory normalisation",
            "Industry utilisation recovery",
        ],
        leading_indicators=[
            "Customer order activity",
            "Industry shipment growth",
            "Inventory-to-sales trends",
            "Capacity utilisation data",
        ],
        confirmation_indicators=[
            "Higher plant utilisation",
            "Operating margin expansion",
            "Improving ROCE",
            "Rising incremental returns",
        ],
        earnings_channels=[
            "Volume",
            "Utilisation",
            "Margins",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market focuses on installed capacity rather than "
            "the speed at which demand is absorbing it."
        ),
        disconfirming_evidence=[
            "Demand slowdown",
            "Inventory build-up",
            "Weak customer orders",
            "New capacity overwhelming demand",
        ],
        kill_switch=(
            "Demand growth fails to translate into sustained "
            "industry utilisation improvement."
        ),
    ),

    # ======================================================
    # 3. CAPEX CYCLE TURN
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPITAL-CYCLE-CAPEX-CYCLE-TURN"
        ),
        name=(
            "Capex Cycle Turn"
        ),
        family=(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ),
        description=(
            "Industry investment transitions from contraction or "
            "underinvestment toward a measured recovery."
        ),
        mechanism=(
            "Capex trough "
            "→ investment recovery "
            "→ productive capacity renewal "
            "→ improved industry economics "
            "→ stronger long-term returns."
        ),
        trigger_signals=[
            "Industry capex trough",
            "Competitor investment restart",
            "Project approvals",
            "Capacity replacement activity",
        ],
        leading_indicators=[
            "Capex announcements",
            "Equipment orders",
            "Project approvals",
            "Financing activity",
        ],
        confirmation_indicators=[
            "Capacity commissioning",
            "Industry volume recovery",
            "Utilisation stabilisation",
            "Improving ROCE",
        ],
        earnings_channels=[
            "Volume",
            "Utilisation",
            "Margins",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market interprets the early investment recovery as "
            "value-destructive spending rather than a healthy "
            "capital-cycle reset."
        ),
        disconfirming_evidence=[
            "Speculative overinvestment",
            "Weak demand visibility",
            "Low project returns",
            "Rapid industry capacity oversupply",
        ],
        kill_switch=(
            "New industry investment consistently produces "
            "capacity faster than demand can absorb."
        ),
    ),

    # ======================================================
    # 4. UNDERINVESTMENT-LED SUPPLY TIGHTENING
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPITAL-CYCLE-UNDERINVESTMENT-SUPPLY-TIGHTENING"
        ),
        name=(
            "Underinvestment-Led Supply Tightening"
        ),
        family=(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ),
        description=(
            "Prolonged industry underinvestment constrains future "
            "capacity and creates tighter supply-demand economics."
        ),
        mechanism=(
            "Historical underinvestment "
            "→ limited future capacity "
            "→ supply tightening "
            "→ utilisation and pricing improvement "
            "→ margin expansion."
        ),
        trigger_signals=[
            "Extended industry capex weakness",
            "Aging asset base",
            "Limited project pipeline",
            "Long capacity lead times",
        ],
        leading_indicators=[
            "Industry capex-to-sales",
            "Asset age",
            "Project approvals",
            "Capacity replacement requirements",
        ],
        confirmation_indicators=[
            "Utilisation approaching high levels",
            "Firm pricing",
            "Longer customer lead times",
            "Margin expansion",
        ],
        earnings_channels=[
            "Utilisation",
            "Pricing",
            "Margins",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market assumes new supply will arrive quickly even "
            "though industry lead times and underinvestment "
            "constrain capacity creation."
        ),
        disconfirming_evidence=[
            "Large new capacity announcements",
            "Shorter-than-expected project timelines",
            "Demand weakness",
            "Technology-driven capacity expansion",
        ],
        kill_switch=(
            "Industry supply expands rapidly enough to eliminate "
            "the expected capacity scarcity."
        ),
    ),

    # ======================================================
    # 5. PEAK-CAPACITY CYCLE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPITAL-CYCLE-PEAK-CAPACITY-UTILISATION"
        ),
        name=(
            "Peak Capacity Utilisation Cycle"
        ),
        family=(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ),
        description=(
            "Industry utilisation approaches capacity limits while "
            "incremental supply remains constrained."
        ),
        mechanism=(
            "High utilisation "
            "→ constrained incremental supply "
            "→ pricing power "
            "→ margin expansion "
            "→ elevated incremental returns."
        ),
        trigger_signals=[
            "Utilisation approaching peak levels",
            "Tight industry inventories",
            "Long customer lead times",
            "Limited incremental capacity",
        ],
        leading_indicators=[
            "Industry utilisation",
            "Inventory levels",
            "Lead times",
            "Capacity pipeline",
        ],
        confirmation_indicators=[
            "Pricing increases",
            "Margin expansion",
            "High ROCE",
            "Strong ROIIC",
        ],
        earnings_channels=[
            "Utilisation",
            "Pricing",
            "Margins",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market assumes peak utilisation will immediately "
            "attract enough new capacity to normalise returns."
        ),
        disconfirming_evidence=[
            "Rapid competitor capex",
            "Demand contraction",
            "Customer destocking",
            "Technology substitution",
        ],
        kill_switch=(
            "A sustained wave of new capacity removes the "
            "industry supply constraint."
        ),
    ),

    # ======================================================
    # 6. CAPITAL RETURNS INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPITAL-CYCLE-CAPITAL-RETURNS-INFLECTION"
        ),
        name=(
            "Capital Returns Inflection"
        ),
        family=(
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ),
        description=(
            "Improving industry economics allow companies to "
            "generate materially higher returns on incremental capital."
        ),
        mechanism=(
            "Improving supply-demand balance "
            "→ better utilisation and pricing "
            "→ stronger margins "
            "→ higher incremental returns "
            "→ improved capital allocation economics."
        ),
        trigger_signals=[
            "ROCE recovery",
            "ROIIC improvement",
            "Margin recovery",
            "Improving industry pricing",
        ],
        leading_indicators=[
            "Incremental margins",
            "Utilisation trends",
            "Industry pricing",
            "Competitor returns",
        ],
        confirmation_indicators=[
            "Sustained ROCE improvement",
            "Higher ROIIC",
            "Free cash flow improvement",
            "Disciplined capital allocation",
        ],
        earnings_channels=[
            "Margins",
            "ROCE",
            "ROIIC",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market treats improved returns as temporary cyclical "
            "normalisation rather than evidence of a structural "
            "capital-cycle improvement."
        ),
        disconfirming_evidence=[
            "ROCE deterioration",
            "Falling incremental returns",
            "Aggressive capital spending",
            "Weakening industry pricing",
        ],
        kill_switch=(
            "Incremental returns fail to remain above the "
            "company's cost of capital as the cycle progresses."
        ),
    ),
]


__all__ = [
    "INDUSTRY_CAPITAL_CYCLE_PATTERNS",
]