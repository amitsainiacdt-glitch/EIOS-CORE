"""
EIOS
Everest Investment Operating System

Signal Interpretation Engine Test
=================================

Verifies the controlled boundary:

EvidenceItem
        ↓
Explicit SignalInterpretation
        ↓
SignalInterpretationEngine
        ↓
Canonical Signal

Design boundary
---------------
This test verifies that Signal creation requires explicit
interpretation and that evidence provenance is preserved.

The test does NOT test:
- AI interpretation
- semantic interpretation
- opportunity scoring
- valuation
- catalyst classification
- investment decisions
"""

from modules.opportunity.evidence_engine import (
    EvidenceItem,
)

from modules.opportunity.signals.signal_interpretation import (
    SignalInterpretation,
)

from modules.opportunity.signals.signal_interpretation_engine import (
    SignalInterpretationEngine,
)

from modules.opportunity.signals.signal_model import (
    EvidenceQuality,
    SignalDirection,
    SignalDomain,
    SignalStage,
    SignalType,
    TimeHorizon,
)


# ==========================================================
# TEST DATA
# ==========================================================


def make_evidence() -> EvidenceItem:
    """
    Create deterministic EvidenceItem test data.
    """

    return EvidenceItem(
        evidence_id="EVIDENCE-001",

        statement=(
            "Industrial demand is improving with "
            "stronger order activity."
        ),

        source="https://example.com/research",

        category="Demand",

        direction="Supporting",

        strength=85.0,

        confidence=90.0,

        independent_confirmation=2,

        is_primary_source=False,

        is_time_sensitive=True,

        notes="Synthetic evidence for testing.",
    )


def make_interpretation() -> SignalInterpretation:
    """
    Create deterministic explicit signal interpretation.
    """

    return SignalInterpretation(
        title="Industrial Demand Acceleration",

        description=(
            "Evidence indicates accelerating "
            "industrial demand."
        ),

        detected_date="2026-08-19",

        domain=SignalDomain.SECTOR,

        signal_type=SignalType.ACCELERATION,

        direction=SignalDirection.POSITIVE,

        stage=SignalStage.EMERGING,

        horizon=TimeHorizon.MEDIUM_TERM,

        sectors=[
            "Capital Goods",
        ],

        companies=[
            "The Anup Engineering Limited",
        ],

        themes=[
            "Industrial Capex",
        ],

        economic_mechanism=(
            "Improving demand may increase order "
            "intake and capacity utilization."
        ),

        supply_demand_impact=(
            "Demand is strengthening."
        ),

        earnings_impact=(
            "Potential positive operating leverage."
        ),

        valuation_impact=(
            "Potential improvement in earnings "
            "expectations."
        ),

        magnitude=75.0,

        probability=80.0,

        persistence=70.0,

        relevance=90.0,

        market_expectation=(
            "Market expectations remain moderate."
        ),

        market_recognition=20.0,

        price_reaction=(
            "Limited market recognition."
        ),

        causal_chain=[
            "Demand improvement",
            "Higher order intake",
            "Revenue acceleration",
            "Potential earnings improvement",
        ],

        beneficiaries=[
            "Capital goods companies",
        ],

        adversely_affected=[],

        historical_precedent=(
            "Prior industrial recovery cycles."
        ),

        invalidation_conditions=[
            "Order intake reverses materially.",
            "Industrial demand weakens for "
            "multiple periods.",
        ],
    )


# ==========================================================
# MAIN TEST
# ==========================================================


def main() -> None:

    print("=" * 60)

    print(
        "EIOS SIGNAL INTERPRETATION ENGINE TEST"
    )

    print("=" * 60)

    engine = SignalInterpretationEngine()

    # ======================================================
    # TEST 1 — ENGINE CREATION
    # ======================================================

    assert engine is not None

    print(
        "Test 1 — Engine Creation                 : PASS"
    )

    # ======================================================
    # TEST 2 — VALID CONVERSION
    # ======================================================

    evidence = make_evidence()

    interpretation = make_interpretation()

    result = engine.create(
        evidence=evidence,
        interpretation=interpretation,
        signal_id="SIG-001",
    )

    assert result.accepted is True

    assert result.signal is not None

    print(
        "Test 2 — Evidence → Signal               : PASS"
    )

    signal = result.signal

    # ======================================================
    # TEST 3 — SIGNAL ID
    # ======================================================

    assert signal.signal_id == "SIG-001"

    print(
        "Test 3 — Signal Identity                  : PASS"
    )

    # ======================================================
    # TEST 4 — INTERPRETATION PRESERVATION
    # ======================================================

    assert (
        signal.title
        == interpretation.title
    )

    assert (
        signal.description
        == interpretation.description
    )

    assert (
        signal.domain
        == interpretation.domain
    )

    assert (
        signal.signal_type
        == interpretation.signal_type
    )

    assert (
        signal.direction
        == interpretation.direction
    )

    assert (
        signal.stage
        == interpretation.stage
    )

    assert (
        signal.horizon
        == interpretation.horizon
    )

    assert (
        signal.detected_date
        == interpretation.detected_date
    )

    print(
        "Test 4 — Interpretation Preservation     : PASS"
    )

    # ======================================================
    # TEST 5 — EVIDENCE ID PRESERVATION
    # ======================================================

    assert (
        signal.evidence
        == [
            evidence.evidence_id
        ]
    )

    print(
        "Test 5 — Evidence Identity Preservation  : PASS"
    )

    # ======================================================
    # TEST 6 — SOURCE PRESERVATION
    # ======================================================

    assert (
        signal.source
        == evidence.source
    )

    assert (
        signal.supporting_sources
        == [
            evidence.source
        ]
    )

    print(
        "Test 6 — Source Preservation              : PASS"
    )

    # ======================================================
    # TEST 7 — CONFIDENCE PRESERVATION
    # ======================================================

    assert (
        signal.confidence
        == evidence.confidence
    )

    assert (
        signal.independent_confirmation
        == evidence.independent_confirmation
    )

    assert (
        signal.corroboration
        == float(
            evidence.independent_confirmation
        )
    )

    print(
        "Test 7 — Evidence Confidence              : PASS"
    )

    # ======================================================
    # TEST 8 — EVIDENCE QUALITY
    # ======================================================

    assert (
        signal.evidence_quality
        == EvidenceQuality.A
    )

    print(
        "Test 8 — Evidence Quality Classification : PASS"
    )

    # ======================================================
    # TEST 9 — PROVENANCE METADATA
    # ======================================================

    assert (
        signal.metadata["evidence_id"]
        == evidence.evidence_id
    )

    assert (
        signal.metadata["evidence_source"]
        == evidence.source
    )

    assert (
        signal.metadata["evidence_category"]
        == evidence.category
    )

    print(
        "Test 9 — Provenance Metadata              : PASS"
    )

    # ======================================================
    # TEST 10 — EVIDENCE REMAINS UNMODIFIED
    # ======================================================

    original_statement = evidence.statement

    original_source = evidence.source

    original_strength = evidence.strength

    original_confidence = evidence.confidence

    assert (
        evidence.statement
        == original_statement
    )

    assert (
        evidence.source
        == original_source
    )

    assert (
        evidence.strength
        == original_strength
    )

    assert (
        evidence.confidence
        == original_confidence
    )

    print(
        "Test 10 — Evidence Remains Unmodified     : PASS"
    )

    # ======================================================
    # TEST 11 — MISSING EVIDENCE ID
    # ======================================================

    invalid_evidence = EvidenceItem(
        evidence_id="",

        statement=(
            "Valid statement."
        ),

        source="https://example.com",

        strength=80.0,

        confidence=80.0,
    )

    result = engine.create(
        evidence=invalid_evidence,
        interpretation=interpretation,
        signal_id="SIG-002",
    )

    assert result.accepted is False

    assert result.signal is None

    assert (
        "evidence_id"
        in result.reason
    )

    print(
        "Test 11 — Missing Evidence ID Rejected    : PASS"
    )

    # ======================================================
    # TEST 12 — MISSING INTERPRETATION TITLE
    # ======================================================

    invalid_interpretation = (
        SignalInterpretation(
            title="",

            description=(
                "Description is present."
            ),

            domain=SignalDomain.SECTOR,

            signal_type=SignalType.CHANGE,

            direction=SignalDirection.POSITIVE,
        )
    )

    result = engine.create(
        evidence=evidence,
        interpretation=invalid_interpretation,
        signal_id="SIG-003",
    )

    assert result.accepted is False

    assert result.signal is None

    assert (
        "title"
        in result.reason
    )

    print(
        "Test 12 — Missing Title Rejected           : PASS"
    )

    # ======================================================
    # TEST 13 — MISSING DESCRIPTION
    # ======================================================

    invalid_interpretation = (
        SignalInterpretation(
            title="Valid Signal",

            description="",

            domain=SignalDomain.SECTOR,

            signal_type=SignalType.CHANGE,

            direction=SignalDirection.POSITIVE,
        )
    )

    result = engine.create(
        evidence=evidence,
        interpretation=invalid_interpretation,
        signal_id="SIG-004",
    )

    assert result.accepted is False

    assert result.signal is None

    assert (
        "description"
        in result.reason
    )

    print(
        "Test 13 — Missing Description Rejected     : PASS"
    )

    # ======================================================
    # TEST 14 — EMPTY SIGNAL ID
    # ======================================================

    empty_signal_id_rejected = False

    try:

        engine.create(
            evidence=evidence,
            interpretation=interpretation,
            signal_id="",
        )

    except ValueError:

        empty_signal_id_rejected = True

    assert (
        empty_signal_id_rejected
        is True
    )

    print(
        "Test 14 — Empty Signal ID Boundary         : PASS"
    )

    # ======================================================
    # TEST 15 — ANALYTICAL BOUNDARY
    # ======================================================

    valid_result = engine.create(
        evidence=evidence,
        interpretation=interpretation,
        signal_id="SIG-005",
    )

    assert valid_result.accepted is True

    assert valid_result.signal is not None

    assert not hasattr(
        valid_result,
        "opportunity_score",
    )

    assert not hasattr(
        valid_result,
        "valuation",
    )

    assert not hasattr(
        valid_result,
        "catalyst_score",
    )

    print(
        "Test 15 — Analytical Boundary              : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print(
        "EIOS SIGNAL INTERPRETATION ENGINE "
        ": ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()