"""
EIOS
Everest Investment Operating System

Recovery Breadth Engine Test
"""

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
    RecoveryClusterDirection,
    RecoveryClusterStage,
    RecoveryClusterType,
)

from modules.opportunity.recovery.recovery_breadth_assessment import (
    RecoveryBreadthStage,
    RecoveryBreadthDirection,
    RecoveryBreadthType,
    RecoveryLeadershipState,
)

from modules.opportunity.recovery.recovery_breadth_engine import (
    RecoveryBreadthEngine,
)


def make_cluster(
    cluster_id,
    supporting=0,
    stabilizing=0,
    deteriorating=0,
    inflection=50.0,
    early=False,
    confirmed=False,
    contradiction=0.0,
    corroboration=60.0,
    temporal=70.0,
):
    return RecoveryClusterAssessment(
        cluster_id=cluster_id,
        cluster_name=cluster_id,
        cluster_type=RecoveryClusterType.SECTOR,
        direction=(
            RecoveryClusterDirection.POSITIVE
            if supporting > 0
            else RecoveryClusterDirection.STABILIZING
        ),
        stage=(
            RecoveryClusterStage.CONFIRMED_RECOVERY_CLUSTER
            if confirmed
            else (
                RecoveryClusterStage.EARLY_RECOVERY_CLUSTER
                if early
                else RecoveryClusterStage.STABILIZING_CLUSTER
            )
        ),
        supporting_assessments=supporting,
        stabilizing_assessments=stabilizing,
        deteriorating_assessments=deteriorating,
        inflection_breadth=inflection,
        early_recovery_cluster=early,
        confirmed_recovery_cluster=confirmed,
        contradiction_score=contradiction,
        corroboration_score=corroboration,
        temporal_score=temporal,
        independent_sources=3,
        independent_signals=3,
        independent_domains=2,
    )


def main() -> None:

    # ======================================================
    # ENGINE
    # ======================================================

    engine = RecoveryBreadthEngine()

    assert engine is not None

    print(
        "Engine Exists                   : PASS"
    )

    # ======================================================
    # EMPTY INPUT
    # ======================================================

    result = engine.assess([])

    assert (
        result.stage
        == RecoveryBreadthStage.INSUFFICIENT
    )

    assert (
        result.direction
        == RecoveryBreadthDirection.UNKNOWN
    )

    assert result.warnings

    print(
        "Empty Input                     : PASS"
    )

    # ======================================================
    # ISOLATED IMPROVEMENT
    # ======================================================

    result = engine.assess(
        [
            make_cluster(
                "SECTOR-A",
                supporting=1,
                early=True,
            )
        ],
        breadth_id="TEST",
        breadth_name="Test Universe",
        breadth_type=RecoveryBreadthType.SECTOR,
    )

    assert (
        result.stage
        == RecoveryBreadthStage.ISOLATED
    )

    assert (
        result.recovery_breadth
        == 100.0
    )

    print(
        "Isolated Improvement           : PASS"
    )

    # ======================================================
    # EARLY BREADTH
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            early=True,
        ),
        make_cluster(
            "B",
            supporting=1,
        ),
        make_cluster(
            "C",
            stabilizing=1,
        ),
        make_cluster(
            "D",
            deteriorating=1,
        ),
    ]

    result = engine.assess(
        assessments,
        previous_breadth=10.0,
    )

    assert (
        result.recovery_breadth
        >= 25.0
    )

    assert (
        result.direction
        == RecoveryBreadthDirection.EXPANDING
    )

    assert (
        result.stage
        == RecoveryBreadthStage.EARLY_BREADTH
    )

    assert (
        result.early_breadth_signal
        is True
    )

    print(
        "Early Breadth Expansion        : PASS"
    )

    # ======================================================
    # BROADENING
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            early=True,
        ),
        make_cluster(
            "B",
            supporting=1,
            early=True,
        ),
        make_cluster(
            "C",
            supporting=1,
        ),
        make_cluster(
            "D",
            stabilizing=1,
        ),
        make_cluster(
            "E",
            stabilizing=1,
        ),
        make_cluster(
            "F",
            deteriorating=1,
        ),
        make_cluster(
            "G",
            deteriorating=1,
        ),
        make_cluster(
            "H",
            deteriorating=1,
        ),
    ]

    result = engine.assess(
        assessments,
        previous_breadth=25.0,
    )

    assert (
        result.recovery_breadth
        >= 50.0
    )

    assert (
        result.direction
        == RecoveryBreadthDirection.EXPANDING
    )

    assert (
        result.stage
        == RecoveryBreadthStage.BROADENING
    )

    assert (
        result.recovery_breadth_signal
        is True
    )

    print(
        "Broadening Recovery            : PASS"
    )

    # ======================================================
    # BROAD RECOVERY
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "B",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "C",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "D",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "E",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "F",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "G",
            stabilizing=1,
        ),
        make_cluster(
            "H",
            stabilizing=1,
        ),
    ]

    result = engine.assess(
        assessments,
        previous_breadth=60.0,
    )

    assert (
        result.current_breadth
        >= 70.0
    )

    assert (
        result.confirmed_recovery_breadth
        >= 40.0
    )

    assert (
        result.stage
        == RecoveryBreadthStage.BROAD_RECOVERY
    )

    assert (
        result.confirmed_breadth_signal
        is True
    )

    print(
        "Broad Recovery                 : PASS"
    )

    # ======================================================
    # SATURATED RECOVERY
    # ======================================================

    assessments = [
        make_cluster(
            f"SECTOR-{i}",
            supporting=1,
            confirmed=True,
        )
        for i in range(9)
    ]

    result = engine.assess(
        assessments,
        previous_breadth=80.0,
    )

    assert (
        result.current_breadth
        >= 85.0
    )

    assert (
        result.confirmed_recovery_breadth
        >= 60.0
    )

    assert (
        result.stage
        == RecoveryBreadthStage.SATURATED
    )

    print(
        "Saturated Recovery             : PASS"
    )

    # ======================================================
    # CONTRACTING BREADTH
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            early=True,
        ),
        make_cluster(
            "B",
            supporting=1,
        ),
        make_cluster(
            "C",
            stabilizing=1,
        ),
        make_cluster(
            "D",
            deteriorating=1,
        ),
        make_cluster(
            "E",
            deteriorating=1,
        ),
        make_cluster(
            "F",
            deteriorating=1,
        ),
        make_cluster(
            "G",
            deteriorating=1,
        ),
        make_cluster(
            "H",
            deteriorating=1,
        ),
    ]

    result = engine.assess(
        assessments,
        previous_breadth=80.0,
    )

    assert (
        result.direction
        == RecoveryBreadthDirection.CONTRACTING
    )

    assert (
        result.breadth_contracting
        is True
    )

    assert (
        result.stage
        == RecoveryBreadthStage.CONTRACTING
    )

    print(
        "Contracting Breadth             : PASS"
    )

    # ======================================================
    # LEADERSHIP
    # ======================================================

    assessments = [
        make_cluster(
            "LEADER-A",
            supporting=1,
            early=True,
        ),
        make_cluster(
            "LEADER-B",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "FOLLOWER-C",
            stabilizing=1,
        ),
        make_cluster(
            "FOLLOWER-D",
            stabilizing=1,
        ),
    ]

    result = engine.assess(
        assessments,
        previous_breadth=20.0,
    )

    assert (
        result.leader_count
        == 2
    )

    assert (
        result.leading_entities
        == [
            "LEADER-A",
            "LEADER-B",
        ]
    )

    assert (
        result.leadership_state
        == RecoveryLeadershipState.CLEAR_LEADERS
    )

    print(
        "Recovery Leadership            : PASS"
    )

    # ======================================================
    # CONTRADICTION
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            early=True,
            contradiction=10.0,
        ),
        make_cluster(
            "B",
            supporting=1,
            early=True,
            contradiction=20.0,
        ),
        make_cluster(
            "C",
            deteriorating=1,
            contradiction=80.0,
        ),
    ]

    result = engine.assess(
        assessments,
        previous_breadth=20.0,
    )

    assert (
        result.contradiction_score
        > 0.0
    )

    assert result.warnings

    print(
        "Contradictory Evidence         : PASS"
    )

    # ======================================================
    # BREADTH METRICS
    # ======================================================

    assert (
        0.0
        <= result.improvement_breadth
        <= 100.0
    )

    assert (
        0.0
        <= result.recovery_breadth
        <= 100.0
    )

    assert (
        0.0
        <= result.confirmed_recovery_breadth
        <= 100.0
    )

    print(
        "Breadth Metric Range           : PASS"
    )

    # ======================================================
    # CONFIDENCE
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
    # INPUT IMMUTABILITY
    # ======================================================

    original = make_cluster(
        "IMMUTABLE",
        supporting=1,
        early=True,
    )

    original_stage = (
        original.stage
    )

    original_breadth = (
        original.inflection_breadth
    )

    engine.assess(
        [original],
        previous_breadth=0.0,
    )

    assert (
        original.stage
        == original_stage
    )

    assert (
        original.inflection_breadth
        == original_breadth
    )

    print(
        "Input Immutability             : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            early=True,
        ),
        make_cluster(
            "B",
            supporting=1,
        ),
        make_cluster(
            "C",
            stabilizing=1,
        ),
    ]

    first = engine.assess(
        assessments,
        previous_breadth=10.0,
    )

    second = engine.assess(
        assessments,
        previous_breadth=10.0,
    )

    assert (
        first == second
    )

    print(
        "Deterministic Assessment       : PASS"
    )

    # ======================================================
    # TRANSPARENT REASONING
    # ======================================================

    assert (
        first.reasons
        or first.warnings
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
        "EIOS RECOVERY BREADTH ENGINE : PASS"
    )


if __name__ == "__main__":
    main()