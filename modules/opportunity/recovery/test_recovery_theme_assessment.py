"""
EIOS
Recovery Theme Assessment Model Tests
"""


from modules.opportunity.recovery.recovery_theme_assessment import (
    RecoveryThemeAssessment,
    RecoveryThemeType,
    RecoveryThemeStage,
    RecoveryThemeDirection,
    RecoveryThemeConfidence,
)


def main():

    # ======================================================
    # MODEL EXISTENCE
    # ======================================================

    assessment = RecoveryThemeAssessment()

    assert isinstance(
        assessment,
        RecoveryThemeAssessment,
    )

    print(
        "Assessment Type                : PASS"
    )

    # ======================================================
    # DEFAULT THEME TYPE
    # ======================================================

    assert (
        assessment.theme_type
        == RecoveryThemeType.UNKNOWN
    )

    print(
        "Default Theme Type             : PASS"
    )

    # ======================================================
    # DEFAULT STAGE
    # ======================================================

    assert (
        assessment.stage
        == RecoveryThemeStage.UNKNOWN
    )

    print(
        "Default Stage                  : PASS"
    )

    # ======================================================
    # DEFAULT DIRECTION
    # ======================================================

    assert (
        assessment.direction
        == RecoveryThemeDirection.UNKNOWN
    )

    print(
        "Default Direction              : PASS"
    )

    # ======================================================
    # DEFAULT CONFIDENCE
    # ======================================================

    assert (
        assessment.confidence_level
        == RecoveryThemeConfidence.UNKNOWN
    )

    print(
        "Default Confidence             : PASS"
    )

    # ======================================================
    # ENUM INTEGRITY
    # ======================================================

    assert (
        len(RecoveryThemeType)
        >= 10
    )

    assert (
        len(RecoveryThemeStage)
        >= 5
    )

    assert (
        len(RecoveryThemeDirection)
        == 5
    )

    assert (
        len(RecoveryThemeConfidence)
        == 5
    )

    print(
        "Enum Integrity                 : PASS"
    )

    # ======================================================
    # DEFAULT LISTS
    # ======================================================

    assert assessment.cluster_ids == []
    assert assessment.sectors == []
    assert assessment.industries == []
    assert assessment.countries == []
    assert assessment.regions == []
    assert assessment.supporting_evidence == []
    assert assessment.contradictory_evidence == []
    assert assessment.reasons == []
    assert assessment.warnings == []

    print(
        "List Field Integrity            : PASS"
    )

    # ======================================================
    # DEFAULT NUMERIC VALUES
    # ======================================================

    assert assessment.cluster_count == 0
    assert assessment.recovery_breadth == 0.0
    assert assessment.confirmed_recovery_breadth == 0.0
    assert assessment.coherence_score == 0.0
    assert assessment.confidence == 0.0
    assert assessment.contradiction_score == 0.0

    print(
        "Numeric Defaults               : PASS"
    )

    # ======================================================
    # PASSIVE MODEL
    # ======================================================

    assessment.theme_id = (
        "THEME-INDUSTRIAL-CAPEX"
    )

    assessment.theme_name = (
        "Industrial Capital Cycle Recovery"
    )

    assessment.theme_type = (
        RecoveryThemeType.CAPEX_CYCLE
    )

    assessment.cluster_ids.append(
        "CLUSTER-001"
    )

    assessment.sectors.append(
        "Industrials"
    )

    assessment.cluster_count = 1

    assert (
        assessment.theme_id
        == "THEME-INDUSTRIAL-CAPEX"
    )

    assert (
        assessment.theme_name
        == "Industrial Capital Cycle Recovery"
    )

    assert (
        assessment.theme_type
        == RecoveryThemeType.CAPEX_CYCLE
    )

    assert (
        assessment.cluster_ids
        == ["CLUSTER-001"]
    )

    assert (
        assessment.sectors
        == ["Industrials"]
    )

    assert (
        assessment.cluster_count
        == 1
    )

    print(
        "Passive Model Behavior          : PASS"
    )

    # ======================================================
    # NO CALCULATION
    # ======================================================

    assessment.recovery_breadth = 73.0

    assessment.coherence_score = 82.0

    assessment.confidence = 91.0

    assert (
        assessment.recovery_breadth
        == 73.0
    )

    assert (
        assessment.coherence_score
        == 82.0
    )

    assert (
        assessment.confidence
        == 91.0
    )

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
        "EIOS RECOVERY THEME "
        "ASSESSMENT MODEL : PASS"
    )


if __name__ == "__main__":
    main()