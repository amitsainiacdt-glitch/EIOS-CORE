"""
EIOS
Everest Investment Operating System

Recovery Detection Engine Test
"""

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
    RecoveryDirection,
    RecoveryStage,
)

from modules.opportunity.recovery.recovery_engine import (
    RecoveryDetectionEngine,
)

from modules.opportunity.signals.signal_model import (
    SignalDirection,
)

from modules.opportunity.signals.temporal_signal_engine import (
    TemporalSignalEvolution,
)


def make_temporal(
    *,
    direction=SignalDirection.UNKNOWN,
    trend=False,
    accelerating=False,
    decelerating=False,
    stabilizing=False,
    inflection=False,
    bottoming=False,
    reversal=False,
    persistent=False,
    confidence=0.0,
):
    return TemporalSignalEvolution(
        direction=direction,
        trend=trend,
        accelerating=accelerating,
        decelerating=decelerating,
        stabilizing=stabilizing,
        inflection=inflection,
        bottoming=bottoming,
        reversal=reversal,
        persistent=persistent,
        confidence=confidence,
        observations=4,
        valid_observations=4,
    )


def main() -> None:

    # ======================================================
    # ENGINE EXISTS
    # ======================================================

    engine = RecoveryDetectionEngine()

    assert engine is not None

    print(
        "Engine Exists                   : PASS"
    )

    # ======================================================
    # RESULT TYPE
    # ======================================================

    temporal = make_temporal()

    result = engine.assess(
        temporal
    )

    assert isinstance(
        result,
        RecoveryAssessment,
    )

    print(
        "Assessment Result Type          : PASS"
    )

    # ======================================================
    # DEFAULT / DETERIORATING
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.NEGATIVE,
        )
    )

    assert (
        result.stage
        == RecoveryStage.DETERIORATING
    )

    assert (
        result.direction
        == RecoveryDirection.NEGATIVE
    )

    print(
        "Deteriorating Classification   : PASS"
    )

    # ======================================================
    # SLOWING DETERIORATION
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.NEGATIVE,
            decelerating=True,
            confidence=55.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.SLOWING_DETERIORATION
    )

    print(
        "Slowing Deterioration           : PASS"
    )

    # ======================================================
    # STABILIZING
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.NEUTRAL,
            stabilizing=True,
            bottoming=True,
            confidence=60.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.STABILIZING
    )

    assert result.stabilization_detected
    assert result.bottoming_detected

    print(
        "Stabilizing Classification      : PASS"
    )

    # ======================================================
    # EARLY INFLECTION
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.MIXED,
            inflection=True,
            confidence=65.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.EARLY_INFLECTION
    )

    assert result.inflection_detected

    print(
        "Early Inflection                : PASS"
    )

    # ======================================================
    # EARLY RECOVERY
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.POSITIVE,
            inflection=True,
            persistent=True,
            confidence=75.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.EARLY_RECOVERY
    )

    assert (
        result.direction
        == RecoveryDirection.POSITIVE
    )

    assert result.inflection_detected
    assert result.persistence_detected

    print(
        "Early Recovery                  : PASS"
    )

    # ======================================================
    # EARLY RECOVERY THROUGH REVERSAL
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.POSITIVE,
            reversal=True,
            trend=True,
            confidence=80.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.EARLY_RECOVERY
    )

    assert result.reversal_detected

    print(
        "Recovery Reversal               : PASS"
    )

    # ======================================================
    # CONFIRMED RECOVERY
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.POSITIVE,
            trend=True,
            accelerating=True,
            reversal=True,
            persistent=True,
            confidence=90.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.CONFIRMED_RECOVERY
    )

    assert (
        result.direction
        == RecoveryDirection.POSITIVE
    )

    assert result.reversal_detected
    assert result.persistence_detected

    print(
        "Confirmed Recovery              : PASS"
    )

    # ======================================================
    # EVIDENCE TRANSFER
    # ======================================================

    temporal = make_temporal(
        direction=SignalDirection.POSITIVE,
        trend=True,
        accelerating=True,
        stabilizing=True,
        inflection=True,
        bottoming=True,
        reversal=True,
        persistent=True,
        confidence=85.0,
    )

    result = engine.assess(
        temporal
    )

    assert (
        result.temporal_support
        > 0.0
    )

    assert (
        result.signal_breadth
        > 0.0
    )

    assert (
        result.corroboration
        > 0.0
    )

    assert (
        result.persistence
        == 100.0
    )

    print(
        "Evidence Transfer              : PASS"
    )

    # ======================================================
    # BOOLEAN TRANSFER
    # ======================================================

    assert (
        result.bottoming_detected
    )

    assert (
        result.stabilization_detected
    )

    assert (
        result.inflection_detected
    )

    assert (
        result.reversal_detected
    )

    assert (
        result.persistence_detected
    )

    print(
        "Temporal Feature Transfer      : PASS"
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
    # NO INPUT MUTATION
    # ======================================================

    temporal = make_temporal(
        direction=SignalDirection.POSITIVE,
        inflection=True,
        persistent=True,
        confidence=75.0,
    )

    original_direction = (
        temporal.direction
    )

    original_inflection = (
        temporal.inflection
    )

    engine.assess(
        temporal
    )

    assert (
        temporal.direction
        == original_direction
    )

    assert (
        temporal.inflection
        == original_inflection
    )

    print(
        "Input Immutability             : PASS"
    )

    # ======================================================
    # DETERMINISTIC RESULT
    # ======================================================

    temporal = make_temporal(
        direction=SignalDirection.POSITIVE,
        reversal=True,
        persistent=True,
        trend=True,
        accelerating=True,
        confidence=90.0,
    )

    first = engine.assess(
        temporal
    )

    second = engine.assess(
        temporal
    )

    assert first == second

    print(
        "Deterministic Assessment       : PASS"
    )

    # ======================================================
    # RECOVERY IS NOT JUST BOTTOMING
    # ======================================================

    result = engine.assess(
        make_temporal(
            direction=SignalDirection.NEUTRAL,
            bottoming=True,
            confidence=60.0,
        )
    )

    assert (
        result.stage
        == RecoveryStage.STABILIZING
    )

    assert (
        result.stage
        != RecoveryStage.EARLY_RECOVERY
    )

    print(
        "Bottoming ≠ Recovery           : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY DETECTION ENGINE : PASS"
    )


if __name__ == "__main__":
    main()