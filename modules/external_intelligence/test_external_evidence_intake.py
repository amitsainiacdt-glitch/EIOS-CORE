"""
EIOS
Everest Investment Operating System

External Evidence Intake Test
=============================

Validates the controlled boundary between an external
Observation and the canonical EvidenceItem.
"""

from datetime import datetime

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_intake import (
    ExternalEvidenceIntake,
)

from modules.observation.observation import (
    Observation,
)


def make_observation():

    return Observation(
        title="Industrial capacity expansion",
        description=(
            "The company announced expansion "
            "of manufacturing capacity."
        ),
        source="Synthetic External Source",
        category="External Web",
        entity="The Anup Engineering Limited",
        confidence=80.0,
        timestamp=datetime.now(),
    )


def main():

    print("=" * 60)
    print("EIOS EXTERNAL EVIDENCE INTAKE TEST")
    print("=" * 60)

    # ======================================================
    # SETUP
    # ======================================================

    intake = ExternalEvidenceIntake()

    observation = make_observation()

    # ======================================================
    # TEST 1 — INTAKE CREATION
    # ======================================================

    assert intake is not None

    print(
        "Test 1 — Intake Creation             : PASS"
    )

    # ======================================================
    # TEST 2 — EXPLICIT ASSESSMENT
    # ======================================================

    assessment = EvidenceAssessment(
        category="Capacity Expansion",
        direction="Supporting",
        strength=85.0,
        confidence=90.0,
        independent_confirmation=1,
        is_primary_source=True,
        is_time_sensitive=True,
        notes=(
            "Explicitly assessed external information."
        ),
    )

    evidence = intake.assess(
        observation=observation,
        assessment=assessment,
        evidence_id="EXT-0001",
    )

    assert evidence is not None

    print(
        "Test 2 — Evidence Creation            : PASS"
    )

    # ======================================================
    # TEST 3 — IDENTITY PRESERVATION
    # ======================================================

    assert (
        evidence.statement
        == observation.description
    )

    assert (
        evidence.source
        == observation.source
    )

    assert (
        evidence.category
        == assessment.category
    )

    assert (
        evidence.direction
        == assessment.direction
    )

    print(
        "Test 3 — Identity Preservation         : PASS"
    )

    # ======================================================
    # TEST 4 — ASSESSMENT TRANSFER
    # ======================================================

    assert evidence.strength == 85.0

    assert evidence.confidence == 90.0

    assert (
        evidence.independent_confirmation
        == 1
    )

    assert (
        evidence.is_primary_source
        is True
    )

    assert (
        evidence.is_time_sensitive
        is True
    )

    assert (
        evidence.notes
        == assessment.notes
    )

    print(
        "Test 4 — Assessment Transfer           : PASS"
    )

    # ======================================================
    # TEST 5 — EVIDENCE ID
    # ======================================================

    assert (
        evidence.evidence_id
        == "EXT-0001"
    )

    print(
        "Test 5 — Evidence ID                   : PASS"
    )

    # ======================================================
    # TEST 6 — NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        evidence,
        "opportunity_score",
    )

    assert not hasattr(
        evidence,
        "valuation",
    )

    assert not hasattr(
        evidence,
        "catalyst_score",
    )

    print(
        "Test 6 — No Analytical Fabrication     : PASS"
    )

    # ======================================================
    # TEST 7 — INVALID STRENGTH
    # ======================================================

    invalid_strength = EvidenceAssessment(
        category="Test",
        strength=150.0,
        confidence=90.0,
    )

    try:

        intake.assess(
            observation=observation,
            assessment=invalid_strength,
        )

    except ValueError:

        pass

    else:

        raise AssertionError(
            "Invalid strength was accepted"
        )

    print(
        "Test 7 — Strength Validation            : PASS"
    )

    # ======================================================
    # TEST 8 — INVALID CONFIDENCE
    # ======================================================

    invalid_confidence = EvidenceAssessment(
        category="Test",
        strength=80.0,
        confidence=150.0,
    )

    try:

        intake.assess(
            observation=observation,
            assessment=invalid_confidence,
        )

    except ValueError:

        pass

    else:

        raise AssertionError(
            "Invalid confidence was accepted"
        )

    print(
        "Test 8 — Confidence Validation          : PASS"
    )

    # ======================================================
    # TEST 9 — MISSING ASSESSMENT
    # ======================================================

    try:

        intake.assess(
            observation=observation,
            assessment=None,
        )

    except ValueError:

        pass

    else:

        raise AssertionError(
            "Missing assessment was accepted"
        )

    print(
        "Test 9 — Missing Assessment Guard        : PASS"
    )

    # ======================================================
    # TEST 10 — MISSING OBSERVATION
    # ======================================================

    try:

        intake.assess(
            observation=None,
            assessment=assessment,
        )

    except ValueError:

        pass

    else:

        raise AssertionError(
            "Missing observation was accepted"
        )

    print(
        "Test 10 — Missing Observation Guard      : PASS"
    )

    # ======================================================
    # TEST 11 — MULTIPLE EVIDENCE
    # ======================================================

    second_observation = Observation(
        title="New export order",
        description=(
            "The company received a new export order."
        ),
        source="Synthetic External Source",
        category="External Web",
        entity="The Anup Engineering Limited",
        confidence=85.0,
        timestamp=observation.timestamp,
    )

    second_assessment = EvidenceAssessment(
        category="Order / Contract",
        direction="Supporting",
        strength=80.0,
        confidence=85.0,
        independent_confirmation=2,
    )

    evidence_items = intake.assess_many(
        observations=[
            observation,
            second_observation,
        ],
        assessments=[
            assessment,
            second_assessment,
        ],
    )

    assert len(evidence_items) == 2

    assert (
        evidence_items[0].evidence_id
        == "EXT-0001"
    )

    assert (
        evidence_items[1].evidence_id
        == "EXT-0002"
    )

    assert (
        evidence_items[0].statement
        == observation.description
    )

    assert (
        evidence_items[1].statement
        == second_observation.description
    )

    print(
        "Test 11 — Multiple Evidence Intake     : PASS"
    )

    # ======================================================
    # TEST 12 — COLLECTION LENGTH VALIDATION
    # ======================================================

    try:

        intake.assess_many(
            observations=[
                observation,
            ],
            assessments=[],
        )

    except ValueError:

        pass

    else:

        raise AssertionError(
            "Mismatched collections were accepted"
        )

    print(
        "Test 12 — Collection Validation         : PASS"
    )

    # ======================================================
    # TEST 13 — EMPTY COLLECTION
    # ======================================================

    empty_result = intake.assess_many(
        observations=[],
        assessments=[],
    )

    assert empty_result == []

    print(
        "Test 13 — Empty Collection             : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "EIOS EXTERNAL EVIDENCE INTAKE : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()