"""
EIOS
Everest Investment Operating System

Operating Leverage Catalyst Patterns
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# OPERATING LEVERAGE PATTERNS
# ==========================================================

OPERATING_LEVERAGE_PATTERNS = [

    # ======================================================
    # 1. FIXED COST ABSORPTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-OPERATING-LEVERAGE-"
            "FIXED-COST-ABSORPTION"
        ),
        family=CatalystFamily.OPERATING_LEVERAGE,
        name="Fixed Cost Absorption",
        description=(
            "Revenue growth increases absorption of an "
            "existing fixed operating-cost base, causing "
            "operating profit to grow faster than revenue."
        ),
        mechanism=(
            "Revenue growth -> fixed-cost absorption -> "
            "incremental margin expansion -> earnings acceleration."
        ),
        trigger_signals=[
            "Revenue acceleration",
            "Stable fixed-cost base",
            "Improving operating utilisation",
            "Rising contribution from existing infrastructure",
        ],
        leading_indicators=[
            "Revenue growth",
            "Revenue per operating unit",
            "Fixed-cost-to-revenue ratio",
            "Utilisation improvement",
        ],
        confirmation_indicators=[
            "EBITDA margin expansion",
            "Higher incremental EBITDA margin",
            "EBIT growth exceeding revenue growth",
            "Operating expense absorption",
        ],
        earnings_channels=[
            "EBITDA",
            "EBIT",
            "EPS",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market extrapolates historical margins and "
            "fails to recognise that the existing fixed-cost "
            "base can support substantially higher revenue."
        ),
        disconfirming_evidence=[
            "Fixed costs rise materially with revenue",
            "Revenue growth fails to persist",
            "Operating expenses scale proportionately",
            "Incremental margins deteriorate",
        ],
        kill_switch=(
            "Sustained revenue deceleration, structural increase "
            "in fixed operating costs, or loss of operating leverage."
        ),
    ),

    # ======================================================
    # 2. INCREMENTAL MARGIN INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-OPERATING-LEVERAGE-"
            "INCREMENTAL-MARGIN-INFLECTION"
        ),
        family=CatalystFamily.OPERATING_LEVERAGE,
        name="Incremental Margin Inflection",
        description=(
            "Incremental revenue begins generating materially "
            "higher operating margins than the existing business."
        ),
        mechanism=(
            "Revenue acceleration -> limited incremental fixed cost "
            "-> higher incremental margin -> EBIT acceleration."
        ),
        trigger_signals=[
            "Revenue growth acceleration",
            "Stable operating-cost structure",
            "Improving contribution margin",
            "Early margin inflection",
        ],
        leading_indicators=[
            "Quarterly revenue growth",
            "Incremental EBITDA margin",
            "Operating expense growth versus revenue",
            "Employee cost growth versus revenue",
        ],
        confirmation_indicators=[
            "Sustained incremental margin expansion",
            "EBITDA growth above revenue growth",
            "EBIT growth above revenue growth",
            "EPS acceleration",
        ],
        earnings_channels=[
            "EBITDA Margin",
            "EBIT",
            "EPS",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market focuses on reported average margins instead "
            "of the much stronger economics of incremental revenue."
        ),
        disconfirming_evidence=[
            "Incremental margins fail to improve",
            "Operating expenses scale with revenue",
            "Gross margin deterioration offsets leverage",
            "Growth requires substantial new fixed costs",
        ],
        kill_switch=(
            "Persistent deterioration in incremental margins, "
            "operating-cost growth matching revenue growth, or "
            "no evidence of margin inflection."
        ),
    ),

    # ======================================================
    # 3. UTILISATION TO LEVERAGE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-OPERATING-LEVERAGE-"
            "UTILISATION-TO-LEVERAGE"
        ),
        family=CatalystFamily.OPERATING_LEVERAGE,
        name="Utilisation-to-Leverage",
        description=(
            "Higher utilisation of an established operating base "
            "converts unused fixed capacity into disproportionate "
            "operating earnings."
        ),
        mechanism=(
            "Utilisation increase -> fixed-cost absorption -> "
            "incremental margin expansion -> earnings acceleration."
        ),
        trigger_signals=[
            "Utilisation increase",
            "Production increase",
            "Order book improvement",
            "Demand recovery",
        ],
        leading_indicators=[
            "Capacity utilisation",
            "Production volumes",
            "Dispatches",
            "Order book",
        ],
        confirmation_indicators=[
            "Higher EBITDA margin",
            "Higher EBIT margin",
            "Improving ROCE",
            "Improving ROIIC",
        ],
        earnings_channels=[
            "Revenue",
            "EBITDA Margin",
            "EBIT",
            "EPS",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market recognises higher utilisation but "
            "underestimates the resulting earnings leverage."
        ),
        disconfirming_evidence=[
            "Utilisation increase fails to persist",
            "Additional costs rise proportionately",
            "Demand weakens",
            "Incremental margins remain unchanged",
        ],
        kill_switch=(
            "Sustained utilisation deterioration, loss of demand "
            "visibility, or no corresponding incremental profitability."
        ),
    ),

    # ======================================================
    # 4. REVENUE THRESHOLD CROSSING
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-OPERATING-LEVERAGE-"
            "REVENUE-THRESHOLD-CROSSING"
        ),
        family=CatalystFamily.OPERATING_LEVERAGE,
        name="Revenue Threshold Crossing",
        description=(
            "Revenue crosses a structural absorption threshold "
            "after which incremental revenue produces a materially "
            "larger increase in operating profit."
        ),
        mechanism=(
            "Revenue crosses fixed-cost absorption threshold -> "
            "incremental contribution rises -> EBIT/EPS inflection."
        ),
        trigger_signals=[
            "Revenue approaching operating break-even threshold",
            "Improving utilisation",
            "Operating expense absorption",
            "Demand acceleration",
        ],
        leading_indicators=[
            "Revenue run-rate",
            "Operating expense-to-revenue ratio",
            "Contribution margin",
            "Utilisation",
        ],
        confirmation_indicators=[
            "EBIT turning positive or accelerating",
            "Sharp EBITDA margin improvement",
            "EPS inflection",
            "Free cash flow inflection",
        ],
        earnings_channels=[
            "EBITDA",
            "EBIT",
            "EPS",
            "Free Cash Flow",
        ],
        market_mistake=(
            "Market assumes earnings will improve linearly, "
            "while the business is approaching a nonlinear "
            "operating-profit threshold."
        ),
        disconfirming_evidence=[
            "Threshold is pushed higher by new costs",
            "Revenue fails to cross the required level",
            "Contribution margin deteriorates",
            "Operating expenses accelerate",
        ],
        kill_switch=(
            "Revenue growth failure, persistent operating losses "
            "beyond the expected threshold, or structural increase "
            "in fixed costs."
        ),
    ),

    # ======================================================
    # 5. VOLUME TO EARNINGS AMPLIFICATION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-OPERATING-LEVERAGE-"
            "VOLUME-TO-EARNINGS-AMPLIFICATION"
        ),
        family=CatalystFamily.OPERATING_LEVERAGE,
        name="Volume-to-Earnings Amplification",
        description=(
            "A relatively modest increase in physical volume "
            "produces disproportionately higher operating profit "
            "because the fixed-cost base is already established."
        ),
        mechanism=(
            "Volume growth -> fixed-cost absorption -> "
            "higher incremental operating margin -> "
            "disproportionate earnings growth."
        ),
        trigger_signals=[
            "Volume acceleration",
            "Higher throughput",
            "Improving utilisation",
            "Stable operating infrastructure",
        ],
        leading_indicators=[
            "Unit volumes",
            "Production",
            "Dispatches",
            "Throughput",
        ],
        confirmation_indicators=[
            "EBITDA growth above volume growth",
            "EBIT growth above revenue growth",
            "Incremental margin expansion",
            "EPS acceleration",
        ],
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EBIT",
            "EPS",
        ],
        market_mistake=(
            "Market values volume growth linearly and "
            "fails to account for the nonlinear earnings "
            "impact of the existing fixed-cost base."
        ),
        disconfirming_evidence=[
            "Volume growth requires significant new costs",
            "Realisation declines materially",
            "Utilisation does not improve",
            "Incremental profitability remains weak",
        ],
        kill_switch=(
            "Volume deterioration, loss of operating leverage, "
            "or structural increase in variable costs."
        ),
    ),

    # ======================================================
    # 6. EPS INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-OPERATING-LEVERAGE-"
            "EPS-INFLECTION"
        ),
        family=CatalystFamily.OPERATING_LEVERAGE,
        name="EPS Inflection",
        description=(
            "Operating leverage becomes visible through a "
            "disproportionate acceleration in EPS relative to "
            "revenue growth."
        ),
        mechanism=(
            "Revenue/volume growth -> fixed-cost absorption -> "
            "incremental margin expansion -> EPS acceleration."
        ),
        trigger_signals=[
            "Revenue acceleration",
            "Margin inflection",
            "Operating-cost absorption",
            "Improving utilisation",
        ],
        leading_indicators=[
            "Incremental EBITDA margin",
            "EBIT growth",
            "Operating expense leverage",
            "Operating profit",
        ],
        confirmation_indicators=[
            "EPS growth exceeding revenue growth",
            "EBIT acceleration",
            "Free cash flow acceleration",
            "Consensus EPS revisions",
        ],
        earnings_channels=[
            "EBIT",
            "EPS",
            "Free Cash Flow",
            "ROCE",
            "ROIIC",
        ],
        market_mistake=(
            "Market models earnings growth linearly and "
            "fails to recognise the nonlinear EPS response "
            "created by operating leverage."
        ),
        disconfirming_evidence=[
            "EPS acceleration is driven by non-operating items",
            "Incremental margins fail to improve",
            "Revenue growth weakens",
            "Operating costs rise disproportionately",
        ],
        kill_switch=(
            "Sustained EPS deceleration, loss of incremental "
            "margin expansion, or operating leverage failing "
            "to appear in reported earnings."
        ),
    ),
]


# ==========================================================
# EXPORT
# ==========================================================

__all__ = [
    "OPERATING_LEVERAGE_PATTERNS",
]