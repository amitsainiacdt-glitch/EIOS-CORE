"""
EIOS
Everest Investment Operating System

Recovery Evidence Model Test
"""

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
)

from modules.opportunity.recovery.recovery_evidence import (
    RecoveryEvidence,
)

from modules.opportunity.signals.signal_model import (
    SignalDomain,
)


def main() -> None:

    # ======================================================
    # TYPE INTEGRITY
    # ======================================================

    assessment = RecoveryAssessment()

    evidence = RecoveryEvidence(
        signal_id="SIG-001",
        recovery_assessment=assessment,
        source_key="SOURCE-001",
        domain=SignalDomain.COMPANY,
    )

    assert isinstance(
        evidence,
        RecoveryEvidence,
    )

    print(
        "Evidence Type                  : PASS"
    )

    # ======================================================
    # SIGNAL ID
    # ======================================================

    assert (
        evidence.signal_id
        == "SIG-001"
    )

    print(
        "Signal Identity                : PASS"
    )

    # ======================================================
    # ASSESSMENT TYPE
    # ======================================================

    assert isinstance(
        evidence.recovery_assessment,
        RecoveryAssessment,
    )

    print(
        "Recovery Assessment            : PASS"
    )

    # ======================================================
    # SOURCE IDENTITY
    # ======================================================

    assert (
        evidence.source_key
        == "SOURCE-001"
    )

    print(
        "Source Identity                : PASS"
    )

    # ======================================================
    # DOMAIN
    # ======================================================

    assert (
        evidence.domain
        == SignalDomain.COMPANY
    )

    print(
        "Domain Integrity               : PASS"
    )

    # ======================================================
    # DEFAULT CONSTRUCTION
    # ======================================================

    empty = RecoveryEvidence()

    assert (
        empty.signal_id
        == ""
    )

    assert (
        empty.source_key
        == ""
    )

    assert (
        empty.domain
        == SignalDomain.COMPANY
    )

    print(
        "Default Construction           : PASS"
    )

    # ======================================================
    # PASSIVE MODEL
    # ======================================================

    evidence.recovery_assessment.stage = (
        evidence.recovery_assessment.stage
    )

    evidence.signal_id = "SIG-002"
    evidence.source_key = "SOURCE-002"
    evidence.domain = SignalDomain.SECTOR

    assert (
        evidence.signal_id
        == "SIG-002"
    )

    assert (
        evidence.source_key
        == "SOURCE-002"
    )

    assert (
        evidence.domain
        == SignalDomain.SECTOR
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
        "EIOS RECOVERY EVIDENCE MODEL : PASS"
    )


if __name__ == "__main__":
    main()