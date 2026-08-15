"""
EIOS
Everest Investment Operating System

Recovery Cluster Evidence Model Test
"""

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
)

from modules.opportunity.recovery.recovery_evidence import (
    RecoveryEvidence,
)

from modules.opportunity.recovery.recovery_cluster_evidence import (
    RecoveryClusterEvidence,
)

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterType,
)


def main() -> None:

    assessment = RecoveryAssessment()

    recovery_evidence = RecoveryEvidence(
        signal_id="SIG-001",
        recovery_assessment=assessment,
        source_key="SRC-001",
    )

    cluster_evidence = (
        RecoveryClusterEvidence(
            cluster_key="AUTO-INDIA",
            cluster_name="Indian Auto Industry",
            cluster_type=(
                RecoveryClusterType.INDUSTRY
            ),
            recovery_evidence=recovery_evidence,
        )
    )

    # ======================================================
    # TYPE
    # ======================================================

    assert isinstance(
        cluster_evidence,
        RecoveryClusterEvidence,
    )

    print(
        "Cluster Evidence Type          : PASS"
    )

    # ======================================================
    # CLUSTER IDENTITY
    # ======================================================

    assert (
        cluster_evidence.cluster_key
        == "AUTO-INDIA"
    )

    assert (
        cluster_evidence.cluster_name
        == "Indian Auto Industry"
    )

    print(
        "Cluster Identity               : PASS"
    )

    # ======================================================
    # CLUSTER TYPE
    # ======================================================

    assert (
        cluster_evidence.cluster_type
        == RecoveryClusterType.INDUSTRY
    )

    print(
        "Cluster Type                   : PASS"
    )

    # ======================================================
    # RECOVERY EVIDENCE
    # ======================================================

    assert isinstance(
        cluster_evidence.recovery_evidence,
        RecoveryEvidence,
    )

    assert (
        cluster_evidence
        .recovery_evidence
        .signal_id
        == "SIG-001"
    )

    print(
        "Recovery Evidence Integrity    : PASS"
    )

    # ======================================================
    # DEFAULT CONSTRUCTION
    # ======================================================

    empty = RecoveryClusterEvidence()

    assert (
        empty.cluster_key
        == ""
    )

    assert (
        empty.cluster_name
        == ""
    )

    assert (
        empty.cluster_type
        == RecoveryClusterType.UNKNOWN
    )

    assert (
        empty.recovery_evidence
        is None
    )

    print(
        "Default Construction           : PASS"
    )

    # ======================================================
    # PASSIVE MODEL
    # ======================================================

    cluster_evidence.cluster_key = (
        "INDUSTRIAL-CAPEX"
    )

    cluster_evidence.cluster_name = (
        "Industrial Capital Cycle"
    )

    assert (
        cluster_evidence.cluster_key
        == "INDUSTRIAL-CAPEX"
    )

    assert (
        cluster_evidence.cluster_name
        == "Industrial Capital Cycle"
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
        "EIOS RECOVERY CLUSTER "
        "EVIDENCE MODEL : PASS"
    )


if __name__ == "__main__":
    main()