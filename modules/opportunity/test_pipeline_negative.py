"""
EIOS
Everest Investment Operating System

Opportunity Pipeline
Negative-Path Integration Tests

Purpose
-------
Verify that the Opportunity Pipeline behaves conservatively
when evidence, valuation, asymmetry or catalyst quality
deteriorates.

These tests are deliberately designed around failure modes,
not ideal cases.
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
# COMMON FIXTURES
# ==========================================================


def make_signal(
    direction=SignalDirection.POSITIVE,
) -> Signal:

    return Signal(
        signal_id="NEG-TEST-001",
        title="Industrial Capex Signal",
        description="Synthetic negative-path test signal.",
        domain=SignalDomain.MACRO,
        signal_type=SignalType.ACCELERATION,
        direction=direction,
        stage=SignalStage.VALIDATED,
        horizon=TimeHorizon.MEDIUM_TERM,
        source="Synthetic test",
        source_type="Primary",
        sectors=["Industrial"],
        companies=["TEST COMPANY"],
        themes=["Industrial Capex"],
        economic_mechanism=(
            "Industrial investment affects demand."
        ),
        supply_demand_impact=(
            "Demand impact is under test."
        ),
        earnings_impact=(
            "Potential earnings impact."
        ),
    )


def make_scenarios(
    permanent_loss=False,
):

    return [
        AsymmetryScenario(
            name="Bull",
            probability=35.0,
            return_percent=100.0,
            time_months=24,
            permanent_loss=permanent_loss,
        ),
        AsymmetryScenario(
            name="Base",
            probability=50.0,
            return_percent=35.0,
            time_months=30,
            permanent_loss=False,
        ),
        AsymmetryScenario(
            name="Bear",
            probability=15.0,
            return_percent=-20.0,
            time_months=24,
            permanent_loss=False,
        ),
    ]


def make_evidence():

    return [
        EvidenceItem(
            evidence_id="NEG-E001",
            statement=(
                "Primary evidence supports the opportunity."
            ),
            source="Primary disclosure",
            category="Company",
            direction="Supporting",
            strength=90.0,
            confidence=90.0,
            independent_confirmation=2,
            is_primary_source=True,
            is_time_sensitive=True,
        ),
        EvidenceItem(
            evidence_id="NEG-E002",
            statement=(
                "Independent evidence confirms the trend."
            ),
            source="Industry evidence",
            category="Industry",
            direction="Supporting",
            strength=85.0,
            confidence=85.0,
            independent_confirmation=2,
            is_primary_source=True,
            is_time_sensitive=True,
        ),
        EvidenceItem(
            evidence_id="NEG-E003",
            statement=(
                "Peer evidence confirms the development."
            ),
            source="Peer disclosure",
            category="Competitive",
            direction="Supporting",
            strength=85.0,
            confidence=85.0,
            independent_confirmation=2,
            is_primary_source=True,
            is_time_sensitive=True,
        ),
    ]


def make_kill_switch():

    return [
        KillSwitch(
            name="Thesis Failure",
            condition=(
                "Core operating assumption fails."
            ),
            severity="High",
            measurable=True,
            threshold="Material deterioration",
            monitoring_frequency="Quarterly",
            rationale="Invalidates the thesis.",
            triggered=False,
        )
    ]


# ==========================================================
# PIPELINE RUNNER
# ==========================================================


def run_pipeline(
    *,
    evidence,
    scenarios,
    valuation,
    signal_direction=SignalDirection.POSITIVE,
    kill_switches=None,
):

    pipeline = OpportunityPipeline()

    return pipeline.run(
        company="TEST COMPANY",
        sector="Industrial",
        cmp=3500.0,
        signals=[
            make_signal(signal_direction)
        ],
        causal_chain=None,
        catalyst_id="NEG-CAT-001",
        catalyst_title="Industrial Capex",
        catalyst_trigger="Synthetic test catalyst.",
        market_expectation=45.0,
        eios_expectation=80.0,
        market_earnings_expectation=40.0,
        eios_earnings_expectation=75.0,
        valuation=valuation,
        asymmetry_scenarios=scenarios,
        supporting_evidence=evidence,
        contradictory_evidence=[],
        assumptions=[
            "Synthetic test assumption."
        ],
        kill_switches=(
            kill_switches
            if kill_switches is not None
            else make_kill_switch()
        ),
        monitoring_signals=[
            "Order growth",
            "Capex",
        ],
        invalidation_conditions=[
            "Core thesis deteriorates."
        ],
        affected_sectors=["Industrial"],
        affected_companies=["TEST COMPANY"],
    )


# ==========================================================
# TEST 1
# STRONG OPPORTUNITY + STRONG EVIDENCE
# ==========================================================


def test_strong_case():

    result = run_pipeline(
        evidence=make_evidence(),
        scenarios=make_scenarios(),
        valuation=TestValuation(),
    )

    assert result.synthesis is not None

    assert result.evidence is not None

    assert result.evidence.sufficiently_supported

    print(
        "Case 1 — Strong Opportunity : PASS"
    )


# ==========================================================
# TEST 2
# STRONG OPPORTUNITY + NO EVIDENCE
# ==========================================================


def test_no_evidence():

    result = run_pipeline(
        evidence=[],
        scenarios=make_scenarios(),
        valuation=TestValuation(),
    )

    assert result.synthesis is not None

    assert not result.synthesis.evidence_sufficient

    print(
        "Case 2 — No Evidence Gate    : PASS"
    )


# ==========================================================
# TEST 3
# NO KILL SWITCH
# ==========================================================


def test_no_kill_switch():

    result = run_pipeline(
        evidence=make_evidence(),
        scenarios=make_scenarios(),
        valuation=TestValuation(),
        kill_switches=[],
    )

    assert result.synthesis is not None

    assert (
        not result.synthesis.kill_switches
    )

    print(
        "Case 3 — No Kill Switch      : PASS"
    )


# ==========================================================
# TEST 4
# HIGH PERMANENT LOSS
# ==========================================================


def test_permanent_loss():

    scenarios = [
        AsymmetryScenario(
            name="Bull",
            probability=20.0,
            return_percent=100.0,
            time_months=24,
            permanent_loss=False,
        ),
        AsymmetryScenario(
            name="Base",
            probability=20.0,
            return_percent=20.0,
            time_months=30,
            permanent_loss=False,
        ),
        AsymmetryScenario(
            name="Permanent Loss",
            probability=60.0,
            return_percent=-100.0,
            time_months=24,
            permanent_loss=True,
        ),
    ]

    result = run_pipeline(
        evidence=make_evidence(),
        scenarios=scenarios,
        valuation=TestValuation(),
    )

    assert result.synthesis is not None

    assert (
        result.asymmetry.permanent_loss_probability
        >= 50.0
    )

    assert (
        result.synthesis.decision.value
        == "Reject"
    )

    print(
        "Case 4 — Permanent Loss      : PASS"
    )


# ==========================================================
# TEST 5
# WEAK VALUATION SUPPORT
# ==========================================================


def test_weak_valuation():

    weak_valuation = TestValuation(
        intrinsic_value=3500.0,
        fair_value=3500.0,
        confidence=50.0,
    )

    result = run_pipeline(
        evidence=make_evidence(),
        scenarios=make_scenarios(),
        valuation=weak_valuation,
    )

    assert result.synthesis is not None

    assert result.mispricing is not None

    assert (
        result.mispricing.potential_mispricing
        is False
    )

    print(
        "Case 5 — Weak Valuation       : PASS"
    )


# ==========================================================
# MAIN
# ==========================================================


def main():

    print()
    print("=" * 60)
    print(
        "EIOS OPPORTUNITY PIPELINE"
    )
    print(
        "NEGATIVE-PATH TEST"
    )
    print("=" * 60)

    test_strong_case()

    test_no_evidence()

    test_no_kill_switch()

    test_permanent_loss()

    test_weak_valuation()

    print()
    print("-" * 60)
    print(
        "EIOS OPPORTUNITY PIPELINE "
        "NEGATIVE-PATH TEST : PASS"
    )
    print("-" * 60)


if __name__ == "__main__":
    main()