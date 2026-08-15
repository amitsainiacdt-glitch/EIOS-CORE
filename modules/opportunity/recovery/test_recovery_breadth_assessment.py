"""
EIOS
Everest Investment Operating System

Recovery Breadth Assessment Model Test
"""

from modules.opportunity.recovery.recovery_breadth_assessment import (
    RecoveryBreadthAssessment,
    RecoveryBreadthType,
    RecoveryBreadthStage,
    RecoveryBreadthDirection,
    RecoveryLeadershipState,
)


def main() -> None:

    # ======================================================
    # ASSESSMENT TYPE
    # ======================================================

    assessment = (
        RecoveryBreadthAssessment()
    )

    assert isinstance(
        assessment,
        RecoveryBreadthAssessment,
    )

    print(
        "Assessment Type                : PASS"
    )

    # ======================================================
    # DEFAULT BREADTH TYPE
    # ======================================================

    assert (
        assessment.breadth_type
        == RecoveryBreadthType.UNKNOWN
    )

    print(
        "Default Breadth Type           : PASS"
    )

    # ======================================================
    # DEFAULT STAGE
    # ======================================================

    assert (
        assessment.stage
        == RecoveryBreadthStage.INSUFFICIENT
    )

    print(
        "Default Stage                  : PASS"
    )

    # ======================================================
    # DEFAULT DIRECTION
    # ======================================================

    assert (
        assessment.direction
        == RecoveryBreadthDirection.UNKNOWN
    )

    print(
        "Default Direction              : PASS"
    )

    # ======================================================
    # DEFAULT LEADERSHIP
    # ======================================================

    assert (
        assessment.leadership_state
        == RecoveryLeadershipState.UNKNOWN
    )

    print(
        "Default Leadership             : PASS"
    )

    # ======================================================
    # ENUM INTEGRITY
    # ======================================================

    assert len(
        RecoveryBreadthType
    ) >= 1

    assert len(
        RecoveryBreadthStage
    ) >= 1

    assert len(
        RecoveryBreadthDirection
    ) >= 1

    assert len(
        RecoveryLeadershipState
    ) >= 1

    print(
        "Enum Integrity                 : PASS"
    )

    # ======================================================
    # NUMERIC DEFAULTS
    # ======================================================

    numeric_fields = [
        assessment.total_entities,
        assessment.assessed_entities,
        assessment.improving_entities,
        assessment.stabilizing_entities,
        assessment.deteriorating_entities,
        assessment.unchanged_entities,
        assessment.insufficient_entities,
        assessment.early_inflection_entities,
        assessment.early_recovery_entities,
        assessment.confirmed_recovery_entities,
        assessment.improvement_breadth,
        assessment.stabilization_breadth,
        assessment.recovery_breadth,
        assessment.confirmed_recovery_breadth,
        assessment.deterioration_breadth,
        assessment.contradiction_breadth,
        assessment.previous_breadth,
        assessment.current_breadth,
        assessment.breadth_change,
        assessment.breadth_acceleration,
        assessment.leader_count,
        assessment.leader_breadth,
        assessment.independent_sources,
        assessment.independent_signals,
        assessment.independent_domains,
        assessment.temporal_support,
        assessment.corroboration_score,
        assessment.contradiction_score,
        assessment.confidence,
    ]

    assert all(
        value == 0
        for value in numeric_fields
    )

    print(
        "Numeric Defaults               : PASS"
    )

    # ======================================================
    # BOOLEAN DEFAULTS
    # ======================================================

    boolean_fields = [
        assessment.breadth_expanding,
        assessment.breadth_stable,
        assessment.breadth_contracting,
        assessment.broad_based,
        assessment.early_breadth_signal,
        assessment.recovery_breadth_signal,
        assessment.confirmed_breadth_signal,
    ]

    assert all(
        value is False
        for value in boolean_fields
    )

    print(
        "Boolean Defaults               : PASS"
    )

    # ======================================================
    # LIST DEFAULTS
    # ======================================================

    assert (
        assessment.leading_entities
        == []
    )

    assert (
        assessment.lagging_entities
        == []
    )

    assert (
        assessment.reasons
        == []
    )

    assert (
        assessment.warnings
        == []
    )

    print(
        "List Field Integrity            : PASS"
    )

    # ======================================================
    # PASSIVE MODEL BEHAVIOR
    # ======================================================

    assessment.breadth_id = (
        "AUTO-SECTOR-2026"
    )

    assessment.breadth_name = (
        "Indian Auto Sector"
    )

    assessment.breadth_type = (
        RecoveryBreadthType.SECTOR
    )

    assessment.stage = (
        RecoveryBreadthStage.EARLY_BREADTH
    )

    assessment.direction = (
        RecoveryBreadthDirection.EXPANDING
    )

    assessment.leadership_state = (
        RecoveryLeadershipState.EARLY_LEADERS
    )

    assessment.total_entities = 20

    assessment.assessed_entities = 15

    assessment.improving_entities = 7

    assessment.stabilizing_entities = 5

    assessment.deteriorating_entities = 2

    assessment.unchanged_entities = 1

    assessment.early_recovery_entities = 4

    assessment.recovery_breadth = 46.67

    assessment.breadth_expanding = True

    assessment.broad_based = True

    assessment.leading_entities = [
        "COMPANY-A",
        "COMPANY-B",
    ]

    assessment.reasons.append(
        "Recovery breadth is expanding."
    )

    assert (
        assessment.breadth_id
        == "AUTO-SECTOR-2026"
    )

    assert (
        assessment.breadth_name
        == "Indian Auto Sector"
    )

    assert (
        assessment.breadth_type
        == RecoveryBreadthType.SECTOR
    )

    assert (
        assessment.stage
        == RecoveryBreadthStage.EARLY_BREADTH
    )

    assert (
        assessment.direction
        == RecoveryBreadthDirection.EXPANDING
    )

    assert (
        assessment.leadership_state
        == RecoveryLeadershipState.EARLY_LEADERS
    )

    assert (
        assessment.total_entities
        == 20
    )

    assert (
        assessment.recovery_breadth
        == 46.67
    )

    assert (
        assessment.breadth_expanding
        is True
    )

    assert (
        assessment.broad_based
        is True
    )

    assert (
        assessment.leading_entities
        == [
            "COMPANY-A",
            "COMPANY-B",
        ]
    )

    assert (
        assessment.reasons
        == [
            "Recovery breadth is expanding."
        ]
    )

    print(
        "Passive Model Behavior         : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY BREADTH "
        "ASSESSMENT MODEL : PASS"
    )


if __name__ == "__main__":
    main()