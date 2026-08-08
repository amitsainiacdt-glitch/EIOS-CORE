"""
EIOS
Everest Investment Operating System

Opportunity Pipeline
End-to-End Integration Test
"""

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

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
    SignalStage,
    TimeHorizon,
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
# MAIN
# ==========================================================


def main() -> None:

    print()
    print("=" * 60)
    print("EIOS OPPORTUNITY PIPELINE TEST")
    print("=" * 60)

    # ======================================================
    # BASIC COMPANY DATA
    # ======================================================

    company = "TEST INDUSTRIAL COMPANY"

    sector = "Industrial"

    cmp = 3500.0

    # ======================================================
    # CANONICAL EIOS SIGNAL
    # ======================================================

    signal = Signal(

        signal_id="SIG-001",

        title=(
            "Industrial Capex Acceleration"
        ),

        description=(
            "Industrial capital expenditure "
            "is accelerating."
        ),

        domain=SignalDomain.MACRO,

        signal_type=SignalType.ACCELERATION,

        direction=SignalDirection.POSITIVE,

        stage=SignalStage.VALIDATED,

        horizon=TimeHorizon.MEDIUM_TERM,

        source=(
            "Primary industry evidence"
        ),

        source_type="Primary",

        sectors=[
            "Industrial"
        ],

        companies=[
            company
        ],

        themes=[
            "Industrial Capex",
            "Capital Cycle",
        ],

        economic_mechanism=(
            "Higher industrial investment "
            "increases demand."
        ),

        supply_demand_impact=(
            "Demand is improving."
        ),

        earnings_impact=(
            "Potential earnings acceleration."
        ),
    )

    signals = [
        signal
    ]

    print(
        "Canonical Signal        : PASS"
    )

    # ======================================================
    # ASSUMPTIONS
    # ======================================================

    assumptions = [

        "Industrial capex remains elevated.",

        "Company captures incremental demand.",

        "Margins remain within historical range.",
    ]

    invalidation_conditions = [

        "Industrial capex materially reverses.",

        "Order growth deteriorates materially.",
    ]

    # ======================================================
    # ASYMMETRY SCENARIOS
    # ======================================================

    scenarios = [

        AsymmetryScenario(

            name="Bull",

            probability=35.0,

            return_percent=100.0,

            time_months=24,

            permanent_loss=False,

            rationale=(
                "Strong capex cycle and "
                "earnings acceleration."
            ),
        ),

        AsymmetryScenario(

            name="Base",

            probability=50.0,

            return_percent=35.0,

            time_months=30,

            permanent_loss=False,

            rationale=(
                "Moderate earnings improvement."
            ),
        ),

        AsymmetryScenario(

            name="Bear",

            probability=15.0,

            return_percent=-20.0,

            time_months=24,

            permanent_loss=False,

            rationale=(
                "Capex cycle moderates but "
                "business remains viable."
            ),
        ),
    ]

    # ======================================================
    # SUPPORTING EVIDENCE
    # ======================================================

    supporting_evidence = [

        EvidenceItem(

            evidence_id="EVID-001",

            statement=(
                "Primary evidence confirms "
                "accelerating industrial capex."
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
                "Core catalyst evidence."
            ),
        ),

        EvidenceItem(

            evidence_id="EVID-002",

            statement=(
                "Company order activity confirms "
                "stronger industrial demand."
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

            evidence_id="EVID-003",

            statement=(
                "Peer companies report similar "
                "demand acceleration."
            ),

            source="Peer disclosures",

            category="Competitive",

            direction="Supporting",

            strength=85.0,

            confidence=85.0,

            independent_confirmation=2,

            is_primary_source=True,

            is_time_sensitive=True,

            notes=(
                "Independent confirmation."
            ),
        ),

        EvidenceItem(

            evidence_id="EVID-004",

            statement=(
                "Capacity expansion supports "
                "durability of the demand cycle."
            ),

            source="Industry research",

            category="Industry",

            direction="Supporting",

            strength=85.0,

            confidence=85.0,

            independent_confirmation=1,

            is_primary_source=False,

            is_time_sensitive=True,

            notes=(
                "Supports catalyst duration."
            ),
        ),

        EvidenceItem(

            evidence_id="EVID-005",

            statement=(
                "Management commentary confirms "
                "improving order visibility."
            ),

            source="Company disclosure",

            category="Management",

            direction="Supporting",

            strength=90.0,

            confidence=90.0,

            independent_confirmation=2,

            is_primary_source=True,

            is_time_sensitive=True,

            notes=(
                "Management confirmation."
            ),
        ),
    ]

    # ======================================================
    # CONTRADICTORY EVIDENCE
    # ======================================================

    contradictory_evidence = [

        EvidenceItem(

            evidence_id="EVID-006",

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
    # KILL SWITCH
    # ======================================================

    kill_switches = [

        KillSwitch(

            name="Capex Cycle Reversal",

            condition=(
                "Industrial capex declines materially "
                "for multiple periods."
            ),

            severity="High",

            measurable=True,

            threshold=(
                "Capex decline for two consecutive periods"
            ),

            monitoring_frequency="Quarterly",

            rationale=(
                "Would invalidate the central catalyst."
            ),

            triggered=False,
        ),
    ]

    # ======================================================
    # RUN PIPELINE
    # ======================================================

    pipeline = OpportunityPipeline()

    result = pipeline.run(

        company=company,

        sector=sector,

        cmp=cmp,

        signals=signals,

        causal_chain=None,

        catalyst_id="CAT-001",

        catalyst_title=(
            "Industrial Capex Acceleration"
        ),

        catalyst_trigger=(
            "Industrial investment cycle accelerates."
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

            "Order growth",

            "Industry capex",

            "Margin trend",
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
            "Synthetic end-to-end Opportunity "
            "integration test."
        ),

        economic_impact=(
            "Higher industrial demand."
        ),

        earnings_impact=(
            "Potential earnings acceleration."
        ),

        valuation_impact=(
            "Potential intrinsic-value realization."
        ),
    )

    # ======================================================
    # STAGE VALIDATION
    # ======================================================

    assert result.catalyst is not None

    print(
        "Catalyst               : PASS"
    )

    assert result.expectation_gap is not None

    print(
        "Expectation Gap        : PASS"
    )

    assert result.mispricing is not None

    print(
        "Mispricing             : PASS"
    )

    assert result.asymmetry is not None

    print(
        "Asymmetry              : PASS"
    )

    assert result.evidence is not None

    print(
        "Evidence               : PASS"
    )

    assert result.synthesis is not None

    print(
        "Synthesis              : PASS"
    )

    # ======================================================
    # EVIDENCE HAND-OFF
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
        "Evidence → Synthesis   : PASS"
    )

    # ======================================================
    # SCORE VALIDATION
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
        "Score / Confidence     : PASS"
    )

    # ======================================================
    # FINAL REPORT
    # ======================================================

    print()

    print("-" * 60)

    print(
        f"Catalyst Score         : "
        f"{result.catalyst.catalyst_score:.2f}"
    )

    print(
        f"Expectation Gap        : "
        f"{result.expectation_gap.gap_score:.2f}"
    )

    print(
        f"Mispricing Score       : "
        f"{result.mispricing.mispricing_score:.2f}"
    )

    print(
        f"Asymmetry Score        : "
        f"{result.asymmetry.asymmetry_score:.2f}"
    )

    print(
        f"Evidence Score         : "
        f"{result.evidence.evidence_score:.2f}"
    )

    print(
        f"Evidence Confidence    : "
        f"{result.evidence.confidence:.2f}"
    )

    print(
        f"Evidence Sufficient    : "
        f"{result.evidence.sufficiently_supported}"
    )

    print(
        f"Opportunity Score      : "
        f"{result.synthesis.opportunity_score:.2f}"
    )

    print(
        f"Opportunity Confidence : "
        f"{result.synthesis.confidence:.2f}"
    )

    print(
        f"Decision               : "
        f"{result.synthesis.decision.value}"
    )

    print("-" * 60)

    print()

    print(
        "EIOS OPPORTUNITY PIPELINE : PASS"
    )


if __name__ == "__main__":
    main()