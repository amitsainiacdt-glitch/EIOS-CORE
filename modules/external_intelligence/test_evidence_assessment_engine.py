"""
EIOS
Everest Investment Operating System

External Evidence Assessment Engine Test
"""

from datetime import datetime

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_assessment_engine import (
    EvidenceAssessmentEngine,
)

from modules.observation.observation import (
    Observation,
)

from modules.opportunity.evidence_engine import (
    EvidenceItem,
)


def make_observation() -> Observation:

    return Observation(
        title="Industrial Demand Increase",
        description=(
            "Industrial demand is increasing."
        ),
        source="Company Filing",
        category="Industry",
        entity="Test Company",
        confidence=85.0,
        timestamp=datetime.now(),
    )


def make_assessment() -> EvidenceAssessment:

    return EvidenceAssessment(
        category="Industry",
        direction="Supporting",
        strength=90.0,
        confidence=85.0,
        independent_confirmation=2,
        is_primary_source=True,
        is_time_sensitive=True,
        notes="Primary-source assessment.",
    )


def main() -> None:

    engine = EvidenceAssessmentEngine()

    observation = make_observation()
    assessment = make_assessment()

    # ======================================================
    # ENGINE
    # ======================================================

    assert engine is not None

    print(
        "Assessment Engine Exists       : PASS"
    )

    # ======================================================
    # EVIDENCE CREATION
    # ======================================================

    evidence = engine.assess(
        observation=observation,
        assessment=assessment,
        evidence_id="EXT-EVID-001",
    )

    assert isinstance(
        evidence,
        EvidenceItem,
    )

    print(
        "EvidenceItem Creation          : PASS"
    )

    # ======================================================
    # IDENTITY / CONTENT
    # ======================================================

    assert (
        evidence.evidence_id
        == "EXT-EVID-001"
    )

    assert (
        evidence.statement
        == observation.description
    )

    assert (
        evidence.source
        == observation.source
    )

    print(
        "Identity / Content Transfer    : PASS"
    )

    # ======================================================
    # ASSESSMENT TRANSFER
    # ======================================================

    assert (
        evidence.category
        == assessment.category
    )

    assert (
        evidence.direction
        == assessment.direction
    )

    assert (
        evidence.strength
        == assessment.strength
    )

    assert (
        evidence.confidence
        == assessment.confidence
    )

    assert (
        evidence.independent_confirmation
        == assessment.independent_confirmation
    )

    assert (
        evidence.is_primary_source
        == assessment.is_primary_source
    )

    assert (
        evidence.is_time_sensitive
        == assessment.is_time_sensitive
    )

    assert (
        evidence.notes
        == assessment.notes
    )

    print(
        "Assessment Transfer            : PASS"
    )

    # ======================================================
    # CATEGORY FALLBACK
    # ======================================================

    empty_category = EvidenceAssessment(
        category="",
        direction="Supporting",
        strength=70.0,
        confidence=70.0,
    )

    fallback_evidence = engine.assess(
        observation=observation,
        assessment=empty_category,
        evidence_id="EXT-EVID-002",
    )

    assert (
        fallback_evidence.category
        == observation.category
    )

    print(
        "Category Fallback              : PASS"
    )

    # ======================================================
    # RANGE PROTECTION
    # ======================================================

    try:

        engine.assess(
            observation=observation,
            assessment=EvidenceAssessment(
                strength=101.0,
                confidence=80.0,
            ),
        )

        raise AssertionError(
            "Invalid strength accepted"
        )

    except ValueError:

        pass

    print(
        "Strength Range Protection      : PASS"
    )

    try:

        engine.assess(
            observation=observation,
            assessment=EvidenceAssessment(
                strength=80.0,
                confidence=-1.0,
            ),
        )

        raise AssertionError(
            "Invalid confidence accepted"
        )

    except ValueError:

        pass

    print(
        "Confidence Range Protection    : PASS"
    )

    # ======================================================
    # CONFIRMATION PROTECTION
    # ======================================================

    try:

        engine.assess(
            observation=observation,
            assessment=EvidenceAssessment(
                strength=80.0,
                confidence=80.0,
                independent_confirmation=-1,
            ),
        )

        raise AssertionError(
            "Negative confirmation accepted"
        )

    except ValueError:

        pass

    print(
        "Confirmation Range Protection  : PASS"
    )

    # ======================================================
    # NULL PROTECTION
    # ======================================================

    try:

        engine.assess(
            observation=None,
            assessment=assessment,
        )

        raise AssertionError(
            "None observation accepted"
        )

    except ValueError:

        pass

    print(
        "Observation Protection          : PASS"
    )

    try:

        engine.assess(
            observation=observation,
            assessment=None,
        )

        raise AssertionError(
            "None assessment accepted"
        )

    except ValueError:

        pass

    print(
        "Assessment Protection           : PASS"
    )

    # ======================================================
    # NO ANALYTICAL CALCULATION
    # ======================================================

    assert not hasattr(
        evidence,
        "evidence_score",
    )

    assert not hasattr(
        evidence,
        "opportunity_score",
    )

    assert not hasattr(
        evidence,
        "valuation",
    )

    print(
        "No Analytical Fabrication       : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    assert (
        observation.description
        == "Industrial demand is increasing."
    )

    assert (
        assessment.strength
        == 90.0
    )

    assert (
        assessment.confidence
        == 85.0
    )

    print(
        "Input Immutability               : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL EVIDENCE "
        "ASSESSMENT ENGINE : PASS"
    )


if __name__ == "__main__":
    main()