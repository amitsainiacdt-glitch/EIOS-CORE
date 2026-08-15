"""
EIOS
Everest Investment Operating System

Capacity Utilisation Catalyst Patterns

Purpose:
Canonical catalyst patterns describing situations where
existing installed capacity moves toward higher utilisation,
creating operating leverage, margin expansion, and improved
capital efficiency.

Design Principles:

- Patterns are passive data definitions.
- No scoring is performed here.
- No ranking is performed here.
- No valuation is performed here.
- No company-specific logic is hardcoded.
- Each pattern contains leading indicators,
  confirmation indicators, earnings channels,
  market mistake, disconfirming evidence,
  and kill switch.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# CANONICAL CAPACITY UTILISATION PATTERNS
# ==========================================================

CAPACITY_UTILISATION_PATTERNS = [

    # ======================================================
    # 1. UTILISATION INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPACITY-UTILISATION-"
            "UTILISATION-INFLECTION"
        ),
        name=(
            "Capacity Utilisation Inflection"
        ),
        family=(
            CatalystFamily.CAPACITY_UTILISATION
        ),
        description=(
            "Existing installed capacity moves from "
            "under-utilisation toward materially higher "
            "utilisation."
        ),
        mechanism=(
            "Utilisation increase → fixed-cost absorption "
            "→ incremental margin expansion → earnings "
            "growth."
        ),
        trigger_signals=[
            "Rising customer demand",
            "Improving order flow",
            "Higher production requirements",
            "Management indicating utilisation improvement",
        ],
        leading_indicators=[
            "Order intake",
            "Dispatch growth",
            "Production growth",
            "Customer capacity expansion",
        ],
        confirmation_indicators=[
            "Reported utilisation increase",
            "Higher production volumes",
            "EBITDA margin improvement",
            "Improved asset productivity",
        ],
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EBITDA Margin",
            "EPS",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market fails to recognise that modest "
            "utilisation improvement can create "
            "disproportionate earnings growth."
        ),
        disconfirming_evidence=[
            "Demand remains weak",
            "Utilisation fails to improve",
            "Production remains below expectations",
            "Fixed costs continue rising",
        ],
        kill_switch=(
            "Sustained utilisation deterioration despite "
            "expected demand recovery."
        ),
    ),

    # ======================================================
    # 2. FIXED-COST ABSORPTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPACITY-UTILISATION-"
            "FIXED-COST-ABSORPTION"
        ),
        name=(
            "Fixed Cost Absorption Through Utilisation"
        ),
        family=(
            CatalystFamily.CAPACITY_UTILISATION
        ),
        description=(
            "Higher utilisation spreads existing fixed "
            "costs across a larger production base."
        ),
        mechanism=(
            "Higher throughput → lower fixed cost per unit "
            "→ gross or operating margin expansion → "
            "earnings acceleration."
        ),
        trigger_signals=[
            "Volume recovery",
            "Production ramp-up",
            "Improving plant loading",
            "Stable fixed-cost base",
        ],
        leading_indicators=[
            "Production volume",
            "Capacity utilisation",
            "Units per facility",
            "Employee productivity",
        ],
        confirmation_indicators=[
            "Lower fixed cost per unit",
            "Operating margin expansion",
            "EBITDA growth ahead of revenue",
            "Improved operating leverage",
        ],
        earnings_channels=[
            "EBITDA Margin",
            "EBIT Margin",
            "EPS",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market extrapolates historical margins and "
            "fails to recognise incremental operating "
            "leverage."
        ),
        disconfirming_evidence=[
            "Fixed costs increase materially",
            "Volume growth fails",
            "Incremental margins remain weak",
            "Utilisation gains do not translate into margins",
        ],
        kill_switch=(
            "Higher utilisation fails to produce measurable "
            "fixed-cost absorption or incremental margin "
            "improvement."
        ),
    ),

    # ======================================================
    # 3. UTILISATION TO MARGIN INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPACITY-UTILISATION-"
            "MARGIN-INFLECTION"
        ),
        name=(
            "Utilisation-Driven Margin Inflection"
        ),
        family=(
            CatalystFamily.CAPACITY_UTILISATION
        ),
        description=(
            "Improving utilisation causes operating margins "
            "to inflect upward after a threshold level of "
            "capacity loading is reached."
        ),
        mechanism=(
            "Utilisation threshold → incremental production "
            "with limited incremental fixed costs → margin "
            "inflection → EPS acceleration."
        ),
        trigger_signals=[
            "Utilisation approaching historical threshold",
            "Strong volume growth",
            "Improving demand visibility",
            "Stable operating cost base",
        ],
        leading_indicators=[
            "Capacity loading",
            "Volume growth",
            "Production efficiency",
            "Order visibility",
        ],
        confirmation_indicators=[
            "Sequential margin expansion",
            "Incremental EBITDA margin improvement",
            "EPS growth exceeding revenue growth",
            "Higher ROCE",
        ],
        earnings_channels=[
            "EBITDA Margin",
            "EBIT Margin",
            "EPS",
            "ROCE",
        ],
        market_mistake=(
            "Market assumes margins will remain near "
            "historical averages and misses the threshold "
            "effect of higher utilisation."
        ),
        disconfirming_evidence=[
            "No utilisation threshold effect",
            "Variable costs rise disproportionately",
            "Margin remains stagnant",
            "Demand loses momentum",
        ],
        kill_switch=(
            "Utilisation increases materially without the "
            "expected incremental margin response."
        ),
    ),

    # ======================================================
    # 4. UNDERUTILISED ASSET REACTIVATION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPACITY-UTILISATION-"
            "UNDERUTILISED-ASSET-REACTIVATION"
        ),
        name=(
            "Underutilised Asset Reactivation"
        ),
        family=(
            CatalystFamily.CAPACITY_UTILISATION
        ),
        description=(
            "Previously underutilised production assets "
            "return toward economically meaningful "
            "utilisation without requiring proportional "
            "new capital expenditure."
        ),
        mechanism=(
            "Idle or underutilised assets → demand recovery "
            "→ incremental output → earnings recovery "
            "without equivalent new capex."
        ),
        trigger_signals=[
            "Demand recovery",
            "Restart of idle production lines",
            "New customer demand",
            "Improving industry cycle",
        ],
        leading_indicators=[
            "Plant restart announcements",
            "Order intake",
            "Production schedules",
            "Customer demand",
        ],
        confirmation_indicators=[
            "Higher asset utilisation",
            "Revenue recovery",
            "Margin recovery",
            "Improved asset turnover",
        ],
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "ROCE",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market values the company on depressed earnings "
            "without recognising the earnings recovery "
            "available from existing underutilised assets."
        ),
        disconfirming_evidence=[
            "Assets remain idle",
            "Demand recovery fails",
            "Restart costs are excessive",
            "Asset economics remain unattractive",
        ],
        kill_switch=(
            "Previously underutilised assets cannot be "
            "economically reactivated despite the expected "
            "demand recovery."
        ),
    ),

    # ======================================================
    # 5. CAPACITY CONSTRAINT RELEASE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPACITY-UTILISATION-"
            "CONSTRAINT-RELEASE"
        ),
        name=(
            "Capacity Constraint Release"
        ),
        family=(
            CatalystFamily.CAPACITY_UTILISATION
        ),
        description=(
            "Operational bottlenecks are removed, allowing "
            "existing installed capacity to serve previously "
            "unfulfilled demand."
        ),
        mechanism=(
            "Bottleneck removal → throughput increase "
            "→ higher utilisation → revenue and earnings "
            "growth."
        ),
        trigger_signals=[
            "Debottlenecking",
            "Process improvement",
            "Equipment upgrades",
            "Improved production flow",
        ],
        leading_indicators=[
            "Throughput improvement",
            "Production cycle time",
            "Order backlog",
            "Yield improvement",
        ],
        confirmation_indicators=[
            "Higher output",
            "Higher utilisation",
            "Improved delivery volumes",
            "Revenue acceleration",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "EBITDA",
            "EPS",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market treats the constraint as permanent and "
            "fails to recognise the earnings unlocked by "
            "debottlenecking existing assets."
        ),
        disconfirming_evidence=[
            "Bottleneck persists",
            "Throughput fails to improve",
            "Demand is insufficient",
            "Debottlenecking costs escalate",
        ],
        kill_switch=(
            "Expected bottleneck removal fails to produce "
            "a sustained increase in productive capacity."
        ),
    ),

    # ======================================================
    # 6. UTILISATION-LED CAPITAL EFFICIENCY
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-CAPACITY-UTILISATION-"
            "CAPITAL-EFFICIENCY-INFLECTION"
        ),
        name=(
            "Utilisation-Led Capital Efficiency Inflection"
        ),
        family=(
            CatalystFamily.CAPACITY_UTILISATION
        ),
        description=(
            "Higher utilisation materially improves returns "
            "on an existing asset base without proportional "
            "incremental capital investment."
        ),
        mechanism=(
            "Higher asset utilisation → higher revenue on "
            "existing capital → improved asset turnover "
            "→ ROCE/ROIIC improvement."
        ),
        trigger_signals=[
            "Revenue growth without proportional capex",
            "Higher plant utilisation",
            "Improved asset turnover",
            "Strong demand visibility",
        ],
        leading_indicators=[
            "Revenue growth",
            "Capacity utilisation",
            "Asset turnover",
            "Capex intensity",
        ],
        confirmation_indicators=[
            "ROCE improvement",
            "ROIIC improvement",
            "Higher asset productivity",
            "Free cash flow conversion",
        ],
        earnings_channels=[
            "ROCE",
            "ROIIC",
            "Free Cash Flow",
            "EPS",
            "Capital Efficiency",
        ],
        market_mistake=(
            "Market focuses on absolute earnings growth "
            "and underestimates the value of earnings growth "
            "generated from an already-funded asset base."
        ),
        disconfirming_evidence=[
            "Capex rises proportionally with revenue",
            "Asset turnover does not improve",
            "ROCE remains depressed",
            "ROIIC fails to improve",
        ],
        kill_switch=(
            "Utilisation-driven growth requires proportional "
            "new capital and fails to improve incremental "
            "capital returns."
        ),
    ),
]


# ==========================================================
# EXPORT
# ==========================================================

__all__ = [
    "CAPACITY_UTILISATION_PATTERNS",
]