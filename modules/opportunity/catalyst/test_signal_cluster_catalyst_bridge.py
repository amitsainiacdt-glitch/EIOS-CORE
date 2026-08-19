"""
EIOS
Everest Investment Operating System

Signal Cluster → Catalyst Bridge Test
=====================================

Purpose
-------
Verifies that an aggregated SignalCluster can be passed
through the SignalClusterCatalystBridge into the existing
Catalyst classification boundary.

Design principles
-----------------
- Uses the canonical Signal model.
- Uses the canonical SignalAggregationEngine.
- Uses the existing CatalystClassifier.
- Does not modify Signals.
- Does not perform valuation.
- Does not perform opportunity scoring.
- Does not create investment decisions.
- Preserves the analytical boundary.
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

from modules.opportunity.catalyst.signal_cluster_catalyst_bridge import (
    SignalClusterCatalystBridge,
)


# ==========================================================
# SIGNAL FACTORY
# ==========================================================


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


# ==========================================================
# MAIN TEST
# ==========================================================


def main() -> None:

    print("=" * 60)

    print(
        "EIOS SIGNAL CLUSTER → CATALYST BRIDGE TEST"
    )

    print("=" * 60)

    # ======================================================
    # TEST 1 — BRIDGE CREATION
    # ======================================================

    bridge = SignalClusterCatalystBridge()

    assert bridge is not None

    print(
        "Test 1 — Bridge Creation              : PASS"
    )

    # ======================================================
    # TEST 2 — CREATE INDEPENDENT SIGNALS
    # ======================================================

    signal_1 = make_signal(
        signal_id="BRIDGE-001",

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
        signal_id="BRIDGE-002",

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
        signal_id="BRIDGE-003",

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
        "Test 2 — Signals Created              : PASS"
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
        cluster_id="BRIDGE-THEME-001",
    )

    assert cluster is not None

    assert cluster.signal_count == 3

    print(
        "Test 3 — Signal Cluster Created       : PASS"
    )

    # ======================================================
    # TEST 4 — CLUSTER QUALITY
    # ======================================================

    assert cluster.cluster_score >= 60.0

    assert cluster.confidence >= 60.0

    assert cluster.emerging

    print(
        "Test 4 — Cluster Quality              : PASS"
    )

    # ======================================================
    # TEST 5 — BRIDGE EXECUTION
    # ======================================================

    result = bridge.classify(
        cluster=cluster,
    )

    assert result is not None

    print(
        "Test 5 — Cluster → Catalyst           : PASS"
    )

    # ======================================================
    # TEST 6 — CLASSIFICATION
    # ======================================================

    assert result.is_classified

    assert result.primary is not None

    print(
        "Test 6 — Catalyst Classification      : PASS"
    )

    # ======================================================
    # TEST 7 — PRIMARY CATALYST
    # ======================================================

    print(
        f"Primary Catalyst : "
        f"{result.primary.family.value}"
    )

    assert result.primary.family is not None

    print(
        "Test 7 — Primary Catalyst             : PASS"
    )

    # ======================================================
    # TEST 8 — CONFIDENCE
    # ======================================================

    print(
        f"Catalyst Confidence : "
        f"{result.confidence:.2f}"
    )

    assert (
        0.0
        <= result.confidence
        <= 100.0
    )

    print(
        "Test 8 — Catalyst Confidence          : PASS"
    )

    # ======================================================
    # TEST 9 — SIGNAL IMMUTABILITY
    # ======================================================

    assert (
        signal_1.signal_id
        == "BRIDGE-001"
    )

    assert (
        signal_2.signal_id
        == "BRIDGE-002"
    )

    assert (
        signal_3.signal_id
        == "BRIDGE-003"
    )

    assert (
        signal_1.magnitude
        == 85.0
    )

    assert (
        signal_2.magnitude
        == 80.0
    )

    assert (
        signal_3.magnitude
        == 75.0
    )

    print(
        "Test 9 — Signal Immutability          : PASS"
    )

    # ======================================================
    # TEST 10 — CLUSTER PRESERVATION
    # ======================================================

    assert (
        cluster.theme
        == "Indian Capital Goods Cycle"
    )

    assert (
        cluster.signal_count
        == 3
    )

    print(
        "Test 10 — Cluster Preservation         : PASS"
    )

    # ======================================================
    # TEST 11 — ANALYTICAL BOUNDARY
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
            bridge,
            method,
        )

    print(
        "Test 11 — Analytical Boundary         : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print("=" * 60)

    print(
        "EIOS SIGNAL CLUSTER → CATALYST BRIDGE : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()