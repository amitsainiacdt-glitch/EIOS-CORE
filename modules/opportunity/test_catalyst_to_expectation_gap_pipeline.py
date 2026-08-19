"""
EIOS
Everest Investment Operating System

Full Catalyst → Expectation Gap Pipeline Test
==============================================

Purpose
-------
Verifies the controlled integration between the existing
Catalyst Engine and the existing Expectation Gap Engine.

Architecture

Signal
    ↓
CatalystEngine
    ↓
Catalyst
    ↓
ExpectationGapEngine
    ↓
ExpectationGap
    ↓
Potential Mispricing Analysis

Design Principles
-----------------
- Uses the canonical Signal model.
- Uses the existing CatalystEngine.
- Uses the existing ExpectationGapEngine.
- Does not create a second Catalyst engine.
- Does not create a second Expectation Gap engine.
- Does not perform valuation.
- Does not perform portfolio allocation.
- Does not make investment decisions.
- Preserves Catalyst identity.
- Preserves Catalyst evidence.
- Preserves assumptions.
- Preserves invalidation conditions.
- Preserves the analytical boundary.
"""


from modules.opportunity.catalyst_engine import (
    CatalystEngine,
)

from modules.opportunity.expectation_gap_engine import (
    ExpectationGapEngine,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
)


def main() -> None:

    print("=" * 60)
    print(
        "EIOS CATALYST → EXPECTATION GAP PIPELINE TEST"
    )
    print("=" * 60)

    # ======================================================
    # TEST 1 — SIGNAL CREATION
    # ======================================================

    signal = Signal(
        signal_id="PIPE-GAP-001",

        title="Industrial Capex Acceleration",

        description=(
            "Industrial investment is accelerating."
        ),

        domain=SignalDomain.SECTOR,

        signal_type=SignalType.ACCELERATION,

        direction=SignalDirection.POSITIVE,

        magnitude=85.0,

        probability=85.0,

        relevance=90.0,

        persistence=85.0,

        confidence=85.0,

        market_recognition=25.0,

        source="Industry Data",

        supporting_sources=[
            "Industry Data",
            "Company Disclosures",
        ],

        evidence=[
            "Order inflows accelerating.",
            "Capacity expansion increasing.",
        ],

        sectors=[
            "Capital Goods",
        ],

        companies=[
            "The Anup Engineering Limited",
        ],

        independent_confirmation=2,
    )

    assert signal.signal_id == (
        "PIPE-GAP-001"
    )

    print(
        "Test 1 — Signal Creation             : PASS"
    )

    # ======================================================
    # TEST 2 — CATALYST ENGINE
    # ======================================================

    catalyst_engine = CatalystEngine()

    catalyst = catalyst_engine.analyze(
        catalyst_id="PIPE-CAT-001",

        title="Capital Goods Cycle Acceleration",

        trigger="Industrial capex acceleration",

        signals=[
            signal,
        ],

        description=(
            "Industrial investment is creating "
            "stronger demand for capital goods."
        ),

        economic_impact=(
            "Higher equipment demand and utilization."
        ),

        earnings_impact=(
            "Potential revenue and margin acceleration."
        ),

        affected_sectors=[
            "Capital Goods",
        ],

        affected_companies=[
            "The Anup Engineering Limited",
        ],

        assumptions=[
            "Industrial capex remains elevated.",
        ],

        invalidation_conditions=[
            "Industrial orders materially weaken.",
        ],
    )

    assert catalyst is not None

    print(
        "Test 2 — Catalyst Creation           : PASS"
    )

    # ======================================================
    # TEST 3 — CATALYST IDENTITY
    # ======================================================

    assert catalyst.catalyst_id == (
        "PIPE-CAT-001"
    )

    print(
        "Test 3 — Catalyst Identity            : PASS"
    )

    # ======================================================
    # TEST 4 — CATALYST QUALITY
    # ======================================================

    assert catalyst.catalyst_score >= 0.0
    assert catalyst.confidence >= 0.0
    assert catalyst.confidence <= 100.0

    print(
        "Test 4 — Catalyst Quality             : PASS"
    )

    # ======================================================
    # TEST 5 — CATALYST → EXPECTATION GAP
    # ======================================================

    gap_engine = ExpectationGapEngine()

    gap = gap_engine.analyze(
        gap_id="PIPE-GAP-001",

        company=(
            "The Anup Engineering Limited"
        ),

        sector="Capital Goods",

        catalyst=catalyst,

        market_expectation=45.0,

        eios_expectation=80.0,

        market_earnings_expectation=40.0,

        eios_earnings_expectation=75.0,

        assumptions=[
            "Order growth persists.",
            "Capacity additions translate into revenue.",
        ],

        invalidation_conditions=[
            "Order inflows reverse.",
            "Industrial capex cycle weakens.",
        ],
    )

    assert gap is not None

    print(
        "Test 5 — Catalyst → Expectation Gap  : PASS"
    )

    # ======================================================
    # TEST 6 — CATALYST PRESERVATION
    # ======================================================

    assert gap.catalyst is catalyst

    assert gap.catalyst.catalyst_id == (
        "PIPE-CAT-001"
    )

    print(
        "Test 6 — Catalyst Preservation        : PASS"
    )

    # ======================================================
    # TEST 7 — EXPECTATION DIFFERENCE
    # ======================================================

    assert (
        gap.market_expectation
        == 45.0
    )

    assert (
        gap.eios_expectation
        == 80.0
    )

    assert (
        gap.expectation_difference
        == 35.0
    )

    print(
        "Test 7 — Expectation Difference       : PASS"
    )

    # ======================================================
    # TEST 8 — EARNINGS GAP
    # ======================================================

    assert (
        gap.market_earnings_expectation
        == 40.0
    )

    assert (
        gap.eios_earnings_expectation
        == 75.0
    )

    assert (
        gap.earnings_gap
        == 35.0
    )

    print(
        "Test 8 — Earnings Gap                 : PASS"
    )

    # ======================================================
    # TEST 9 — POSITIVE GAP
    # ======================================================

    assert gap.positive_gap

    assert not gap.negative_gap

    print(
        "Test 9 — Positive Expectation Gap     : PASS"
    )

    # ======================================================
    # TEST 10 — MARKET RECOGNITION
    # ======================================================

    assert (
        gap.market_recognition
        == catalyst.market_recognition
    )

    print(
        "Test 10 — Market Recognition           : PASS"
    )

    # ======================================================
    # TEST 11 — UNRECOGNIZED POTENTIAL
    # ======================================================

    assert (
        gap.unrecognized_potential
        == 100.0
        - gap.market_recognition
    )

    assert (
        gap.unrecognized_potential
        == 100.0
        - catalyst.market_recognition
    )

    print(
        "Test 11 — Unrecognized Potential       : PASS"
    )

    # ======================================================
    # TEST 12 — GAP SCORE
    # ======================================================

    assert gap.gap_score >= 0.0
    assert gap.gap_score <= 100.0

    print(
        "Test 12 — Expectation Gap Score        : PASS"
    )

    # ======================================================
    # TEST 13 — GAP CONFIDENCE
    # ======================================================

    assert gap.confidence >= 0.0
    assert gap.confidence <= 100.0

    print(
        "Test 13 — Expectation Gap Confidence   : PASS"
    )

    # ======================================================
    # TEST 14 — ASSUMPTIONS
    # ======================================================

    assert len(
        gap.assumptions
    ) == 2

    assert (
        "Order growth persists."
        in gap.assumptions
    )

    assert (
        "Capacity additions translate into revenue."
        in gap.assumptions
    )

    print(
        "Test 14 — Assumption Preservation      : PASS"
    )

    # ======================================================
    # TEST 15 — INVALIDATION CONDITIONS
    # ======================================================

    assert len(
        gap.invalidation_conditions
    ) == 2

    assert (
        "Order inflows reverse."
        in gap.invalidation_conditions
    )

    assert (
        "Industrial capex cycle weakens."
        in gap.invalidation_conditions
    )

    print(
        "Test 15 — Invalidation Preservation   : PASS"
    )

    # ======================================================
    # TEST 16 — CATALYST SIGNAL PRESERVATION
    # ======================================================

    assert (
        catalyst.signals[0].signal_id
        == "PIPE-GAP-001"
    )

    assert (
        catalyst.signals[0].magnitude
        == 85.0
    )

    assert (
        catalyst.signals[0].market_recognition
        == 25.0
    )

    print(
        "Test 16 — Signal Provenance            : PASS"
    )

    # ======================================================
    # TEST 17 — SIGNAL IMMUTABILITY
    # ======================================================

    assert (
        signal.signal_id
        == "PIPE-GAP-001"
    )

    assert (
        signal.magnitude
        == 85.0
    )

    assert (
        signal.probability
        == 85.0
    )

    assert (
        signal.market_recognition
        == 25.0
    )

    print(
        "Test 17 — Signal Immutability          : PASS"
    )

    # ======================================================
    # TEST 18 — CATALYST IMMUTABILITY
    # ======================================================

    assert (
        catalyst.catalyst_id
        == "PIPE-CAT-001"
    )

    assert (
        catalyst.catalyst_score
        >= 0.0
    )

    assert (
        catalyst.confidence
        >= 0.0
    )

    print(
        "Test 18 — Catalyst Preservation        : PASS"
    )

    # ======================================================
    # TEST 19 — EVIDENCE PRESERVATION
    # ======================================================

    assert gap.evidence

    print(
        "Test 19 — Evidence Preservation        : PASS"
    )

    # ======================================================
    # TEST 20 — ANALYTICAL BOUNDARY
    # ======================================================

    forbidden_methods = [
        "calculate_valuation",
        "calculate_intrinsic_value",
        "calculate_opportunity_score",
        "rank_opportunity",
        "allocate_portfolio",
        "execute_trade",
    ]

    for method in forbidden_methods:

        assert not hasattr(
            gap_engine,
            method,
        )

    print(
        "Test 20 — Analytical Boundary          : PASS"
    )

    # ======================================================
    # OUTPUT
    # ======================================================

    print()
    print(
        f"Market Expectation : "
        f"{gap.market_expectation:.2f}"
    )

    print(
        f"EIOS Expectation   : "
        f"{gap.eios_expectation:.2f}"
    )

    print(
        f"Expectation Gap    : "
        f"{gap.expectation_difference:.2f}"
    )

    print(
        f"Market Earnings    : "
        f"{gap.market_earnings_expectation:.2f}"
    )

    print(
        f"EIOS Earnings      : "
        f"{gap.eios_earnings_expectation:.2f}"
    )

    print(
        f"Earnings Gap       : "
        f"{gap.earnings_gap:.2f}"
    )

    print(
        f"Market Recognition : "
        f"{gap.market_recognition:.2f}"
    )

    print(
        f"Unrecognized       : "
        f"{gap.unrecognized_potential:.2f}"
    )

    print(
        f"Gap Score          : "
        f"{gap.gap_score:.2f}"
    )

    print(
        f"Confidence         : "
        f"{gap.confidence:.2f}"
    )

    print(
        f"Positive Gap       : "
        f"{gap.positive_gap}"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print("=" * 60)
    print(
        "EIOS CATALYST → EXPECTATION GAP PIPELINE "
        ": ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()