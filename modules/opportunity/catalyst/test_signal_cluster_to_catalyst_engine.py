"""
EIOS
Everest Investment Operating System

Signal Cluster → Catalyst Engine Integration Test
==================================================

Purpose
-------
Verifies the complete integration:

Signal
    ↓
Signal Aggregation
    ↓
SignalCluster
    ↓
CatalystEngine
    ↓
Catalyst Assessment

This test confirms that the new Signal Intelligence /
Aggregation architecture integrates with the existing
canonical CatalystEngine.

Design Principles
-----------------
- Uses canonical Signal model.
- Uses canonical SignalAggregationEngine.
- Uses canonical CatalystEngine.
- Does not create a second Catalyst engine.
- Does not mutate Signals.
- Does not mutate SignalCluster.
- Does not perform valuation.
- Does not perform opportunity scoring.
- Does not make investment decisions.
"""


from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
)

from modules.opportunity.signals.signal_aggregation import (
    SignalAggregationEngine,
)

from modules.opportunity.catalyst_engine import (
    CatalystEngine,
    Catalyst,
)


def make_signal(
    *,
    signal_id: str,
    title: str,
    description: str,
    domain: SignalDomain,
    signal_type: SignalType,
    direction: SignalDirection,
    magnitude: float,
    probability: float,
    relevance: float,
    persistence: float,
    confidence: float,
    source: str,
    sectors: list[str],
    themes: list[str] | None = None,
) -> Signal:

    return Signal(
        signal_id=signal_id,
        title=title,
        description=description,
        domain=domain,
        signal_type=signal_type,
        direction=direction,
        magnitude=magnitude,
        probability=probability,
        relevance=relevance,
        persistence=persistence,
        confidence=confidence,
        source=source,
        supporting_sources=[
            source,
        ],
        sectors=sectors,
        themes=themes or [],
    )


def main() -> None:

    print("=" * 60)
    print(
        "EIOS SIGNAL CLUSTER → CATALYST ENGINE TEST"
    )
    print("=" * 60)

    # ======================================================
    # TEST 1 — ENGINE CREATION
    # ======================================================

    engine = CatalystEngine()

    assert engine is not None

    print(
        "Test 1 — Catalyst Engine Creation       : PASS"
    )

    # ======================================================
    # TEST 2 — CREATE SIGNALS
    # ======================================================

    signal_1 = make_signal(
        signal_id="ENGINE-001",
        title="Government Capex Acceleration",
        description=(
            "Government infrastructure spending "
            "is accelerating."
        ),
        domain=SignalDomain.FISCAL,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        magnitude=85.0,
        probability=90.0,
        relevance=90.0,
        persistence=85.0,
        confidence=90.0,
        source="Government Budget",
        sectors=[
            "Capital Goods",
            "Infrastructure",
        ],
        themes=[
            "Government Capex",
            "Capital Cycle",
        ],
    )

    signal_2 = make_signal(
        signal_id="ENGINE-002",
        title="Industrial Order Inflow Acceleration",
        description=(
            "Industrial order inflows are increasing."
        ),
        domain=SignalDomain.SECTOR,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        magnitude=80.0,
        probability=85.0,
        relevance=90.0,
        persistence=80.0,
        confidence=85.0,
        source="Industry Data",
        sectors=[
            "Capital Goods",
        ],
        themes=[
            "Order Cycle",
            "Capital Cycle",
        ],
    )

    signal_3 = make_signal(
        signal_id="ENGINE-003",
        title="Capacity Expansion",
        description=(
            "Industrial companies are expanding "
            "production capacity."
        ),
        domain=SignalDomain.CAPITAL_CYCLE,
        signal_type=SignalType.TREND,
        direction=SignalDirection.POSITIVE,
        magnitude=75.0,
        probability=85.0,
        relevance=85.0,
        persistence=80.0,
        confidence=80.0,
        source="Company Filings",
        sectors=[
            "Capital Goods",
        ],
        themes=[
            "Capacity Expansion",
            "Capital Cycle",
        ],
    )

    signals = [
        signal_1,
        signal_2,
        signal_3,
    ]

    print(
        "Test 2 — Signals Created                 : PASS"
    )

    # ======================================================
    # TEST 3 — SIGNAL AGGREGATION
    # ======================================================

    aggregation_engine = (
        SignalAggregationEngine()
    )

    cluster = aggregation_engine.aggregate(
        signals,
        theme="Indian Capital Goods Cycle",
        cluster_id="ENGINE-THEME-001",
    )

    assert cluster is not None

    assert cluster.signal_count == 3

    print(
        "Test 3 — Signal Cluster Created          : PASS"
    )

    # ======================================================
    # TEST 4 — CLUSTER QUALITY
    # ======================================================

    assert cluster.cluster_score >= 60.0
    assert cluster.confidence >= 60.0
    assert cluster.emerging

    print(
        "Test 4 — Cluster Quality                 : PASS"
    )

    # ======================================================
    # TEST 5 — CLUSTER SIGNAL PRESERVATION
    # ======================================================

    cluster_signal_ids = {
        signal.signal_id
        for signal in cluster.signals
    }

    assert cluster_signal_ids == {
        "ENGINE-001",
        "ENGINE-002",
        "ENGINE-003",
    }

    print(
        "Test 5 — Cluster Signal Preservation     : PASS"
    )

    # ======================================================
    # TEST 6 — CATALYST ENGINE EXECUTION
    # ======================================================

    catalyst = engine.analyze(
        catalyst_id="CAT-ENGINE-001",

        title=(
            "Indian Capital Goods Cycle"
        ),

        trigger=(
            "Government capex, industrial orders "
            "and capacity expansion are accelerating."
        ),

        signals=list(
            cluster.signals
        ),

        causal_chain=None,

        description=(
            "Multiple independent signals indicate "
            "a strengthening Indian capital goods cycle."
        ),

        economic_impact=(
            "Higher industrial investment and "
            "capacity utilisation."
        ),

        earnings_impact=(
            "Higher orders and utilisation can "
            "support revenue and margin growth."
        ),

        valuation_impact=(
            "Improving earnings visibility may "
            "increase market recognition."
        ),

        affected_sectors=[
            "Capital Goods",
            "Infrastructure",
        ],

        affected_companies=[],

        assumptions=[
            "Government capital expenditure remains strong.",
            "Industrial order inflows remain healthy.",
        ],

        invalidation_conditions=[
            "Government capex materially declines.",
            "Industrial order inflows materially weaken.",
        ],
    )

    assert catalyst is not None

    assert isinstance(
        catalyst,
        Catalyst,
    )

    print(
        "Test 6 — Catalyst Engine Execution       : PASS"
    )

    # ======================================================
    # TEST 7 — CATALYST CLASSIFICATION
    # ======================================================

    assert catalyst.primary_catalyst_family

    print(
        "Primary Catalyst : "
        f"{catalyst.primary_catalyst_family}"
    )

    print(
        "Test 7 — Catalyst Classification         : PASS"
    )

    # ======================================================
    # TEST 8 — CATALYST SCORE
    # ======================================================

    print(
        "Catalyst Score : "
        f"{catalyst.catalyst_score:.2f}"
    )

    assert (
        catalyst.catalyst_score
        >= 0.0
    )

    assert (
        catalyst.catalyst_score
        <= 100.0
    )

    print(
        "Test 8 — Catalyst Score                  : PASS"
    )

    # ======================================================
    # TEST 9 — CATALYST CONFIDENCE
    # ======================================================

    print(
        "Catalyst Confidence : "
        f"{catalyst.confidence:.2f}"
    )

    assert (
        catalyst.confidence
        >= 0.0
    )

    assert (
        catalyst.confidence
        <= 100.0
    )

    print(
        "Test 9 — Catalyst Confidence             : PASS"
    )

    # ======================================================
    # TEST 10 — DIRECTION
    # ======================================================

    assert (
        catalyst.direction
        == SignalDirection.POSITIVE
    )

    print(
        "Test 10 — Catalyst Direction             : PASS"
    )

    # ======================================================
    # TEST 11 — SIGNAL PRESERVATION
    # ======================================================

    assert (
        catalyst.signals[0].signal_id
        == "ENGINE-001"
    )

    assert (
        catalyst.signals[1].signal_id
        == "ENGINE-002"
    )

    assert (
        catalyst.signals[2].signal_id
        == "ENGINE-003"
    )

    print(
        "Test 11 — Signal Preservation            : PASS"
    )

    # ======================================================
    # TEST 12 — ORIGINAL SIGNAL IMMUTABILITY
    # ======================================================

    assert signal_1.magnitude == 85.0
    assert signal_2.magnitude == 80.0
    assert signal_3.magnitude == 75.0

    assert signal_1.signal_id == "ENGINE-001"
    assert signal_2.signal_id == "ENGINE-002"
    assert signal_3.signal_id == "ENGINE-003"

    print(
        "Test 12 — Signal Immutability            : PASS"
    )

    # ======================================================
    # TEST 13 — CLUSTER PRESERVATION
    # ======================================================

    assert (
        cluster.theme
        == "Indian Capital Goods Cycle"
    )

    assert cluster.signal_count == 3

    print(
        "Test 13 — Cluster Preservation           : PASS"
    )

    # ======================================================
    # TEST 14 — ANALYTICAL BOUNDARY
    # ======================================================

    forbidden_methods = [
        "calculate_valuation",
        "calculate_opportunity_score",
        "rank_opportunity",
        "allocate_portfolio",
        "execute_trade",
    ]

    for method in forbidden_methods:

        assert not hasattr(
            engine,
            method,
        )

    print(
        "Test 14 — Analytical Boundary            : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print("=" * 60)
    print(
        "EIOS SIGNAL CLUSTER → CATALYST ENGINE : ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()