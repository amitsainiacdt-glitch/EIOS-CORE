"""
EIOS
Everest Investment Operating System

Recovery Assessment Model Test
"""

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
    RecoveryDirection,
    RecoveryStage,
)


def main() -> None:

    # ======================================================
    # TYPE INTEGRITY
    # ======================================================

    assessment = RecoveryAssessment()

    assert isinstance(
        assessment,
        RecoveryAssessment,
    )

    print(
        "Assessment Type                : PASS"
    )

    # ======================================================
    # DEFAULT STAGE
    # ======================================================

    assert (
        assessment.stage
        == RecoveryStage.DETERIORATING
    )

    print(
        "Default Stage                  : PASS"
    )

    # ======================================================
    # DEFAULT DIRECTION
    # ======================================================

    assert (
        assessment.direction
        == RecoveryDirection.UNKNOWN
    )

    print(
        "Default Direction              : PASS"
    )

    # ======================================================
    # ENUM INTEGRITY
    # ======================================================

    assert len(RecoveryStage) == 6
    assert len(RecoveryDirection) == 4

    print(
        "Enum Integrity                 : PASS"
    )

    # ======================================================
    # BOOLEAN FIELDS
    # ======================================================

    assert assessment.bottoming_detected is False
    assert assessment.stabilization_detected is False
    assert assessment.inflection_detected is False
    assert assessment.reversal_detected is False
    assert assessment.persistence_detected is False

    print(
        "Boolean Field Integrity        : PASS"
    )

    # ======================================================
    # LIST FIELDS
    # ======================================================

    assert isinstance(
        assessment.reasons,
        list,
    )

    assert isinstance(
        assessment.warnings,
        list,
    )

    print(
        "Explanation Fields             : PASS"
    )

    # ======================================================
    # RANGE DEFAULTS
    # ======================================================

    assert (
        assessment.temporal_support
        == 0.0
    )

    assert (
        assessment.signal_breadth
        == 0.0
    )

    assert (
        assessment.corroboration
        == 0.0
    )

    assert (
        assessment.persistence
        == 0.0
    )

    assert (
        assessment.contradiction
        == 0.0
    )

    assert (
        assessment.confidence
        == 0.0
    )

    print(
        "Numeric Defaults               : PASS"
    )

    # ======================================================
    # PASSIVE MODEL
    # ======================================================

    assessment.stage = (
        RecoveryStage.EARLY_RECOVERY
    )

    assessment.direction = (
        RecoveryDirection.POSITIVE
    )

    assessment.bottoming_detected = True
    assessment.stabilization_detected = True
    assessment.inflection_detected = True

    assessment.reasons.append(
        "Temporal evidence indicates early recovery."
    )

    assert (
        assessment.stage
        == RecoveryStage.EARLY_RECOVERY
    )

    assert (
        assessment.direction
        == RecoveryDirection.POSITIVE
    )

    assert assessment.bottoming_detected
    assert assessment.stabilization_detected
    assert assessment.inflection_detected

    print(
        "Passive Model Behavior          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY ASSESSMENT MODEL : PASS"
    )


if __name__ == "__main__":
    main()