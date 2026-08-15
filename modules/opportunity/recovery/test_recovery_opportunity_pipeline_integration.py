"""
EIOS
Everest Investment Operating System

Recovery Opportunity → Opportunity Pipeline Integration Test

Purpose
-------
Proves that Recovery Opportunity Intelligence can enter the
existing Opportunity Pipeline through the canonical Signal
boundary.

Architecture:

Recovery Opportunity Signal
        ↓
Recovery Opportunity Adapter
        ↓
Canonical Opportunity Signal
        ↓
OpportunityPipeline
        ↓
Catalyst
        ↓
Expectation Gap
        ↓
Mispricing
        ↓
Asymmetry
        ↓
Evidence
        ↓
Synthesis

This test does NOT modify the existing Opportunity Pipeline.
"""

from copy import deepcopy
from dataclasses import dataclass

from modules.opportunity.opportunity_pipeline import (
    OpportunityPipeline,
)

from modules.opportunity.asymmetry_engine import (
    AsymmetryScenario,
)

from modules.opportunity.evidence_engine import (
    EvidenceItem,
    KillSwitch,
)

from modules.opportunity.recovery.recovery_opportunity_adapter import (
    RecoveryOpportunityAdapter,
)

from modules.opportunity.recovery.recovery_opportunity_signal import (
    RecoveryOpportunitySignal,
    RecoveryOpportunityStage,
    RecoveryOpportunityDirection,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDirection,
    SignalStage,
)


# ==========================================================
# TEST VALUATION
# ==========================================================


@dataclass
class TestValuation:

    intrinsic_value: float = 4518.65

    fair_value: float = 4518.65

    confidence: float = 85.0


# ==========================================================
# RECOVERY SIGNAL FACTORY
# ==========================================================


def make_recovery_signal() -> RecoveryOpportunitySignal:
    """
    Create deterministic Recovery Opportunity Intelligence
    for end-to-end pipeline testing.
    """

    signal = RecoveryOpportunitySignal()

    signal.signal_id = (
        "REC-PIPELINE::001"
    )

    signal.theme_id = (
        "THEME::INDUSTRIAL-RECOVERY"
    )

    signal.theme_name = (
        "Industrial Capital Recovery"
    )

    signal.recovery_breadth = 80.0

    signal.confirmed_recovery_breadth = 60.0

    signal.recovery_confidence = 85.0

    signal.recovery_coherence = 75.0

    signal.temporal_support = 75.0

    signal.persistence_score = 70.0

    signal.contradiction_score = 10.0

    signal.catalyst_count = 2

    signal.catalyst_confidence = 85.0

    signal.catalyst_strength = 80.0

    signal.catalyst_coherence = 75.0

    signal.catalyst_supported = True

    signal.broad_recovery_supported = True

    signal.confirmed_recovery_supported = True

    signal.direction = (
        RecoveryOpportunityDirection.POSITIVE
    )

    signal.stage = (
        RecoveryOpportunityStage.ACTIONABLE
    )

    signal.opportunity_ready = True

    signal.requires_more_evidence = False

    signal.catalyst_families = [
        "CAPACITY_EXPANSION",
    ]

    signal.catalyst_patterns = [
        "NEW_CAPACITY_ONLINE",
    ]

    signal.evidence_sources = [
        "Primary industry evidence",
        "Company disclosure",
    ]

    signal.supporting_evidence = [
        "Industrial demand recovery",
        "Capacity expansion",
        "Improving utilisation",
    ]

    signal.contradictory_evidence = []

    return signal


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    company = (
        "RECOVERY TEST INDUSTRIAL COMPANY"
    )

    sector = "Industrial"

    cmp = 3500.0

    # ======================================================
    # 1. ADAPTER
    # ======================================================

    adapter = RecoveryOpportunityAdapter()

    assert adapter is not None

    print(
        "Recovery Adapter Exists         : PASS"
    )

    # ======================================================
    # 2. RECOVERY SIGNAL
    # ======================================================

    recovery_signal = (
        make_recovery_signal()
    )

    recovery_copy = deepcopy(
        recovery_signal
    )

    canonical_signal = (
        adapter.create_signal(
            recovery_signal
        )
    )

    assert isinstance(
        canonical_signal,
        Signal,
    )

    print(
        "Canonical Signal Creation       : PASS"
    )

    # ======================================================
    # 3. RECOVERY INPUT IMMUTABILITY
    # ======================================================

    assert (
        recovery_signal
        == recovery_copy
    )

    print(
        "Recovery Input Immutability     : PASS"
    )

    # ======================================================
    # 4. CANONICAL SIGNAL VALIDATION
    # ======================================================

    assert (
        canonical_signal.direction
        == SignalDirection.POSITIVE
    )

    assert (
        canonical_signal.stage
        == SignalStage.CATALYST
    )

    assert (
        canonical_signal.confidence
        == 85.0
    )

    assert (
        len(canonical_signal.evidence)
        >= 1
    )

    print(
        "Canonical Recovery Signal       : PASS"
    )

    # ======================================================
    # 5. ASYMMETRY SCENARIOS
    # ======================================================

    scenarios = [

        AsymmetryScenario(

            name="Bull",

            probability=35.0,

            return_percent=100.0,

            time_months=24,

            permanent_loss=False,

            rationale=(
                "Broad industrial recovery "
                "and capacity expansion."
            ),
        ),

        AsymmetryScenario(

            name="Base",

            probability=50.0,

            return_percent=35.0,

            time_months=30,

            permanent_loss=False,

            rationale=(
                "Recovery continues at a "
                "moderate pace."
            ),
        ),

        AsymmetryScenario(

            name="Bear",

            probability=15.0,

            return_percent=-20.0,

            time_months=24,

            permanent_loss=False,

            rationale=(
                "Recovery moderates but the "
                "business remains viable."
            ),
        ),
    ]

    # ======================================================
    # 6. SUPPORTING EVIDENCE
    # ======================================================

    supporting_evidence = [

        EvidenceItem(

            evidence_id="REC-EVID-001",

            statement=(
                "Broad industrial recovery is "
                "supported by multiple indicators."
            ),

            source=(
                "Primary industry evidence"
            ),

            category="Industry",

            direction="Supporting",

            strength=90.0,

            confidence=95.0,

            independent_confirmation=2,

            is_primary_source=True,

            is_time_sensitive=True,

            notes=(
                "Recovery breadth evidence."
            ),
        ),

        EvidenceItem(

            evidence_id="REC-EVID-002",

            statement=(
                "Company order activity confirms "
                "improving industrial demand."
            ),

            source="Company disclosure",

            category="Company",

            direction="Supporting",

            strength=90.0,

            confidence=90.0,

            independent_confirmation=2,

            is_primary_source=True,

            is_time_sensitive=True,

            notes=(
                "Direct company evidence."
            ),
        ),

        EvidenceItem(

            evidence_id="REC-EVID-003",

            statement=(
                "Peer companies report similar "
                "demand improvement."
            ),

            source="Peer disclosures",

            category="Competitive",

            direction="Supporting",

            strength=85.0,

            confidence=85.0,

            independent_confirmation=2,

            is_primary_source=False,

            is_time_sensitive=True,

            notes=(
                "Independent confirmation."
            ),
        ),
    ]

    # ======================================================
    # 7. CONTRADICTORY EVIDENCE
    # ======================================================

    contradictory_evidence = [

        EvidenceItem(

            evidence_id="REC-EVID-004",

            statement=(
                "Some end-market uncertainty remains."
            ),

            source="Industry commentary",

            category="Risk",

            direction="Contradictory",

            strength=60.0,

            confidence=75.0,

            independent_confirmation=1,

            is_primary_source=False,

            is_time_sensitive=True,

            notes=(
                "Relevant but not thesis-breaking."
            ),
        ),
    ]

    # ======================================================
    # 8. ASSUMPTIONS
    # ======================================================

    assumptions = [

        "Industrial recovery remains broad.",

        "Company captures incremental demand.",

        "Capacity utilisation continues improving.",
    ]

    invalidation_conditions = [

        "Recovery breadth contracts materially.",

        "Catalyst evidence deteriorates.",

        "Order growth reverses materially.",
    ]

    # ======================================================
    # 9. KILL SWITCHES
    # ======================================================

    kill_switches = [

        KillSwitch(

            name="Recovery Breadth Reversal",

            condition=(
                "Industrial recovery breadth "
                "contracts materially."
            ),

            severity="High",

            measurable=True,

            threshold=(
                "Recovery breadth below "
                "established threshold"
            ),

            monitoring_frequency="Quarterly",

            rationale=(
                "Would invalidate the "
                "recovery thesis."
            ),

            triggered=False,
        ),
    ]

    # ======================================================
    # 10. PIPELINE
    # ======================================================

    pipeline = OpportunityPipeline()

    assert pipeline is not None

    print(
        "Opportunity Pipeline Exists     : PASS"
    )

    # ======================================================
    # 11. RUN
    # ======================================================

    result = pipeline.run(

        company=company,

        sector=sector,

        cmp=cmp,

        signals=[
            canonical_signal
        ],

        causal_chain=None,

        catalyst_id=(
            "CAT::RECOVERY::001"
        ),

        catalyst_title=(
            "Industrial Recovery Catalyst"
        ),

        catalyst_trigger=(
            "Broad industrial recovery "
            "supported by capacity expansion."
        ),

        market_expectation=45.0,

        eios_expectation=80.0,

        market_earnings_expectation=40.0,

        eios_earnings_expectation=75.0,

        valuation=TestValuation(),

        asymmetry_scenarios=scenarios,

        supporting_evidence=(
            supporting_evidence
        ),

        contradictory_evidence=(
            contradictory_evidence
        ),

        assumptions=assumptions,

        kill_switches=kill_switches,

        monitoring_signals=[

            "Recovery breadth",

            "Industrial order growth",

            "Capacity utilisation",

        ],

        invalidation_conditions=(
            invalidation_conditions
        ),

        affected_sectors=[
            "Industrial"
        ],

        affected_companies=[
            company
        ],

        description=(
            "Recovery-derived Opportunity "
            "Pipeline integration test."
        ),

        economic_impact=(
            "Broadening industrial demand "
            "and improving utilisation."
        ),

        earnings_impact=(
            "Potential earnings acceleration "
            "from recovery."
        ),

        valuation_impact=(
            "Potential intrinsic-value realization "
            "as recovery becomes recognized."
        ),
    )

    # ======================================================
    # 12. CATALYST
    # ======================================================

    assert result.catalyst is not None

    print(
        "Recovery → Catalyst              : PASS"
    )

    # ======================================================
    # 13. SIGNAL PRESERVATION
    # ======================================================

    assert (
        len(result.catalyst.signals)
        == 1
    )

    assert (
        result.catalyst.signals[0]
        == canonical_signal
    )

    assert (
        result.catalyst.direction
        == SignalDirection.POSITIVE
    )

    print(
        "Signal → Catalyst                : PASS"
    )

    # ======================================================
    # 14. EXPECTATION GAP
    # ======================================================

    assert (
        result.expectation_gap
        is not None
    )

    print(
        "Catalyst → Expectation Gap       : PASS"
    )

    # ======================================================
    # 15. MISPRICING
    # ======================================================

    assert (
        result.mispricing
        is not None
    )

    print(
        "Expectation Gap → Mispricing     : PASS"
    )

    # ======================================================
    # 16. ASYMMETRY
    # ======================================================

    assert (
        result.asymmetry
        is not None
    )

    print(
        "Mispricing → Asymmetry            : PASS"
    )

    # ======================================================
    # 17. EVIDENCE
    # ======================================================

    assert (
        result.evidence
        is not None
    )

    print(
        "Asymmetry → Evidence              : PASS"
    )

    # ======================================================
    # 18. SYNTHESIS
    # ======================================================

    assert (
        result.synthesis
        is not None
    )

    print(
        "Evidence → Synthesis              : PASS"
    )

    # ======================================================
    # 19. EVIDENCE HAND-OFF
    # ======================================================

    assert (
        result.synthesis.evidence_score
        == result.evidence.evidence_score
    )

    assert (
        result.synthesis.evidence_confidence
        == result.evidence.confidence
    )

    print(
        "Evidence Handoff                  : PASS"
    )

    # ======================================================
    # 20. SCORE RANGE
    # ======================================================

    assert (
        0.0
        <= result.synthesis.opportunity_score
        <= 100.0
    )

    assert (
        0.0
        <= result.synthesis.confidence
        <= 100.0
    )

    print(
        "Synthesis Score Range             : PASS"
    )

    # ======================================================
    # 21. CANONICAL SIGNAL IMMUTABILITY
    # ======================================================

    assert (
        canonical_signal.direction
        == SignalDirection.POSITIVE
    )

    assert (
        canonical_signal.stage
        == SignalStage.CATALYST
    )

    assert (
        canonical_signal.confidence
        == 85.0
    )

    print(
        "Canonical Signal Immutability     : PASS"
    )

    # ======================================================
    # 22. DETERMINISM
    # ======================================================

    second_recovery = (
        make_recovery_signal()
    )

    second_signal = (
        adapter.create_signal(
            second_recovery
        )
    )

    second_result = pipeline.run(

        company=company,

        sector=sector,

        cmp=cmp,

        signals=[
            second_signal
        ],

        causal_chain=None,

        catalyst_id=(
            "CAT::RECOVERY::001"
        ),

        catalyst_title=(
            "Industrial Recovery Catalyst"
        ),

        catalyst_trigger=(
            "Broad industrial recovery "
            "supported by capacity expansion."
        ),

        market_expectation=45.0,

        eios_expectation=80.0,

        market_earnings_expectation=40.0,

        eios_earnings_expectation=75.0,

        valuation=TestValuation(),

        asymmetry_scenarios=scenarios,

        supporting_evidence=(
            supporting_evidence
        ),

        contradictory_evidence=(
            contradictory_evidence
        ),

        assumptions=assumptions,

        kill_switches=kill_switches,

        monitoring_signals=[

            "Recovery breadth",

            "Industrial order growth",

            "Capacity utilisation",

        ],

        invalidation_conditions=(
            invalidation_conditions
        ),

        affected_sectors=[
            "Industrial"
        ],

        affected_companies=[
            company
        ],

        description=(
            "Recovery-derived Opportunity "
            "Pipeline integration test."
        ),

        economic_impact=(
            "Broadening industrial demand "
            "and improving utilisation."
        ),

        earnings_impact=(
            "Potential earnings acceleration "
            "from recovery."
        ),

        valuation_impact=(
            "Potential intrinsic-value realization "
            "as recovery becomes recognized."
        ),
    )

    assert (
        result.synthesis.opportunity_score
        == second_result.synthesis.opportunity_score
    )

    assert (
        result.synthesis.confidence
        == second_result.synthesis.confidence
    )

    assert (
        result.catalyst.catalyst_score
        == second_result.catalyst.catalyst_score
    )

    print(
        "Deterministic Pipeline             : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY → OPPORTUNITY PIPELINE "
        ": PASS"
    )


if __name__ == "__main__":
    main()