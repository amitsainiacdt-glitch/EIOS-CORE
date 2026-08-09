"""
EIOS
Everest Investment Operating System

Capacity Catalyst Patterns

Purpose:
    Canonical catalyst patterns belonging to the
    CAPACITY_EXPANSION catalyst family.

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
# CAPACITY CATALYST PATTERNS
# ==========================================================

CAPACITY_PATTERNS: List[CatalystPattern] = [

    # ======================================================
    # 1. BROWNFIELD CAPACITY EXPANSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CAPACITY-BROWNFIELD",
        family=CatalystFamily.CAPACITY_EXPANSION,
        name="Brownfield Capacity Expansion",

        description=(
            "Expansion of existing facilities to increase "
            "productive capacity."
        ),

        trigger_signals=[
            "brownfield expansion",
            "capacity addition",
            "plant expansion",
        ],

        mechanism=(
            "Additional capacity can increase output, "
            "revenue and operating leverage."
        ),

        transmission_channels=[
            "Capacity",
            "Volume",
            "Utilisation",
            "Revenue",
        ],

        leading_indicators=[
            "Capex announcement",
            "Equipment orders",
            "Construction progress",
        ],

        confirmation_indicators=[
            "Commissioning",
            "Production increase",
            "Utilisation increase",
        ],

        typical_time_horizon="12-36 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],

        market_mistake=(
            "The market underestimates the economic "
            "impact or speed of the expansion."
        ),

        second_order_effects=[
            "Market-share gains",
            "Customer additions",
        ],

        disconfirming_evidence=[
            "Project delay",
            "Weak demand",
            "Poor utilisation",
        ],

        kill_switch=(
            "Expansion fails to achieve commercially "
            "viable utilisation within the expected period."
        ),
    ),

    # ======================================================
    # 2. CAPACITY DEBOTTLENECKING
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-CAPACITY-DEBOTTLENECK",
        family=CatalystFamily.CAPACITY_EXPANSION,
        name="Capacity Debottlenecking",

        description=(
            "Removal of production constraints without "
            "requiring a major new facility."
        ),

        trigger_signals=[
            "debottlenecking",
            "debottleneck",
            "process optimisation",
            "capacity optimisation",
        ],

        mechanism=(
            "Constraint removal increases productive "
            "output from existing assets."
        ),

        transmission_channels=[
            "Volume",
            "Utilisation",
            "Asset Productivity",
        ],

        leading_indicators=[
            "Process modification",
            "Small expansion capex",
            "Equipment upgrade",
        ],

        confirmation_indicators=[
            "Higher production",
            "Higher utilisation",
            "Incremental margin improvement",
        ],

        typical_time_horizon="6-24 months",

        earnings_channels=[
            "Revenue",
            "EBITDA",
            "ROIC",
            "FCF",
        ],

        market_mistake=(
            "The market treats debottlenecking as "
            "routine maintenance rather than incremental capacity."
        ),

        second_order_effects=[
            "Higher asset productivity",
            "Earlier customer fulfilment",
        ],

        disconfirming_evidence=[
            "No measurable output increase",
            "Unexpected capex",
        ],

        kill_switch=(
            "Debottlenecking produces no material "
            "incremental economic output."
        ),
    ),
]


__all__ = [
    "CAPACITY_PATTERNS",
]