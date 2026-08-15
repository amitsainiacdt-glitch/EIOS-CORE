"""
EIOS
Everest Investment Operating System

Recovery Cluster Engine Test
"""

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
    RecoveryDirection,
    RecoveryStage,
)

from modules.opportunity.recovery.recovery_evidence import (
    RecoveryEvidence,
)

from modules.opportunity.recovery.recovery_cluster_evidence import (
    RecoveryClusterEvidence,
)

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
    RecoveryClusterDirection,
    RecoveryClusterStage,
    RecoveryClusterType,
)

from modules.opportunity.recovery.recovery_cluster_engine import (
    RecoveryClusterEngine,
)


# ==========================================================
# HELPERS
# ==========================================================


def make_evidence(
    signal_id,
    source_key,
    direction,
    stage,
    temporal_support=0.0,
    reversal=False,
    persistence=False,
    cluster_key="INDUSTRIAL",
    cluster_name="Industrial Recovery",
    cluster_type=RecoveryClusterType.SECTOR,
):
    assessment = RecoveryAssessment(
        direction=direction,
        stage=stage,
        temporal_support=temporal_support,
        reversal_detected=reversal,
        persistence_detected=persistence,
    )

    recovery_evidence = RecoveryEvidence(
        signal_id=signal_id,
        source_key=source_key,
        recovery_assessment=assessment,
    )

    return RecoveryClusterEvidence(
        cluster_key=cluster_key,
        cluster_name=cluster_name,
        cluster_type=cluster_type,
        recovery_evidence=recovery_evidence,
    )


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    # ======================================================
    # ENGINE
    # ======================================================

    engine = RecoveryClusterEngine()

    assert engine is not None

    print(
        "Engine Exists                   : PASS"
    )

    # ======================================================
    # EMPTY INPUT
    # ======================================================

    result = engine.assess([])

    assert isinstance(
        result,
        RecoveryClusterAssessment,
    )

    assert (
        result.stage
        == RecoveryClusterStage.INSUFFICIENT_EVIDENCE
    )

    assert (
        result.total_recovery_assessments
        == 0
    )

    assert result.warnings

    print(
        "Empty Input                     : PASS"
    )

    # ======================================================
    # SINGLE SIGNAL
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
        )
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.total_recovery_assessments
        == 1
    )

    assert (
        result.supporting_assessments
        == 1
    )

    assert (
        result.direction
        == RecoveryClusterDirection.POSITIVE
    )

    assert (
        result.stage
        == RecoveryClusterStage.INSUFFICIENT_EVIDENCE
    )

    print(
        "Single Signal Insufficient     : PASS"
    )

    # ======================================================
    # EARLY CLUSTERING
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            RecoveryDirection.STABILIZING,
            RecoveryStage.STABILIZING,
            temporal_support=65.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.emerging_cluster
        is True
    )

    assert (
        result.stage
        == RecoveryClusterStage.EARLY_CLUSTERING
    )

    print(
        "Early Clustering               : PASS"
    )

    # ======================================================
    # STABILIZING CLUSTER
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.STABILIZING,
            RecoveryStage.STABILIZING,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            RecoveryDirection.STABILIZING,
            RecoveryStage.STABILIZING,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_INFLECTION,
            temporal_support=75.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.stabilizing_cluster
        is True
    )

    assert (
        result.stage
        == RecoveryClusterStage.STABILIZING_CLUSTER
    )

    assert (
        result.breadth_score
        >= 60.0
    )

    print(
        "Stabilizing Cluster            : PASS"
    )

    # ======================================================
    # EARLY RECOVERY CLUSTER
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            reversal=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=80.0,
            reversal=True,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            RecoveryDirection.STABILIZING,
            RecoveryStage.EARLY_INFLECTION,
            temporal_support=70.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.early_recovery_cluster
        is True
    )

    assert (
        result.stage
        == RecoveryClusterStage.EARLY_RECOVERY_CLUSTER
    )

    assert (
        result.broad_based
        is True
    )

    assert (
        result.confidence
        >= 0.0
    )

    print(
        "Early Recovery Cluster        : PASS"
    )

    # ======================================================
    # CONFIRMED RECOVERY CLUSTER
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.POSITIVE,
            RecoveryStage.CONFIRMED_RECOVERY,
            temporal_support=85.0,
            reversal=True,
            persistence=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            RecoveryDirection.POSITIVE,
            RecoveryStage.CONFIRMED_RECOVERY,
            temporal_support=90.0,
            reversal=True,
            persistence=True,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            RecoveryDirection.POSITIVE,
            RecoveryStage.CONFIRMED_RECOVERY,
            temporal_support=85.0,
            reversal=True,
            persistence=True,
        ),
        make_evidence(
            "SIG-004",
            "SRC-004",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=80.0,
            reversal=True,
            persistence=True,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.confirmed_recovery_cluster
        is True
    )

    assert (
        result.stage
        == RecoveryClusterStage.CONFIRMED_RECOVERY_CLUSTER
    )

    assert (
        result.reversal_breadth
        >= 40.0
    )

    assert (
        result.persistence_breadth
        >= 40.0
    )

    assert (
        result.corroboration_score
        >= 60.0
    )

    assert (
        result.temporal_score
        >= 60.0
    )

    print(
        "Confirmed Recovery Cluster     : PASS"
    )

    # ======================================================
    # SOURCE DEDUPLICATION
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SAME-SOURCE",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-002",
            "SAME-SOURCE",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-003",
            "SAME-SOURCE",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.independent_sources
        == 1
    )

    assert (
        result.corroboration_score
        < 60.0
    )

    print(
        "Source Deduplication            : PASS"
    )

    # ======================================================
    # CONTRADICTION
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            RecoveryDirection.NEGATIVE,
            RecoveryStage.DETERIORATING,
            temporal_support=20.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.deteriorating_assessments
        == 1
    )

    assert (
        result.contradiction_score
        > 0.0
    )

    assert (
        "SIG-003"
        in result.contradictory_signal_ids
    )

    assert result.warnings

    print(
        "Contradictory Evidence         : PASS"
    )

    # ======================================================
    # IDENTITY
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-ID",
            "SRC-ID",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
        )
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.cluster_id
        == "INDUSTRIAL"
    )

    assert (
        result.cluster_name
        == "Industrial Recovery"
    )

    assert (
        result.cluster_type
        == RecoveryClusterType.SECTOR
    )

    print(
        "Cluster Identity               : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-IMMUTABLE",
            "SRC-IMMUTABLE",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
        )
    ]

    original_signal_id = (
        evidence[0]
        .recovery_evidence
        .signal_id
    )

    original_source_key = (
        evidence[0]
        .recovery_evidence
        .source_key
    )

    original_stage = (
        evidence[0]
        .recovery_evidence
        .recovery_assessment
        .stage
    )

    engine.assess(
        evidence
    )

    assert (
        evidence[0]
        .recovery_evidence
        .signal_id
        == original_signal_id
    )

    assert (
        evidence[0]
        .recovery_evidence
        .source_key
        == original_source_key
    )

    assert (
        evidence[0]
        .recovery_evidence
        .recovery_assessment
        .stage
        == original_stage
    )

    print(
        "Input Immutability             : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            RecoveryDirection.STABILIZING,
            RecoveryStage.STABILIZING,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            RecoveryDirection.POSITIVE,
            RecoveryStage.EARLY_RECOVERY,
            temporal_support=80.0,
        ),
    ]

    first = engine.assess(
        evidence
    )

    second = engine.assess(
        evidence
    )

    assert (
        first == second
    )

    print(
        "Deterministic Assessment       : PASS"
    )

    # ======================================================
    # CONFIDENCE RANGE
    # ======================================================

    assert (
        0.0
        <= result.confidence
        <= 100.0
    )

    print(
        "Confidence Range               : PASS"
    )

    # ======================================================
    # TRANSPARENT REASONING
    # ======================================================

    assert (
        result.reasons
        or result.warnings
    )

    print(
        "Transparent Reasoning          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY CLUSTER ENGINE : PASS"
    )


if __name__ == "__main__":
    main()