"""
EIOS
Everest Investment Operating System

Recovery Theme Engine Tests

Purpose:
Validate deterministic aggregation of Recovery Cluster
Assessments into Recovery Theme Assessments.

Tests:
- Engine existence
- Empty input
- Single cluster
- Emerging theme
- Developing theme
- Broad theme
- Validated theme
- Structural theme
- Reversal
- Recovery breadth
- Confirmed breadth
- Direction
- Confidence
- Confidence range
- Contradictory evidence
- Input immutability
- Deterministic assessment
- Transparent reasoning
"""


from copy import deepcopy

from modules.opportunity.recovery.recovery_theme_engine import (
    RecoveryThemeEngine,
)

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
)


# ==========================================================
# TEST DATA FACTORY
# ==========================================================


def make_cluster(
    cluster_id,
    supporting=1,
    confirmed=False,
    stabilizing=0,
    deteriorating=0,
    temporal=70.0,
    persistence=60.0,
    inflection=50.0,
    reversal=20.0,
    contradiction=0.0,
    coherence=70.0,
    sources=2,
    signals=2,
):

    assessment = RecoveryClusterAssessment()

    assessment.cluster_id = cluster_id

    assessment.cluster_name = (
        f"Cluster {cluster_id}"
    )

    assessment.supporting_assessments = (
        supporting
    )

    assessment.confirmed_recovery_cluster = (
        confirmed
    )

    assessment.stabilizing_assessments = (
        stabilizing
    )

    assessment.deteriorating_assessments = (
        deteriorating
    )

    assessment.temporal_score = temporal

    assessment.persistence_breadth = (
        persistence
    )

    assessment.inflection_breadth = (
        inflection
    )

    assessment.reversal_breadth = (
        reversal
    )

    assessment.contradiction_score = (
        contradiction
    )

    assessment.coherence_score = (
        coherence
    )

    assessment.corroboration_score = (
        70.0
    )

    assessment.independent_sources = (
        sources
    )

    assessment.independent_signals = (
        signals
    )

    return assessment


# ==========================================================
# MAIN
# ==========================================================


def main():

    engine = RecoveryThemeEngine()

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

    assert (
        result.cluster_count
        == 0
    )

    print(
        "Empty Input                     : PASS"
    )

    # ======================================================
    # SINGLE CLUSTER
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            confirmed=False,
        )
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.cluster_count
        == 1
    )

    assert (
        result.recovering_cluster_count
        == 1
    )

    assert (
        result.recovery_breadth
        == 100.0
    )

    assert (
        result.stage.value
        == "Emerging Theme"
    )

    print(
        "Single Cluster                : PASS"
    )

    # ======================================================
    # EMERGING THEME
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            temporal=50.0,
            coherence=40.0,
        ),
        make_cluster(
            "B",
            supporting=0,
            stabilizing=1,
            temporal=40.0,
            coherence=40.0,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.cluster_count
        == 2
    )

    assert (
        result.recovery_breadth
        == 50.0
    )

    assert (
        result.stage.value
        == "Developing Theme"
    )

    print(
        "Developing Theme              : PASS"
    )

    # ======================================================
    # BROAD THEME
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            coherence=60.0,
        ),
        make_cluster(
            "B",
            supporting=1,
            coherence=60.0,
        ),
        make_cluster(
            "C",
            supporting=1,
            coherence=60.0,
        ),
        make_cluster(
            "D",
            supporting=0,
            stabilizing=1,
            coherence=60.0,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.cluster_count
        == 4
    )

    assert (
        result.recovery_breadth
        == 75.0
    )

    assert (
        result.stage.value
        == "Broad Recovery Theme"
    )

    print(
        "Broad Theme                   : PASS"
    )

    # ======================================================
    # VALIDATED THEME
    # ======================================================

    assessments = [
        make_cluster(
            "A",
            supporting=1,
            confirmed=True,
            coherence=75.0,
        ),
        make_cluster(
            "B",
            supporting=1,
            confirmed=True,
            coherence=75.0,
        ),
        make_cluster(
            "C",
            supporting=1,
            confirmed=True,
            coherence=75.0,
        ),
        make_cluster(
            "D",
            supporting=1,
            confirmed=True,
            coherence=75.0,
        ),
        make_cluster(
            "E",
            supporting=0,
            stabilizing=1,
            coherence=75.0,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.cluster_count
        == 5
    )

    assert (
        result.recovery_breadth
        >= 70.0
    )

    assert (
        result.confirmed_recovery_breadth
        >= 40.0
    )

    assert (
        result.stage.value
        == "Validated Theme"
    )

    print(
        "Validated Theme               : PASS"
    )

    # ======================================================
    # STRUCTURAL THEME
    # ======================================================

    assessments = [
        make_cluster(
            f"STRUCT-{i}",
            supporting=1,
            confirmed=True,
            coherence=85.0,
            temporal=80.0,
            persistence=80.0,
        )
        for i in range(6)
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.cluster_count
        == 6
    )

    assert (
        result.recovery_breadth
        == 100.0
    )

    assert (
        result.confirmed_recovery_breadth
        == 100.0
    )

    assert (
        result.stage.value
        == "Structural Recovery Theme"
    )

    print(
        "Structural Theme              : PASS"
    )

    # ======================================================
    # REVERSAL
    # ======================================================

    assessments = [
        make_cluster(
            "R1",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "R2",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "R3",
            supporting=0,
            deteriorating=1,
        ),
        make_cluster(
            "R4",
            supporting=0,
            deteriorating=1,
        ),
        make_cluster(
            "R5",
            supporting=0,
            deteriorating=1,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.deteriorating_cluster_count
        > result.recovering_cluster_count
    )

    assert (
        result.stage.value
        == "Reversing Theme"
    )

    assert (
        result.direction.value
        == "Negative"
    )

    print(
        "Reversal Theme                : PASS"
    )

    # ======================================================
    # RECOVERY BREADTH
    # ======================================================

    assessments = [
        make_cluster(
            "B1",
            supporting=1,
        ),
        make_cluster(
            "B2",
            supporting=1,
        ),
        make_cluster(
            "B3",
            supporting=1,
        ),
        make_cluster(
            "B4",
            supporting=0,
            stabilizing=1,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.recovery_breadth
        == 75.0
    )

    assert (
        0.0
        <= result.recovery_breadth
        <= 100.0
    )

    print(
        "Recovery Breadth              : PASS"
    )

    # ======================================================
    # CONFIRMED BREADTH
    # ======================================================

    assessments = [
        make_cluster(
            "C1",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "C2",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "C3",
            supporting=1,
            confirmed=False,
        ),
        make_cluster(
            "C4",
            supporting=0,
            stabilizing=1,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.confirmed_recovery_breadth
        == 50.0
    )

    print(
        "Confirmed Breadth             : PASS"
    )

    # ======================================================
    # POSITIVE DIRECTION
    # ======================================================

    assessments = [
        make_cluster(
            f"P-{i}",
            supporting=1,
            confirmed=True,
        )
        for i in range(4)
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.direction.value
        == "Positive"
    )

    print(
        "Positive Direction            : PASS"
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
        "Confidence Range              : PASS"
    )

    # ======================================================
    # CONTRADICTORY EVIDENCE
    # ======================================================

    assessments = [
        make_cluster(
            "X1",
            supporting=1,
            confirmed=True,
            contradiction=70.0,
        ),
        make_cluster(
            "X2",
            supporting=1,
            contradiction=60.0,
        ),
        make_cluster(
            "X3",
            supporting=0,
            stabilizing=1,
            contradiction=50.0,
        ),
    ]

    result = engine.assess(
        assessments
    )

    assert (
        result.contradiction_score
        > 0.0
    )

    assert (
        len(result.warnings)
        > 0
    )

    print(
        "Contradictory Evidence         : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    assessments = [
        make_cluster(
            "IMM-1",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "IMM-2",
            supporting=1,
        ),
    ]

    original = deepcopy(
        assessments
    )

    engine.assess(
        assessments
    )

    assert (
        assessments
        == original
    )

    print(
        "Input Immutability             : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    assessments = [
        make_cluster(
            "DET-1",
            supporting=1,
            confirmed=True,
        ),
        make_cluster(
            "DET-2",
            supporting=1,
        ),
        make_cluster(
            "DET-3",
            supporting=1,
        ),
    ]

    first = engine.assess(
        assessments
    )

    second = engine.assess(
        assessments
    )

    assert (
        first.cluster_count
        == second.cluster_count
    )

    assert (
        first.recovery_breadth
        == second.recovery_breadth
    )

    assert (
        first.confirmed_recovery_breadth
        == second.confirmed_recovery_breadth
    )

    assert (
        first.stage
        == second.stage
    )

    assert (
        first.direction
        == second.direction
    )

    assert (
        first.confidence
        == second.confidence
    )

    assert (
        first.reasons
        == second.reasons
    )

    print(
        "Deterministic Assessment       : PASS"
    )

    # ======================================================
    # TRANSPARENT REASONING
    # ======================================================

    assert (
        len(first.reasons)
        > 0
    )

    assert all(
        isinstance(
            reason,
            str,
        )
        for reason in first.reasons
    )

    print(
        "Transparent Reasoning          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY THEME "
        "ENGINE : PASS"
    )


if __name__ == "__main__":
    main()