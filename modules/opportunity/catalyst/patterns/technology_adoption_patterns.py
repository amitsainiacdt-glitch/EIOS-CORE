"""
EIOS
Everest Investment Operating System

Technology Adoption Catalyst Patterns

Purpose:
Canonical catalyst pattern definitions for technology adoption.

Design Principles:
- Definitions only.
- No scoring.
- No valuation.
- No ranking.
- No company-specific logic.
- No investment decision logic.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


TECHNOLOGY_ADOPTION_PATTERNS = [

    # ======================================================
    # 1. ADOPTION RAMP
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-TECH-ADOPTION-RAMP",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        name="Technology Adoption Ramp",
        description=(
            "A technology moves from early adoption toward broader "
            "mainstream customer adoption, creating an accelerating "
            "deployment cycle."
        ),
        trigger_signals=[
            "rising customer adoption rates",
            "increasing pilot-to-commercial conversion",
            "shortening customer decision cycles",
            "growing technology deployment volumes",
        ],
        mechanism=(
            "Increasing familiarity, improving economics, and "
            "demonstrated customer outcomes reduce adoption friction "
            "and expand the pool of willing adopters."
        ),
        transmission_channels=[
            "customer adoption",
            "deployment growth",
            "technology penetration",
            "ecosystem expansion",
        ],
        leading_indicators=[
            "pilot activity",
            "customer enquiries",
            "implementation pipeline",
            "technology trials",
        ],
        confirmation_indicators=[
            "commercial deployments",
            "adoption-rate acceleration",
            "repeat deployments",
            "customer reference growth",
        ],
        typical_time_horizon=(
            "12-36 months"
        ),
        earnings_channels=[
            "higher technology-related demand",
            "greater deployment activity",
            "larger addressable market",
        ],
        market_mistake=(
            "The market treats current adoption as a niche phenomenon "
            "and underestimates the speed of mainstream adoption."
        ),
        second_order_effects=[
            "supplier ecosystem expansion",
            "complementary product demand",
            "infrastructure investment",
            "industry learning effects",
        ],
        disconfirming_evidence=[
            "adoption rates plateau",
            "pilot conversion deteriorates",
            "customer economics fail to improve",
            "deployment timelines lengthen materially",
        ],
        kill_switch=(
            "Sustained evidence that mainstream customers are unwilling "
            "to adopt the technology despite improving availability "
            "and economics."
        ),
    ),


    # ======================================================
    # 2. ADOPTION PENETRATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-TECH-ADOPTION-PENETRATION",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        name="Technology Adoption Penetration",
        description=(
            "Technology penetration rises materially within an "
            "established addressable market, increasing the number "
            "of customers using the technology."
        ),
        trigger_signals=[
            "low initial penetration",
            "rising installed base",
            "increasing customer adoption percentage",
            "growing technology utilization across target segments",
        ],
        mechanism=(
            "The technology progresses deeper into an existing market "
            "as adoption barriers decline and more customers cross "
            "the economic or operational threshold for deployment."
        ),
        transmission_channels=[
            "penetration expansion",
            "installed-base growth",
            "customer conversion",
            "market deepening",
        ],
        leading_indicators=[
            "technology enquiries",
            "customer surveys",
            "installed-base additions",
            "deployment commitments",
        ],
        confirmation_indicators=[
            "penetration-rate increases",
            "installed-base acceleration",
            "higher customer conversion",
            "broader segment adoption",
        ],
        typical_time_horizon=(
            "12-48 months"
        ),
        earnings_channels=[
            "larger customer base",
            "higher deployment demand",
            "greater recurring usage opportunity",
        ],
        market_mistake=(
            "The market extrapolates current penetration too conservatively "
            "and fails to recognize the remaining adoption runway."
        ),
        second_order_effects=[
            "lower customer acquisition friction",
            "greater ecosystem investment",
            "improved technology familiarity",
            "network effects in adoption",
        ],
        disconfirming_evidence=[
            "penetration stalls",
            "addressable customer pool proves smaller than expected",
            "customer conversion rates decline",
            "economic barriers remain persistent",
        ],
        kill_switch=(
            "Evidence that technology penetration has structurally "
            "reached a ceiling well below the assumed adoption runway."
        ),
    ),


    # ======================================================
    # 3. TECHNOLOGY REPLACEMENT
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-TECH-ADOPTION-REPLACEMENT",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        name="Technology Replacement",
        description=(
            "Customers begin replacing an incumbent technology, "
            "process, or architecture with a newer technology."
        ),
        trigger_signals=[
            "replacement projects",
            "incumbent technology obsolescence",
            "customer migration programs",
            "increasing technology conversion activity",
        ],
        mechanism=(
            "A newer technology delivers sufficient economic, "
            "performance, regulatory, or operational advantages "
            "to justify replacement of the incumbent solution."
        ),
        transmission_channels=[
            "technology migration",
            "replacement demand",
            "new installation cycle",
            "customer conversion",
        ],
        leading_indicators=[
            "replacement budgets",
            "migration announcements",
            "technology qualification",
            "customer trials",
        ],
        confirmation_indicators=[
            "commercial replacement orders",
            "accelerating migration",
            "declining incumbent installations",
            "higher replacement share",
        ],
        typical_time_horizon=(
            "18-60 months"
        ),
        earnings_channels=[
            "replacement demand",
            "new technology deployments",
            "larger customer programs",
        ],
        market_mistake=(
            "The market assumes incumbent technologies will retain "
            "their installed base for longer than is actually possible."
        ),
        second_order_effects=[
            "accelerated installed-base turnover",
            "supplier qualification shifts",
            "new ecosystem formation",
            "incumbent asset impairment",
        ],
        disconfirming_evidence=[
            "replacement economics weaken",
            "customers extend incumbent asset lives",
            "migration projects are delayed",
            "incumbent technology remains materially superior",
        ],
        kill_switch=(
            "Evidence that customers are systematically deferring "
            "replacement and extending the economic life of incumbent "
            "technology."
        ),
    ),


    # ======================================================
    # 4. TECHNOLOGY STANDARDIZATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-TECH-ADOPTION-STANDARDIZATION",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        name="Technology Standardization",
        description=(
            "An emerging technology gains broad industry acceptance "
            "as a preferred or standardized architecture, reducing "
            "adoption uncertainty."
        ),
        trigger_signals=[
            "industry standards emerging",
            "major customers adopting common architecture",
            "supplier certification",
            "interoperability improvements",
        ],
        mechanism=(
            "Standardization reduces technology uncertainty, "
            "compatibility concerns, implementation risk, and "
            "fragmentation, making adoption easier for additional users."
        ),
        transmission_channels=[
            "adoption acceleration",
            "qualification expansion",
            "ecosystem compatibility",
            "implementation simplification",
        ],
        leading_indicators=[
            "standards-body activity",
            "large-customer endorsements",
            "certification programs",
            "interoperability initiatives",
        ],
        confirmation_indicators=[
            "widespread standard adoption",
            "supplier certification growth",
            "common architecture deployment",
            "reduced implementation friction",
        ],
        typical_time_horizon=(
            "18-48 months"
        ),
        earnings_channels=[
            "broader technology adoption",
            "larger qualified customer pool",
            "higher deployment activity",
        ],
        market_mistake=(
            "The market underestimates how standardization can convert "
            "technology uncertainty into rapid mainstream adoption."
        ),
        second_order_effects=[
            "supplier ecosystem growth",
            "lower implementation costs",
            "faster customer qualification",
            "complementary technology investment",
        ],
        disconfirming_evidence=[
            "competing standards persist",
            "interoperability remains poor",
            "major customers reject standardization",
            "certification activity stalls",
        ],
        kill_switch=(
            "Persistent fragmentation between competing standards "
            "prevents the technology from becoming a broadly accepted "
            "industry architecture."
        ),
    ),


    # ======================================================
    # 5. ECOSYSTEM RAMP
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-TECH-ADOPTION-ECOSYSTEM-RAMP",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        name="Technology Ecosystem Ramp",
        description=(
            "Supporting infrastructure, software, suppliers, "
            "service providers, and ecosystem participants mature "
            "enough to remove bottlenecks to technology adoption."
        ),
        trigger_signals=[
            "infrastructure build-out",
            "supplier ecosystem expansion",
            "support-service availability",
            "complementary software growth",
        ],
        mechanism=(
            "Technology adoption accelerates when complementary "
            "components and infrastructure become sufficiently "
            "available, reliable, and scalable."
        ),
        transmission_channels=[
            "deployment enablement",
            "ecosystem expansion",
            "implementation capacity",
            "customer confidence",
        ],
        leading_indicators=[
            "supplier additions",
            "infrastructure commitments",
            "ecosystem partnerships",
            "service-provider expansion",
        ],
        confirmation_indicators=[
            "ecosystem capacity growth",
            "shorter implementation timelines",
            "higher deployment throughput",
            "increased customer adoption",
        ],
        typical_time_horizon=(
            "12-48 months"
        ),
        earnings_channels=[
            "higher technology deployments",
            "greater ecosystem demand",
            "increased implementation activity",
        ],
        market_mistake=(
            "The market focuses on the technology itself while "
            "underestimating the importance of ecosystem maturity "
            "as the actual adoption bottleneck."
        ),
        second_order_effects=[
            "faster deployment cycles",
            "lower implementation risk",
            "new complementary products",
            "greater customer confidence",
        ],
        disconfirming_evidence=[
            "infrastructure remains constrained",
            "supplier shortages persist",
            "ecosystem investment slows",
            "implementation bottlenecks worsen",
        ],
        kill_switch=(
            "Critical ecosystem bottlenecks remain unresolved despite "
            "continued demand for the underlying technology."
        ),
    ),


    # ======================================================
    # 6. COST-PARITY ADOPTION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-TECH-ADOPTION-COST-PARITY",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        name="Technology Cost-Parity Adoption",
        description=(
            "A technology reaches economic parity or superiority "
            "versus an incumbent solution, materially lowering the "
            "economic barrier to adoption."
        ),
        trigger_signals=[
            "technology cost declines",
            "total cost of ownership improvement",
            "productivity gains",
            "incumbent cost inflation",
        ],
        mechanism=(
            "Improving technology economics move adoption from "
            "strategic experimentation toward economically rational "
            "mainstream deployment."
        ),
        transmission_channels=[
            "lower adoption barriers",
            "customer ROI improvement",
            "technology substitution",
            "deployment acceleration",
        ],
        leading_indicators=[
            "cost curves",
            "customer ROI calculations",
            "technology efficiency gains",
            "component cost declines",
        ],
        confirmation_indicators=[
            "customer payback periods improve",
            "technology reaches cost parity",
            "commercial adoption accelerates",
            "incumbent substitution increases",
        ],
        typical_time_horizon=(
            "12-48 months"
        ),
        earnings_channels=[
            "higher adoption",
            "larger deployment opportunity",
            "faster customer conversion",
        ],
        market_mistake=(
            "The market values the technology using historical economics "
            "and fails to recognize that falling costs have crossed "
            "the threshold for mass adoption."
        ),
        second_order_effects=[
            "accelerated customer migration",
            "supplier capacity expansion",
            "new applications becoming economical",
            "faster ecosystem investment",
        ],
        disconfirming_evidence=[
            "cost reductions fail to materialize",
            "customer ROI remains unattractive",
            "incumbent economics improve faster",
            "adoption does not respond to improved economics",
        ],
        kill_switch=(
            "The technology fails to achieve the assumed economic "
            "threshold and remains structurally uneconomic versus "
            "the incumbent solution."
        ),
    ),
]


__all__ = [
    "TECHNOLOGY_ADOPTION_PATTERNS",
]