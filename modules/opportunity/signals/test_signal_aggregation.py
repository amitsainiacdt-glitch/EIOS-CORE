"""
EIOS
Everest Investment Operating System

Signal Aggregation Test

Purpose:
Verifies that multiple independent signals can be
combined into a higher-order emerging intelligence theme.
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


def main():

    engine = SignalAggregationEngine()

    print("=" * 60)
    print("EIOS SIGNAL AGGREGATION TEST")
    print("=" * 60)

    # ==========================================================
    # SIGNAL 1 — GOVERNMENT CAPEX
    # ==========================================================

    government_capex = Signal(
        signal_id="AGG-001",
        title="Government Capital Expenditure Increase",
        description="Public infrastructure spending is accelerating.",
        domain=SignalDomain.FISCAL,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        magnitude=85.0,
        probability=90.0,
        relevance=90.0,
        persistence=85.0,
        confidence=90.0,
        source="Government Budget",
        supporting_sources=[
            "Government Budget",
            "Official Ministry Release",
        ],
        sectors=[
            "Capital Goods",
            "Infrastructure",
        ],
    )

    # ==========================================================
    # SIGNAL 2 — ORDER INFLOW
    # ==========================================================

    order_inflow = Signal(
        signal_id="AGG-002",
        title="Industrial Order Inflow Acceleration",
        description="New industrial orders are increasing.",
        domain=SignalDomain.SECTOR,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        magnitude=80.0,
        probability=85.0,
        relevance=90.0,
        persistence=80.0,
        confidence=85.0,
        source="Industry Data",
        supporting_sources=[
            "Industry Data",
            "Company Disclosures",
        ],
        sectors=[
            "Capital Goods",
        ],
    )

    # ==========================================================
    # SIGNAL 3 — CAPACITY EXPANSION
    # ==========================================================

    capacity_expansion = Signal(
        signal_id="AGG-003",
        title="Industry Capacity Expansion",
        description="Companies are increasing production capacity.",
        domain=SignalDomain.CAPITAL_CYCLE,
        signal_type=SignalType.TREND,
        direction=SignalDirection.POSITIVE,
        magnitude=75.0,
        probability=85.0,
        relevance=85.0,
        persistence=80.0,
        confidence=80.0,
        source="Company Filings",
        supporting_sources=[
            "Annual Reports",
            "Company Announcements",
        ],
        sectors=[
            "Capital Goods",
        ],
    )

    # ==========================================================
    # AGGREGATE
    # ==========================================================

    signals = [
        government_capex,
        order_inflow,
        capacity_expansion,
    ]

    cluster = engine.aggregate(
        signals,
        theme="Indian Capital Goods Cycle",
        cluster_id="THEME-001",
    )

    print("\nTheme")
    print(
        f"Theme : {cluster.theme}"
    )

    print(
        f"Signals : {cluster.signal_count}"
    )

    print(
        f"Independent Sources : "
        f"{cluster.independent_sources}"
    )

    print(
        f"Average Strength : "
        f"{cluster.average_strength:.2f}"
    )

    print(
        f"Cluster Score : "
        f"{cluster.cluster_score:.2f}"
    )

    print(
        f"Confidence : "
        f"{cluster.confidence:.2f}"
    )

    print(
        f"Emerging : "
        f"{cluster.emerging}"
    )

    assert cluster.signal_count == 3

    assert (
        cluster.independent_sources >= 3
    )

    assert (
        cluster.cluster_score >= 60
    )

    assert cluster.confidence >= 60

    assert cluster.emerging

    print("\nAggregation Test : PASS")

    # ==========================================================
    # CONTRADICTION TEST
    # ==========================================================

    contradictory = Signal(
        signal_id="AGG-004",
        title="Industrial Demand Warning",
        description="Some indicators show weakening demand.",
        domain=SignalDomain.SECTOR,
        signal_type=SignalType.DECELERATION,
        direction=SignalDirection.NEGATIVE,
        magnitude=65.0,
        probability=70.0,
        relevance=75.0,
        persistence=60.0,
        confidence=70.0,
        source="Industry Survey",
        contradictory_evidence=[
            "Demand weakness evidence",
        ],
        sectors=[
            "Capital Goods",
        ],
    )

    cluster_with_contradiction = engine.aggregate(
        signals + [contradictory],
        theme="Capital Goods Cycle With Contradiction",
        cluster_id="THEME-002",
    )

    print("\nContradiction Test")

    print(
        f"Contradictions : "
        f"{cluster_with_contradiction.contradiction_count}"
    )

    print(
        f"Confidence : "
        f"{cluster_with_contradiction.confidence:.2f}"
    )

    assert (
        cluster_with_contradiction.contradiction_count
        > 0
    )

    print(
        "Contradiction Handling : PASS"
    )

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n" + "=" * 60)
    print("SIGNAL AGGREGATION : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()