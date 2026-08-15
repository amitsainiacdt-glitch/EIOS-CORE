"""
EIOS
Everest Investment Operating System

Multi-Signal Recovery Assessment Model Test
"""

from modules.opportunity.recovery.multi_signal_recovery_assessment import (
    MultiSignalRecoveryAssessment,
    MultiSignalRecoveryDirection,
    MultiSignalRecoveryStage,
)


def main() -> None:

    # ======================================================
    # TYPE INTEGRITY
    # ======================================================

    assessment = (
        MultiSignalRecoveryAssessment()
    )

    assert isinstance(
        assessment,
        MultiSignalRecoveryAssessment,
    )

    print(
        "Assessment Type                : PASS"
    )

    # ======================================================
    # DEFAULT STAGE
    # ======================================================

    assert (
        assessment.stage
        == MultiSignalRecoveryStage.INSUFFICIENT_EVIDENCE
    )

    print(
        "Default Stage                  : PASS"
    )

    # ======================================================
    # DEFAULT DIRECTION
    # ======================================================

    assert (
        assessment.direction
        == MultiSignalRecoveryDirection.UNKNOWN
    )

    print(
        "Default Direction              : PASS"
    )

    # ======================================================
    # ENUM INTEGRITY
    # ======================================================

    assert (
        len(MultiSignalRecoveryStage)
        == 5
    )

    assert (
        len(MultiSignalRecoveryDirection)
        == 5
    )

    print(
        "Enum Integrity                 : PASS"
    )

    # ======================================================
    # DEFAULT COUNTS
    # ======================================================

    assert (
        assessment.total_signals
        == 0
    )

    assert (
        assessment.improving_signals
        == 0
    )

    assert (
        assessment.stabilizing_signals
        == 0
    )

    assert (
        assessment.deteriorating_signals
        == 0
    )

    assert (
        assessment.neutral_signals
        == 0
    )

    print(
        "Default Signal Counts          : PASS"
    )

    # ======================================================
    # DEFAULT SCORES
    # ======================================================

    assert (
        assessment.breadth_score
        == 0.0
    )

    assert (
        assessment.corroboration_score
        == 0.0
    )

    assert (
        assessment.temporal_score
        == 0.0
    )

    assert (
        assessment.consistency_score
        == 0.0
    )

    assert (
        assessment.contradiction_score
        == 0.0
    )

    assert (
        assessment.confidence
        == 0.0
    )

    print(
        "Default Scores                : PASS"
    )

    # ======================================================
    # RECOVERY BOOLEAN FIELDS
    # ======================================================

    assert (
        assessment.isolated_improvement
        is False
    )

    assert (
        assessment.broad_stabilization
        is False
    )

    assert (
        assessment.broad_inflection
        is False
    )

    assert (
        assessment.broad_reversal
        is False
    )

    assert (
        assessment.persistent_recovery
        is False
    )

    print(
        "Recovery Boolean Fields       : PASS"
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

    assert isinstance(
        assessment.supporting_signal_ids,
        list,
    )

    assert isinstance(
        assessment.contradictory_signal_ids,
        list,
    )

    print(
        "List Field Integrity           : PASS"
    )

    # ======================================================
    # PASSIVE MODEL BEHAVIOR
    # ======================================================

    assessment.stage = (
        MultiSignalRecoveryStage.EARLY_BROAD_RECOVERY
    )

    assessment.direction = (
        MultiSignalRecoveryDirection.POSITIVE
    )

    assessment.total_signals = 7

    assessment.improving_signals = 5

    assessment.stabilizing_signals = 2

    assessment.breadth_score = 82.0

    assessment.corroboration_score = 78.0

    assessment.temporal_score = 80.0

    assessment.consistency_score = 75.0

    assessment.confidence = 79.0

    assessment.broad_inflection = True

    assessment.persistent_recovery = True

    assessment.reasons.append(
        "Multiple independent signals support "
        "an early broad recovery."
    )

    assessment.supporting_signal_ids.extend(
        [
            "SIG-001",
            "SIG-002",
            "SIG-003",
        ]
    )

    assert (
        assessment.stage
        == MultiSignalRecoveryStage.EARLY_BROAD_RECOVERY
    )

    assert (
        assessment.direction
        == MultiSignalRecoveryDirection.POSITIVE
    )

    assert (
        assessment.total_signals
        == 7
    )

    assert (
        assessment.improving_signals
        == 5
    )

    assert (
        assessment.broad_inflection
        is True
    )

    assert (
        assessment.persistent_recovery
        is True
    )

    assert len(
        assessment.supporting_signal_ids
    ) == 3

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
        "EIOS MULTI-SIGNAL RECOVERY "
        "ASSESSMENT MODEL : PASS"
    )


if __name__ == "__main__":
    main()