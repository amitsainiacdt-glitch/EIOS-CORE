"""
EIOS
Everest Investment Operating System

Supply Constraint Catalyst Patterns

Purpose:
Canonical catalyst patterns for the Supply Constraint family.

Design Principles:

- Passive data only.
- No analysis.
- No scoring.
- No ranking.
- No valuation.
- No company-specific logic.
- Each pattern represents a distinct supply-constraint mechanism.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


SUPPLY_CONSTRAINT_PATTERNS = [

    CatalystPattern(
        pattern_id=(
            "PAT-SUPPLY-CONSTRAINT-CAPACITY-SHORTAGE"
        ),
        name=(
            "Structural Capacity Shortage"
        ),
        description=(
            "Industry capacity remains insufficient to meet "
            "underlying demand."
        ),
        mechanism=(
            "Insufficient capacity → supply scarcity → "
            "pricing power/utilisation → higher earnings."
        ),
        trigger_signals=[
            "Demand exceeds available industry capacity",
            "Industry capacity additions remain limited",
            "Lead times extend",
        ],
        leading_indicators=[
            "Capacity utilisation",
            "Lead times",
            "Industry capex",
            "Order backlogs",
        ],
        confirmation_indicators=[
            "Sustained high utilisation",
            "Tight product availability",
            "Improving realisations",
        ],
        earnings_channels=[
            "Pricing",
            "Volume",
            "Margins",
            "Utilisation",
        ],
        market_mistake=(
            "Market assumes additional capacity will arrive "
            "before the shortage becomes economically meaningful."
        ),
        disconfirming_evidence=[
            "Rapid industry capacity additions",
            "Demand deterioration",
            "Declining utilisation",
        ],
        kill_switch=(
            "New capacity structurally eliminates the supply shortage."
        ),
        family=CatalystFamily.SUPPLY_CONSTRAINT,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-SUPPLY-CONSTRAINT-LEAD-TIME-EXTENSION"
        ),
        name=(
            "Lead-Time Extension"
        ),
        description=(
            "Persistent supply tightness causes customer lead times "
            "to extend materially."
        ),
        mechanism=(
            "Longer lead times → constrained availability → "
            "pricing power → earnings improvement."
        ),
        trigger_signals=[
            "Customer lead times increase",
            "Supplier delivery schedules extend",
            "Backlogs rise",
        ],
        leading_indicators=[
            "Quoted lead times",
            "Order backlog",
            "Booking visibility",
            "Customer inventory levels",
        ],
        confirmation_indicators=[
            "Lead times remain elevated",
            "Order conversion remains strong",
            "Pricing improves alongside tightness",
        ],
        earnings_channels=[
            "Pricing",
            "Volume",
            "Margins",
        ],
        market_mistake=(
            "Market treats longer lead times as temporary "
            "operational disruption."
        ),
        disconfirming_evidence=[
            "Lead times normalise",
            "Backlog cancellation",
            "Customer destocking",
        ],
        kill_switch=(
            "Lead times return to normal without sustained "
            "pricing or utilisation benefits."
        ),
        family=CatalystFamily.SUPPLY_CONSTRAINT,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-SUPPLY-CONSTRAINT-INVENTORY-DEPLETION"
        ),
        name=(
            "Inventory Depletion"
        ),
        description=(
            "Low channel or industry inventory amplifies the impact "
            "of constrained supply."
        ),
        mechanism=(
            "Inventory depletion → reduced buffer stock → "
            "availability scarcity → pricing power."
        ),
        trigger_signals=[
            "Channel inventory declines",
            "Customer inventory reaches low levels",
            "Replenishment demand increases",
        ],
        leading_indicators=[
            "Inventory days",
            "Channel inventory",
            "Customer stock levels",
            "Reorder activity",
        ],
        confirmation_indicators=[
            "Inventory remains below normal",
            "Reorders remain strong",
            "Pricing remains firm",
        ],
        earnings_channels=[
            "Volume",
            "Pricing",
            "Margins",
        ],
        market_mistake=(
            "Market assumes low inventory is merely a temporary "
            "working-capital adjustment."
        ),
        disconfirming_evidence=[
            "Inventory rebuilding",
            "Weak reorder activity",
            "Demand deterioration",
        ],
        kill_switch=(
            "Inventory normalisation removes the supply-driven "
            "scarcity premium."
        ),
        family=CatalystFamily.SUPPLY_CONSTRAINT,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-SUPPLY-CONSTRAINT-SUPPLIER-CONSOLIDATION"
        ),
        name=(
            "Supplier Consolidation"
        ),
        description=(
            "A reduction in the number of economically viable "
            "suppliers tightens industry supply."
        ),
        mechanism=(
            "Supplier exit/consolidation → supply rationalisation → "
            "greater scarcity → pricing power."
        ),
        trigger_signals=[
            "Supplier exits",
            "Industry consolidation",
            "Capacity closures",
        ],
        leading_indicators=[
            "Competitor capacity closures",
            "Industry utilisation",
            "Supplier profitability",
            "Industry capex discipline",
        ],
        confirmation_indicators=[
            "Reduced effective capacity",
            "Stable or rising utilisation",
            "Firm pricing",
        ],
        earnings_channels=[
            "Pricing",
            "Margins",
            "Utilisation",
            "ROCE",
        ],
        market_mistake=(
            "Market assumes displaced supply will quickly be "
            "replaced by new entrants."
        ),
        disconfirming_evidence=[
            "New entrants add capacity",
            "Existing competitors expand aggressively",
            "Pricing weakens",
        ],
        kill_switch=(
            "Competitive capacity returns rapidly enough to "
            "restore prior supply conditions."
        ),
        family=CatalystFamily.SUPPLY_CONSTRAINT,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-SUPPLY-CONSTRAINT-RAW-MATERIAL-SCARCITY"
        ),
        name=(
            "Raw Material Scarcity"
        ),
        description=(
            "Restricted availability of a critical input creates "
            "a supply constraint for downstream producers."
        ),
        mechanism=(
            "Input scarcity → constrained production → "
            "product availability → pricing power."
        ),
        trigger_signals=[
            "Critical input shortages",
            "Supplier allocation",
            "Input lead-time extension",
        ],
        leading_indicators=[
            "Raw material inventories",
            "Supplier allocation levels",
            "Input availability",
            "Commodity supply conditions",
        ],
        confirmation_indicators=[
            "Persistent input shortage",
            "Stable production despite constrained supply",
            "Firm downstream pricing",
        ],
        earnings_channels=[
            "Pricing",
            "Volume",
            "Margins",
        ],
        market_mistake=(
            "Market assumes alternative sourcing will quickly "
            "eliminate the input constraint."
        ),
        disconfirming_evidence=[
            "Alternative supply becomes available",
            "Input inventories recover",
            "Downstream demand weakens",
        ],
        kill_switch=(
            "Critical input availability normalises sufficiently "
            "to remove the downstream supply constraint."
        ),
        family=CatalystFamily.SUPPLY_CONSTRAINT,
    ),

    CatalystPattern(
        pattern_id=(
            "PAT-SUPPLY-CONSTRAINT-PRICING-POWER-INFLECTION"
        ),
        name=(
            "Scarcity-Driven Pricing Power Inflection"
        ),
        description=(
            "Persistent supply scarcity allows producers to "
            "increase prices faster than underlying demand growth."
        ),
        mechanism=(
            "Supply scarcity → bargaining power shift → "
            "price increases → margin expansion."
        ),
        trigger_signals=[
            "Price increases announced",
            "Discounting declines",
            "Supply remains constrained",
        ],
        leading_indicators=[
            "Spot prices",
            "Contract pricing",
            "Discount levels",
            "Utilisation",
        ],
        confirmation_indicators=[
            "Realisation growth",
            "Stable volumes",
            "Gross margin improvement",
        ],
        earnings_channels=[
            "Pricing",
            "Margins",
            "EPS",
            "ROIC",
        ],
        market_mistake=(
            "Market assumes pricing gains will reverse as soon "
            "as demand growth moderates."
        ),
        disconfirming_evidence=[
            "Pricing reverses",
            "Utilisation declines",
            "New capacity enters",
        ],
        kill_switch=(
            "Pricing power disappears because supply conditions "
            "normalise."
        ),
        family=CatalystFamily.SUPPLY_CONSTRAINT,
    ),
]


__all__ = [
    "SUPPLY_CONSTRAINT_PATTERNS",
]