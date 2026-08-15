"""
EIOS
Everest Investment Operating System

Competitive Exit Catalyst Patterns

Purpose:
Canonical passive pattern definitions for the
Competitive Exit catalyst family.

Design Principles:

- Passive data only.
- No analysis.
- No scoring.
- No ranking.
- No valuation.
- No company-specific logic.
- All patterns belong to CatalystFamily.COMPETITIVE_EXIT.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# COMPETITIVE EXIT PATTERNS
# ==========================================================

COMPETITIVE_EXIT_PATTERNS = [

    # ------------------------------------------------------
    # 1. COMPETITOR PLANT CLOSURE
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMPETITIVE-EXIT-PLANT-CLOSURE"
        ),
        name=(
            "Competitor Plant Closure"
        ),
        description=(
            "A competitor permanently closes production "
            "capacity, reducing industry supply and creating "
            "an opportunity for surviving producers."
        ),
        mechanism=(
            "Competitor closure → capacity removal → "
            "supply rationalisation → share/pricing opportunity."
        ),
        trigger_signals=[
            "Competitor plant closure announcement",
            "Permanent production shutdown",
            "Asset impairment or closure disclosure",
            "Exit from a product line",
        ],
        leading_indicators=[
            "Persistent competitor losses",
            "Low utilisation at competitor facilities",
            "Maintenance deferrals",
            "Capacity rationalisation announcements",
        ],
        confirmation_indicators=[
            "Industry capacity declines",
            "Competitor production volumes fall",
            "Customer migration to surviving suppliers",
            "Improved industry utilisation",
        ],
        earnings_channels=[
            "Market Share",
            "Pricing",
            "Margins",
        ],
        market_mistake=(
            "Market treats the closure as temporary rather than "
            "recognising permanent industry capacity removal."
        ),
        disconfirming_evidence=[
            "Closed capacity is restarted",
            "Equivalent replacement capacity appears",
            "Industry demand deteriorates materially",
            "Customers do not migrate to surviving producers",
        ],
        kill_switch=(
            "Competitor capacity returns or equivalent new capacity "
            "fully offsets the closure."
        ),
        family=CatalystFamily.COMPETITIVE_EXIT,
    ),

    # ------------------------------------------------------
    # 2. FINANCIALLY DISTRESSED COMPETITOR EXIT
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMPETITIVE-EXIT-FINANCIAL-DISTRESS"
        ),
        name=(
            "Financially Distressed Competitor Exit"
        ),
        description=(
            "A financially stressed competitor becomes "
            "economically unviable and withdraws capacity "
            "from the market."
        ),
        mechanism=(
            "Financial stress → economic unviability → "
            "capacity withdrawal → industry rationalisation."
        ),
        trigger_signals=[
            "Repeated competitor losses",
            "Debt servicing stress",
            "Liquidity deterioration",
            "Credit-rating deterioration",
        ],
        leading_indicators=[
            "Negative free cash flow",
            "Rising leverage",
            "Working-capital stress",
            "Asset sales",
        ],
        confirmation_indicators=[
            "Capacity shutdown",
            "Business discontinuation",
            "Debt restructuring",
            "Customer migration",
        ],
        earnings_channels=[
            "Market Share",
            "Pricing",
            "Margins",
        ],
        market_mistake=(
            "Market assumes financially weak competitors will "
            "continue operating indefinitely despite poor economics."
        ),
        disconfirming_evidence=[
            "Competitor receives substantial capital",
            "Debt is successfully refinanced",
            "Competitor returns to profitability",
            "Capacity remains operational",
        ],
        kill_switch=(
            "Competitor secures sufficient capital to remain "
            "economically viable and maintain capacity."
        ),
        family=CatalystFamily.COMPETITIVE_EXIT,
    ),

    # ------------------------------------------------------
    # 3. INDUSTRY CONSOLIDATION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMPETITIVE-EXIT-INDUSTRY-CONSOLIDATION"
        ),
        name=(
            "Industry Consolidation"
        ),
        description=(
            "Competitor exits, mergers, or acquisitions reduce "
            "the number of economically viable industry participants."
        ),
        mechanism=(
            "Industry consolidation → fewer competitors → "
            "greater supply discipline → pricing/margin opportunity."
        ),
        trigger_signals=[
            "Competitor mergers",
            "Industry acquisitions",
            "Business exits",
            "Capacity rationalisation",
        ],
        leading_indicators=[
            "Weak competitor profitability",
            "Increasing consolidation activity",
            "Low industry returns",
            "Rising distressed asset transactions",
        ],
        confirmation_indicators=[
            "Reduced competitor count",
            "Lower industry capacity growth",
            "Improved pricing discipline",
            "Higher utilisation among survivors",
        ],
        earnings_channels=[
            "Market Share",
            "Pricing",
            "Margins",
        ],
        market_mistake=(
            "Market focuses on near-term consolidation headlines "
            "and misses the structural improvement in industry economics."
        ),
        disconfirming_evidence=[
            "New competitors enter rapidly",
            "Consolidation does not reduce capacity",
            "Pricing remains irrational",
            "Industry returns fail to improve",
        ],
        kill_switch=(
            "Consolidation fails to reduce effective industry "
            "capacity or competitive intensity."
        ),
        family=CatalystFamily.COMPETITIVE_EXIT,
    ),

    # ------------------------------------------------------
    # 4. PRODUCT-LINE EXIT
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMPETITIVE-EXIT-PRODUCT-LINE-EXIT"
        ),
        name=(
            "Competitor Product-Line Exit"
        ),
        description=(
            "A competitor withdraws from a product category, "
            "leaving customers and demand available to remaining suppliers."
        ),
        mechanism=(
            "Competitor product exit → customer displacement → "
            "surviving supplier share gains → revenue growth."
        ),
        trigger_signals=[
            "Product discontinuation",
            "Competitor withdrawal from category",
            "SKU rationalisation",
            "Reduced competitor product availability",
        ],
        leading_indicators=[
            "Declining competitor investment",
            "Longer competitor lead times",
            "Reduced sales coverage",
            "Lower product development activity",
        ],
        confirmation_indicators=[
            "Customer migration",
            "New customer wins",
            "Higher supplier volumes",
            "Improved category share",
        ],
        earnings_channels=[
            "Market Share",
            "Revenue Growth",
            "Margins",
        ],
        market_mistake=(
            "Market underestimates the persistence of customer "
            "migration following a competitor product exit."
        ),
        disconfirming_evidence=[
            "Customers switch to alternative competitors",
            "Exited product returns",
            "Demand for the category contracts materially",
            "Company fails to capture displaced demand",
        ],
        kill_switch=(
            "Displaced customers do not migrate to the company "
            "or the competitor re-enters the product category."
        ),
        family=CatalystFamily.COMPETITIVE_EXIT,
    ),

    # ------------------------------------------------------
    # 5. REGIONAL COMPETITOR EXIT
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMPETITIVE-EXIT-REGIONAL-EXIT"
        ),
        name=(
            "Regional Competitor Exit"
        ),
        description=(
            "A competitor exits a geographic market, creating "
            "a concentrated opportunity for established local suppliers."
        ),
        mechanism=(
            "Regional competitor exit → local supply reduction → "
            "customer migration → regional share gain."
        ),
        trigger_signals=[
            "Regional facility closure",
            "Geographic market withdrawal",
            "Distribution network shutdown",
            "Local sales-force reduction",
        ],
        leading_indicators=[
            "Regional losses",
            "Distribution inefficiency",
            "Reduced local inventory",
            "Competitor service deterioration",
        ],
        confirmation_indicators=[
            "Local customer wins",
            "Regional volume growth",
            "Higher utilisation",
            "Improved regional pricing",
        ],
        earnings_channels=[
            "Market Share",
            "Volume",
            "Pricing",
        ],
        market_mistake=(
            "Market views the competitor exit as geographically "
            "limited and fails to recognise the earnings impact "
            "on the company's exposed region."
        ),
        disconfirming_evidence=[
            "Alternative competitor fills the gap",
            "Customers leave the region",
            "Regional demand contracts",
            "Company fails to gain share",
        ],
        kill_switch=(
            "Another competitor immediately replaces the exited "
            "capacity without improving the company's competitive position."
        ),
        family=CatalystFamily.COMPETITIVE_EXIT,
    ),

    # ------------------------------------------------------
    # 6. STRUCTURAL COMPETITIVE EXIT
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-COMPETITIVE-EXIT-STRUCTURAL-RATIONALISATION"
        ),
        name=(
            "Structural Competitive Rationalisation"
        ),
        description=(
            "A prolonged deterioration in competitor economics "
            "causes permanent industry exits and structurally "
            "reduces competitive intensity."
        ),
        mechanism=(
            "Poor competitor economics → permanent exits → "
            "lower structural competition → stronger pricing "
            "and returns for surviving companies."
        ),
        trigger_signals=[
            "Multi-year competitor losses",
            "Persistent excess capacity",
            "Permanent asset closures",
            "Industry consolidation",
        ],
        leading_indicators=[
            "Sub-economic competitor returns",
            "Repeated capacity shutdowns",
            "Declining competitor investment",
            "Rising distressed asset sales",
        ],
        confirmation_indicators=[
            "Industry capacity permanently declines",
            "Competitive intensity falls",
            "Pricing discipline improves",
            "ROCE improves for surviving companies",
        ],
        earnings_channels=[
            "Market Share",
            "Pricing",
            "Margins",
            "ROCE",
        ],
        market_mistake=(
            "Market assumes cyclical industry weakness will "
            "eventually restore the old competitive structure."
        ),
        disconfirming_evidence=[
            "New capacity enters at competitive economics",
            "Competitors restore profitability",
            "Industry capacity expands materially",
            "Pricing discipline deteriorates",
        ],
        kill_switch=(
            "Competitive capacity returns sufficiently to restore "
            "the previous level of industry competition."
        ),
        family=CatalystFamily.COMPETITIVE_EXIT,
    ),
]


# ==========================================================
# EXPORT
# ==========================================================

__all__ = [
    "COMPETITIVE_EXIT_PATTERNS",
]