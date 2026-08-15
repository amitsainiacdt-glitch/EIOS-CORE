"""
EIOS
Recovery Opportunity Signal Model Tests
"""

from modules.opportunity.recovery.recovery_opportunity_signal import (
    RecoveryOpportunitySignal,
    RecoveryOpportunityStage,
    RecoveryOpportunityDirection,
    RecoveryOpportunityConfidence,
    RecoveryOpportunitySignalType,
)


def main():

    signal = RecoveryOpportunitySignal()

    # ======================================================
    # MODEL
    # ======================================================

    assert isinstance(
        signal,
        RecoveryOpportunitySignal,
    )

    print(
        "Signal Type                    : PASS"
    )

    # ======================================================
    # DEFAULT ENUMS
    # ======================================================

    assert (
        signal.stage
        == RecoveryOpportunityStage.UNKNOWN
    )

    assert (
        signal.direction
        == RecoveryOpportunityDirection.UNKNOWN
    )

    assert (
        signal.confidence_level
        == RecoveryOpportunityConfidence.UNKNOWN
    )

    assert (
        signal.signal_type
        == RecoveryOpportunitySignalType.UNKNOWN
    )

    print(
        "Default Enum Integrity         : PASS"
    )

    # ======================================================
    # DEFAULT NUMERICS
    # ======================================================

    assert signal.recovery_breadth == 0.0

    assert (
        signal.confirmed_recovery_breadth
        == 0.0
    )

    assert signal.recovery_confidence == 0.0

    assert signal.recovery_coherence == 0.0

    assert signal.temporal_support == 0.0

    assert signal.persistence_score == 0.0

    assert signal.contradiction_score == 0.0

    assert signal.catalyst_count == 0

    assert signal.supporting_catalyst_count == 0

    assert signal.confirming_catalyst_count == 0

    assert signal.accelerating_catalyst_count == 0

    assert signal.catalyst_confidence == 0.0

    assert signal.catalyst_strength == 0.0

    assert signal.catalyst_coherence == 0.0

    print(
        "Numeric Defaults               : PASS"
    )

    # ======================================================
    # DEFAULT BOOLEAN STATE
    # ======================================================

    assert signal.opportunity_ready is False

    assert (
        signal.requires_more_evidence
        is True
    )

    assert signal.catalyst_supported is False

    assert (
        signal.broad_recovery_supported
        is False
    )

    assert (
        signal.confirmed_recovery_supported
        is False
    )

    print(
        "Default Boolean State           : PASS"
    )

    # ======================================================
    # LIST INTEGRITY
    # ======================================================

    assert signal.supporting_evidence == []

    assert signal.contradictory_evidence == []

    assert signal.catalyst_families == []

    assert signal.catalyst_patterns == []

    assert signal.evidence_sources == []

    assert signal.reasons == []

    assert signal.warnings == []

    print(
        "List Field Integrity            : PASS"
    )

    # ======================================================
    # PASSIVE MODEL BEHAVIOR
    # ======================================================

    signal.signal_id = "REC-OPP-001"

    signal.theme_id = "THEME-001"

    signal.theme_name = (
        "Industrial Capital Recovery"
    )

    signal.signal_type = (
        RecoveryOpportunitySignalType.RECOVERY_CATALYST
    )

    signal.stage = (
        RecoveryOpportunityStage.ACTIONABLE
    )

    signal.direction = (
        RecoveryOpportunityDirection.POSITIVE
    )

    signal.confidence_level = (
        RecoveryOpportunityConfidence.HIGH
    )

    signal.recovery_breadth = 80.0

    signal.confirmed_recovery_breadth = 60.0

    signal.catalyst_count = 3

    signal.catalyst_supported = True

    signal.opportunity_ready = True

    assert signal.signal_id == "REC-OPP-001"

    assert signal.theme_id == "THEME-001"

    assert (
        signal.signal_type
        == RecoveryOpportunitySignalType.RECOVERY_CATALYST
    )

    assert (
        signal.stage
        == RecoveryOpportunityStage.ACTIONABLE
    )

    assert (
        signal.direction
        == RecoveryOpportunityDirection.POSITIVE
    )

    assert (
        signal.confidence_level
        == RecoveryOpportunityConfidence.HIGH
    )

    assert signal.recovery_breadth == 80.0

    assert (
        signal.confirmed_recovery_breadth
        == 60.0
    )

    assert signal.catalyst_count == 3

    assert signal.catalyst_supported is True

    assert signal.opportunity_ready is True

    print(
        "Passive Model Behavior          : PASS"
    )

    # ======================================================
    # PASSIVE NUMERIC BEHAVIOR
    # ======================================================

    signal.recovery_breadth = 91.0

    signal.catalyst_strength = 87.0

    signal.catalyst_confidence = 83.0

    assert signal.recovery_breadth == 91.0

    assert signal.catalyst_strength == 87.0

    assert signal.catalyst_confidence == 83.0

    print(
        "Passive Numeric Behavior        : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY OPPORTUNITY "
        "SIGNAL MODEL : PASS"
    )


if __name__ == "__main__":
    main()