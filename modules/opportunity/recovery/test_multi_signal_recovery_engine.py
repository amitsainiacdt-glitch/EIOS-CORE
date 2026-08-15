"""
EIOS
Everest Investment Operating System

Multi-Signal Recovery Engine Test
"""

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
    RecoveryDirection,
    RecoveryStage,
)

from modules.opportunity.recovery.recovery_evidence import (
    RecoveryEvidence,
)

from modules.opportunity.recovery.multi_signal_recovery_assessment import (
    MultiSignalRecoveryAssessment,
    MultiSignalRecoveryDirection,
    MultiSignalRecoveryStage,
)

from modules.opportunity.recovery.multi_signal_recovery_engine import (
    MultiSignalRecoveryEngine,
)


# ==========================================================
# HELPERS
# ==========================================================


def make_assessment(
    direction=RecoveryDirection.UNKNOWN,
    stage=RecoveryStage.DETERIORATING,
    temporal_support=0.0,
    inflection=False,
    reversal=False,
    persistence=False,
):
    return RecoveryAssessment(
        stage=stage,
        direction=direction,
        temporal_support=temporal_support,
        inflection_detected=inflection,
        reversal_detected=reversal,
        persistence_detected=persistence,
    )


def make_evidence(
    signal_id,
    source_key,
    direction=RecoveryDirection.UNKNOWN,
    stage=RecoveryStage.DETERIORATING,
    temporal_support=0.0,
    inflection=False,
    reversal=False,
    persistence=False,
):
    return RecoveryEvidence(
        signal_id=signal_id,
        source_key=source_key,
        recovery_assessment=make_assessment(
            direction=direction,
            stage=stage,
            temporal_support=temporal_support,
            inflection=inflection,
            reversal=reversal,
            persistence=persistence,
        ),
    )


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    engine = MultiSignalRecoveryEngine()

    # ======================================================
    # ENGINE EXISTS
    # ======================================================

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
        MultiSignalRecoveryAssessment,
    )

    assert (
        result.stage
        == MultiSignalRecoveryStage.INSUFFICIENT_EVIDENCE
    )

    assert (
        result.total_signals
        == 0
    )

    assert result.warnings

    print(
        "Empty Input                     : PASS"
    )

    # ======================================================
    # SINGLE POSITIVE SIGNAL
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            inflection=True,
        )
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.total_signals
        == 1
    )

    assert (
        result.improving_signals
        == 1
    )

    assert (
        result.direction
        == MultiSignalRecoveryDirection.POSITIVE
    )

    assert (
        result.stage
        == MultiSignalRecoveryStage.INSUFFICIENT_EVIDENCE
    )

    print(
        "Single Signal Insufficient    : PASS"
    )

    # ======================================================
    # ISOLATED IMPROVEMENT
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            direction=RecoveryDirection.NEGATIVE,
            stage=RecoveryStage.DETERIORATING,
            temporal_support=20.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.isolated_improvement
        is True
    )

    assert (
        result.stage
        == MultiSignalRecoveryStage.ISOLATED_IMPROVEMENT
    )

    print(
        "Isolated Improvement           : PASS"
    )

    # ======================================================
    # BROAD STABILIZATION
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            direction=RecoveryDirection.STABILIZING,
            stage=RecoveryStage.STABILIZING,
            temporal_support=65.0,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            direction=RecoveryDirection.STABILIZING,
            stage=RecoveryStage.STABILIZING,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_INFLECTION,
            temporal_support=75.0,
            inflection=True,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.broad_stabilization
        is True
    )

    assert (
        result.stage
        == MultiSignalRecoveryStage.BROAD_STABILIZATION
    )

    print(
        "Broad Stabilization            : PASS"
    )

    # ======================================================
    # EARLY BROAD RECOVERY
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=80.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            direction=RecoveryDirection.STABILIZING,
            stage=RecoveryStage.EARLY_INFLECTION,
            temporal_support=70.0,
            inflection=True,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.stage
        == MultiSignalRecoveryStage.EARLY_BROAD_RECOVERY
    )

    assert (
        result.broad_inflection
        is True
    )

    assert (
        result.breadth_score
        >= 60.0
    )

    assert (
        result.corroboration_score
        >= 40.0
    )

    print(
        "Early Broad Recovery           : PASS"
    )

    # ======================================================
    # CONFIRMED BROAD RECOVERY
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SRC-001",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.CONFIRMED_RECOVERY,
            temporal_support=85.0,
            reversal=True,
            persistence=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.CONFIRMED_RECOVERY,
            temporal_support=90.0,
            reversal=True,
            persistence=True,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=80.0,
            reversal=True,
            persistence=True,
        ),
        make_evidence(
            "SIG-004",
            "SRC-004",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.CONFIRMED_RECOVERY,
            temporal_support=85.0,
            reversal=True,
            persistence=True,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.stage
        == MultiSignalRecoveryStage.CONFIRMED_BROAD_RECOVERY
    )

    assert (
        result.broad_reversal
        is True
    )

    assert (
        result.persistent_recovery
        is True
    )

    assert (
        result.confidence
        >= 70.0
    )

    print(
        "Confirmed Broad Recovery       : PASS"
    )

    # ======================================================
    # SOURCE DEDUPLICATION
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-001",
            "SAME-SOURCE",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-002",
            "SAME-SOURCE",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-003",
            "SAME-SOURCE",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        result.corroboration_score
        == 20.0
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
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            direction=RecoveryDirection.NEGATIVE,
            stage=RecoveryStage.DETERIORATING,
            temporal_support=20.0,
        ),
    ]

    result = engine.assess(
        evidence
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
    # SIGNAL ID TRACKING
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-A",
            "SRC-A",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=70.0,
        ),
        make_evidence(
            "SIG-B",
            "SRC-B",
            direction=RecoveryDirection.STABILIZING,
            stage=RecoveryStage.STABILIZING,
            temporal_support=65.0,
        ),
    ]

    result = engine.assess(
        evidence
    )

    assert (
        "SIG-A"
        in result.supporting_signal_ids
    )

    assert (
        "SIG-B"
        in result.supporting_signal_ids
    )

    print(
        "Signal ID Tracking             : PASS"
    )

    # ======================================================
    # TEMPORAL SUPPORT
    # ======================================================

    assert (
        result.temporal_score
        > 0.0
    )

    print(
        "Temporal Support               : PASS"
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
    # INPUT IMMUTABILITY
    # ======================================================

    evidence = [
        make_evidence(
            "SIG-IMMUTABLE",
            "SRC-IMMUTABLE",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            inflection=True,
        )
    ]

    original_id = (
        evidence[0].signal_id
    )

    original_source = (
        evidence[0].source_key
    )

    original_stage = (
        evidence[0]
        .recovery_assessment
        .stage
    )

    engine.assess(
        evidence
    )

    assert (
        evidence[0].signal_id
        == original_id
    )

    assert (
        evidence[0].source_key
        == original_source
    )

    assert (
        evidence[0]
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
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=75.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-002",
            "SRC-002",
            direction=RecoveryDirection.POSITIVE,
            stage=RecoveryStage.EARLY_RECOVERY,
            temporal_support=80.0,
            inflection=True,
        ),
        make_evidence(
            "SIG-003",
            "SRC-003",
            direction=RecoveryDirection.STABILIZING,
            stage=RecoveryStage.STABILIZING,
            temporal_support=70.0,
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
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS MULTI-SIGNAL RECOVERY ENGINE : PASS"
    )


if __name__ == "__main__":
    main()