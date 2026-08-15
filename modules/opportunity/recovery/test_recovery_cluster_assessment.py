"""
EIOS
Everest Investment Operating System

Recovery Cluster / Theme Assessment Model Test
"""

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
    RecoveryClusterDirection,
    RecoveryClusterStage,
    RecoveryClusterType,
)


def main() -> None:

    assessment = (
        RecoveryClusterAssessment()
    )

    # ======================================================
    # TYPE
    # ======================================================

    assert isinstance(
        assessment,
        RecoveryClusterAssessment,
    )

    print(
        "Assessment Type                : PASS"
    )

    # ======================================================
    # DEFAULT CLUSTER TYPE
    # ======================================================

    assert (
        assessment.cluster_type
        == RecoveryClusterType.UNKNOWN
    )

    print(
        "Default Cluster Type           : PASS"
    )

    # ======================================================
    # DEFAULT STAGE
    # ======================================================

    assert (
        assessment.stage
        == RecoveryClusterStage.INSUFFICIENT_EVIDENCE
    )

    print(
        "Default Stage                  : PASS"
    )

    # ======================================================
    # DEFAULT DIRECTION
    # ======================================================

    assert (
        assessment.direction
        == RecoveryClusterDirection.UNKNOWN
    )

    print(
        "Default Direction              : PASS"
    )

    # ======================================================
    # ENUM INTEGRITY
    # ======================================================

    assert len(
        RecoveryClusterType
    ) == 8

    assert len(
        RecoveryClusterStage
    ) == 5

    assert len(
        RecoveryClusterDirection
    ) == 5

    print(
        "Enum Integrity                 : PASS"
    )

    # ======================================================
    # DEFAULT COUNTS
    # ======================================================

    assert (
        assessment.total_recovery_assessments
        == 0
    )

    assert (
        assessment.supporting_assessments
        == 0
    )

    assert (
        assessment.stabilizing_assessments
        == 0
    )

    assert (
        assessment.deteriorating_assessments
        == 0
    )

    assert (
        assessment.contradictory_assessments
        == 0
    )

    assert (
        assessment.independent_sources
        == 0
    )

    assert (
        assessment.independent_domains
        == 0
    )

    assert (
        assessment.independent_signals
        == 0
    )

    print(
        "Default Counts                 : PASS"
    )

    # ======================================================
    # DEFAULT SCORES
    # ======================================================

    assert (
        assessment.stabilization_breadth
        == 0.0
    )

    assert (
        assessment.inflection_breadth
        == 0.0
    )

    assert (
        assessment.reversal_breadth
        == 0.0
    )

    assert (
        assessment.persistence_breadth
        == 0.0
    )

    assert (
        assessment.coherence_score
        == 0.0
    )

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
        assessment.contradiction_score
        == 0.0
    )

    assert (
        assessment.confidence
        == 0.0
    )

    print(
        "Default Scores                 : PASS"
    )

    # ======================================================
    # BOOLEAN FIELDS
    # ======================================================

    assert (
        assessment.emerging_cluster
        is False
    )

    assert (
        assessment.stabilizing_cluster
        is False
    )

    assert (
        assessment.early_recovery_cluster
        is False
    )

    assert (
        assessment.confirmed_recovery_cluster
        is False
    )

    assert (
        assessment.broad_based
        is False
    )

    assert (
        assessment.cross_domain_confirmation
        is False
    )

    print(
        "Boolean Field Integrity        : PASS"
    )

    # ======================================================
    # LIST FIELDS
    # ======================================================

    assert isinstance(
        assessment.supporting_signal_ids,
        list,
    )

    assert isinstance(
        assessment.contradictory_signal_ids,
        list,
    )

    assert isinstance(
        assessment.source_keys,
        list,
    )

    assert isinstance(
        assessment.domains,
        list,
    )

    assert isinstance(
        assessment.reasons,
        list,
    )

    assert isinstance(
        assessment.warnings,
        list,
    )

    print(
        "List Field Integrity            : PASS"
    )

    # ======================================================
    # PASSIVE MODEL BEHAVIOR
    # ======================================================

    assessment.cluster_id = (
        "RECOVERY-CLUSTER-001"
    )

    assessment.cluster_name = (
        "Industrial Recovery"
    )

    assessment.cluster_type = (
        RecoveryClusterType.SECTOR
    )

    assessment.stage = (
        RecoveryClusterStage.EARLY_RECOVERY_CLUSTER
    )

    assessment.direction = (
        RecoveryClusterDirection.POSITIVE
    )

    assessment.total_recovery_assessments = 8

    assessment.supporting_assessments = 6

    assessment.stabilizing_assessments = 2

    assessment.independent_sources = 6

    assessment.independent_domains = 4

    assessment.independent_signals = 8

    assessment.breadth_score = 78.0

    assessment.coherence_score = 82.0

    assessment.corroboration_score = 80.0

    assessment.temporal_score = 76.0

    assessment.confidence = 79.0

    assessment.broad_based = True

    assessment.cross_domain_confirmation = True

    assessment.early_recovery_cluster = True

    assessment.supporting_signal_ids.extend(
        [
            "SIG-001",
            "SIG-002",
            "SIG-003",
        ]
    )

    assessment.source_keys.extend(
        [
            "SRC-001",
            "SRC-002",
        ]
    )

    assessment.reasons.append(
        "Multiple independent recovery signals "
        "form a coherent sector-level pattern."
    )

    assert (
        assessment.cluster_type
        == RecoveryClusterType.SECTOR
    )

    assert (
        assessment.stage
        == RecoveryClusterStage.EARLY_RECOVERY_CLUSTER
    )

    assert (
        assessment.direction
        == RecoveryClusterDirection.POSITIVE
    )

    assert (
        assessment.total_recovery_assessments
        == 8
    )

    assert (
        assessment.independent_sources
        == 6
    )

    assert (
        assessment.broad_based
        is True
    )

    assert (
        assessment.cross_domain_confirmation
        is True
    )

    assert (
        len(
            assessment.supporting_signal_ids
        )
        == 3
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
        "EIOS RECOVERY CLUSTER / THEME "
        "ASSESSMENT MODEL : PASS"
    )


if __name__ == "__main__":
    main()