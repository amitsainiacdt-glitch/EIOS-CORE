"""
EIOS
Everest Investment Operating System

Full Signal → Catalyst Pipeline Test
====================================

Purpose
-------
Verifies the complete Opportunity Intelligence path:

EvidenceItem
    ↓
SignalInterpretation
    ↓
SignalInterpretationEngine
    ↓
Signal
    ↓
SignalIntelligenceEngine
    ↓
TemporalSignalEngine
    ↓
SignalAggregationEngine
    ↓
SignalCluster
    ↓
SignalClusterCatalystBridge
    ↓
CatalystClassifier

Design Principles
-----------------
- Existing engines are reused.
- No parallel analytical engine is created.
- EvidenceItem remains unchanged.
- Signal remains unchanged after creation.
- SignalCluster remains unchanged.
- Catalyst classification remains inside CatalystClassifier.
- No valuation.
- No opportunity scoring.
- No portfolio allocation.
- No investment decision.
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

from modules.opportunity.signals.signal_intelligence import (
    SignalIntelligenceEngine,
)

from modules.opportunity.signals.temporal_signal_engine import (
    TemporalSignalEngine,
)

from modules.opportunity.signals.signal_aggregation import (
    SignalAggregationEngine,
)

from modules.opportunity.catalyst.signal_cluster_catalyst_bridge import (
    SignalClusterCatalystBridge,
)

from modules.opportunity.signals.signal_model import (
    SignalDomain,
    SignalType,
    SignalDirection,
    SignalStage,
    TimeHorizon,
)


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    print("=" * 60)
    print(
        "EIOS FULL SIGNAL → CATALYST PIPELINE TEST"
    )
    print("=" * 60)

    # ======================================================
    # TEST 1 — EVIDENCE CREATION
    # ======================================================

    evidence = EvidenceItem(
        evidence_id="PIPE-EVIDENCE-001",

        statement=(
            "Industrial capital expenditure is "
            "accelerating across the sector."
        ),

        source="Industry Research",

        category="Capital Cycle",

        direction="Supporting",

        strength=90.0,

        confidence=85.0,

        independent_confirmation=3,

        is_primary_source=False,

        is_time_sensitive=False,

        notes="Synthetic pipeline evidence.",
    )

    assert evidence.evidence_id == (
        "PIPE-EVIDENCE-001"
    )

    original_evidence_id = (
        evidence.evidence_id
    )

    original_statement = (
        evidence.statement
    )

    original_source = (
        evidence.source
    )

    print(
        "Test 1 — Evidence Creation             : PASS"
    )

    # ======================================================
    # TEST 2 — EXPLICIT SIGNAL INTERPRETATION
    # ======================================================

    interpretation = SignalInterpretation(

        title=(
            "Industrial Capital Cycle Acceleration"
        ),

        description=(
            "Industrial capital expenditure is "
            "accelerating, indicating improving "
            "capital-cycle conditions."
        ),

        domain=SignalDomain.CAPITAL_CYCLE,

        signal_type=SignalType.ACCELERATION,

        direction=SignalDirection.POSITIVE,

        stage=SignalStage.VALIDATED,

        horizon=TimeHorizon.MEDIUM_TERM,

        sectors=[
            "Capital Goods",
        ],

        companies=[
            "TEST COMPANY",
        ],

        themes=[
            "Capital Cycle",
            "Industrial Capex",
        ],

        economic_mechanism=(
            "Higher capital expenditure increases "
            "industry demand and capacity utilisation."
        ),

        supply_demand_impact=(
            "Improving demand with increasing "
            "capacity utilisation."
        ),

        earnings_impact=(
            "Higher utilisation may support "
            "revenue and margin expansion."
        ),

        valuation_impact=(
            "Improving earnings visibility may "
            "support valuation recognition."
        ),

        magnitude=85.0,

        probability=85.0,

        persistence=80.0,

        relevance=90.0,

        market_expectation=(
            "Market expectations remain moderate."
        ),

        market_recognition=30.0,

        price_reaction=(
            "Limited market recognition."
        ),

        causal_chain=[
            "Government / private capex",
            "Industrial orders",
            "Capacity utilisation",
            "Revenue growth",
            "Earnings growth",
        ],

        beneficiaries=[
            "Capital Goods",
        ],

        adversely_affected=[],

        historical_precedent=(
            "Prior industrial capex cycles."
        ),

        invalidation_conditions=[
            "Industrial orders materially weaken.",
            "Capex plans are cancelled.",
        ],
    )

    print(
        "Test 2 — Explicit Interpretation       : PASS"
    )

    # ======================================================
    # TEST 3 — EVIDENCE → SIGNAL
    # ======================================================

    interpretation_engine = (
        SignalInterpretationEngine()
    )

    interpretation_result = (
        interpretation_engine.create(
            evidence=evidence,
            interpretation=interpretation,
            signal_id="PIPE-SIGNAL-001",
        )
    )

    assert interpretation_result.accepted

    assert interpretation_result.signal is not None

    signal = (
        interpretation_result.signal
    )

    assert signal.signal_id == (
        "PIPE-SIGNAL-001"
    )

    print(
        "Test 3 — Evidence → Signal             : PASS"
    )

    # ======================================================
    # TEST 4 — SIGNAL PROVENANCE
    # ======================================================

    assert signal.evidence == [
        "PIPE-EVIDENCE-001"
    ]

    assert signal.source == (
        "Industry Research"
    )

    assert signal.metadata[
        "evidence_id"
    ] == "PIPE-EVIDENCE-001"

    assert signal.metadata[
        "evidence_source"
    ] == "Industry Research"

    print(
        "Test 4 — Signal Provenance             : PASS"
    )

    # ======================================================
    # TEST 5 — SIGNAL INTELLIGENCE
    # ======================================================

    intelligence_engine = (
        SignalIntelligenceEngine()
    )

    intelligence = (
        intelligence_engine.analyze(
            signal
        )
    )

    assert intelligence is not None

    assert (
        0.0
        <= intelligence.confidence
        <= 100.0
    )

    print(
        "Test 5 — Signal Intelligence            : PASS"
    )

    # ======================================================
    # TEST 6 — TEMPORAL SIGNAL ANALYSIS
    # ======================================================

    # Temporal analysis requires dated observations.
    # The canonical signal remains untouched.
    #
    # We explicitly create two temporal observations
    # using the same interpretation/provenance boundary.

    temporal_signals = []

    first_result = (
        interpretation_engine.create(
            evidence=evidence,
            interpretation=interpretation,
            signal_id="PIPE-SIGNAL-002",
        )
    )

    first_signal = (
        first_result.signal
    )

    assert first_signal is not None

    first_signal.detected_date = (
        "2026-01-01"
    )

    second_result = (
        interpretation_engine.create(
            evidence=evidence,
            interpretation=interpretation,
            signal_id="PIPE-SIGNAL-003",
        )
    )

    second_signal = (
        second_result.signal
    )

    assert second_signal is not None

    second_signal.detected_date = (
        "2026-03-01"
    )

    temporal_signals.extend(
        [
            first_signal,
            second_signal,
        ]
    )

    temporal_engine = (
        TemporalSignalEngine()
    )

    temporal_result = (
        temporal_engine.analyze(
            temporal_signals
        )
    )

    assert temporal_result is not None

    assert (
        temporal_result.valid_observations
        == 2
    )

    print(
        "Test 6 — Temporal Signal Analysis      : PASS"
    )

    # ======================================================
    # TEST 7 — SIGNAL AGGREGATION
    # ======================================================

    aggregation_engine = (
        SignalAggregationEngine()
    )

    cluster = (
        aggregation_engine.aggregate(
            [
                signal,
                first_signal,
                second_signal,
            ],
            theme="Industrial Capital Cycle",
            cluster_id="PIPE-CLUSTER-001",
        )
    )

    assert cluster is not None

    assert (
        cluster.signal_count
        == 3
    )

    print(
        "Test 7 — Signal Aggregation             : PASS"
    )

    # ======================================================
    # TEST 8 — CLUSTER QUALITY
    # ======================================================

    assert (
        cluster.cluster_score
        >= 60.0
    )

    assert (
        cluster.confidence
        >= 60.0
    )

    print(
        "Test 8 — Cluster Quality                : PASS"
    )

    # ======================================================
    # TEST 9 — CLUSTER → CATALYST
    # ======================================================

    bridge = (
        SignalClusterCatalystBridge()
    )

    catalyst_result = (
        bridge.classify(
            cluster=cluster
        )
    )

    assert catalyst_result is not None

    print(
        "Test 9 — Cluster → Catalyst             : PASS"
    )

    # ======================================================
    # TEST 10 — CATALYST CLASSIFICATION
    # ======================================================

    assert catalyst_result.is_classified

    assert (
        catalyst_result.primary
        is not None
    )

    print(
        "Test 10 — Catalyst Classification       : PASS"
    )

    # ======================================================
    # TEST 11 — PRIMARY CATALYST
    # ======================================================

    print(
        "Primary Catalyst : "
        f"{catalyst_result.primary.family.value}"
    )

    assert (
        catalyst_result.primary.family
        is not None
    )

    print(
        "Test 11 — Primary Catalyst              : PASS"
    )

    # ======================================================
    # TEST 12 — CATALYST CONFIDENCE
    # ======================================================

    print(
        "Catalyst Confidence : "
        f"{catalyst_result.confidence:.2f}"
    )

    assert (
        0.0
        <= catalyst_result.confidence
        <= 100.0
    )

    print(
        "Test 12 — Catalyst Confidence           : PASS"
    )

    # ======================================================
    # TEST 13 — EVIDENCE IMMUTABILITY
    # ======================================================

    assert evidence.evidence_id == (
        original_evidence_id
    )

    assert evidence.statement == (
        original_statement
    )

    assert evidence.source == (
        original_source
    )

    print(
        "Test 13 — Evidence Preservation         : PASS"
    )

    # ======================================================
    # TEST 14 — SIGNAL PROVENANCE AFTER
    #              FULL PIPELINE
    # ======================================================

    assert signal.signal_id == (
        "PIPE-SIGNAL-001"
    )

    assert signal.evidence == [
        "PIPE-EVIDENCE-001"
    ]

    assert signal.source == (
        "Industry Research"
    )

    print(
        "Test 14 — Final Signal Provenance      : PASS"
    )

    # ======================================================
    # TEST 15 — CLUSTER PRESERVATION
    # ======================================================

    assert cluster.cluster_id == (
        "PIPE-CLUSTER-001"
    )

    assert cluster.theme == (
        "Industrial Capital Cycle"
    )

    assert cluster.signal_count == 3

    print(
        "Test 15 — Cluster Preservation          : PASS"
    )

    # ======================================================
    # TEST 16 — ANALYTICAL BOUNDARY
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
        "Test 16 — Analytical Boundary           : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print("=" * 60)

    print(
        "EIOS FULL SIGNAL → CATALYST PIPELINE "
        ": ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()