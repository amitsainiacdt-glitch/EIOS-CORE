"""
EIOS
Everest Investment Operating System

External Source Assessment Engine Test
=======================================
"""

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)

from modules.external_intelligence.external_source_assessment_engine import (
    ExternalSourceAssessmentEngine,
)


def main() -> None:

    engine = ExternalSourceAssessmentEngine()

    # ======================================================
    # ENGINE
    # ======================================================

    assert engine is not None

    print(
        "Assessment Engine Exists       : PASS"
    )

    # ======================================================
    # ASSESSMENT CREATION
    # ======================================================

    assessment = engine.assess(
        source_url="https://example.com/article",
        domain="example.com",
        publisher="Example Publisher",
        source_type="Industry Publication",
        is_primary_source=False,
        publication_date="2026-08-17",
        provenance_complete=True,
        notes="Source metadata.",
    )

    assert isinstance(
        assessment,
        ExternalSourceAssessment,
    )

    print(
        "Assessment Creation            : PASS"
    )

    # ======================================================
    # FIELD TRANSFER
    # ======================================================

    assert (
        assessment.source_url
        == "https://example.com/article"
    )

    assert (
        assessment.domain
        == "example.com"
    )

    assert (
        assessment.publisher
        == "Example Publisher"
    )

    assert (
        assessment.source_type
        == "Industry Publication"
    )

    assert (
        assessment.is_primary_source
        is False
    )

    assert (
        assessment.publication_date
        == "2026-08-17"
    )

    assert (
        assessment.provenance_complete
        is True
    )

    assert (
        assessment.notes
        == "Source metadata."
    )

    print(
        "Field Transfer                 : PASS"
    )

    # ======================================================
    # INPUT VALIDATION
    # ======================================================

    invalid_inputs = [
        (
            {
                "source_url": None,
            },
            "Invalid source URL type",
        ),
        (
            {
                "domain": None,
            },
            "Invalid domain type",
        ),
        (
            {
                "publisher": None,
            },
            "Invalid publisher type",
        ),
        (
            {
                "source_type": None,
            },
            "Invalid source type",
        ),
        (
            {
                "is_primary_source": "yes",
            },
            "Invalid primary-source type",
        ),
        (
            {
                "publication_date": None,
            },
            "Invalid publication date type",
        ),
        (
            {
                "provenance_complete": "yes",
            },
            "Invalid provenance type",
        ),
        (
            {
                "notes": None,
            },
            "Invalid notes type",
        ),
    ]

    for kwargs, message in invalid_inputs:

        try:

            engine.assess(**kwargs)

            raise AssertionError(
                message
                + " accepted"
            )

        except ValueError:

            pass

    print(
        "Input Validation               : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    source_url = (
        "https://example.com/article"
    )

    domain = "example.com"

    publisher = "Example Publisher"

    assessment = engine.assess(
        source_url=source_url,
        domain=domain,
        publisher=publisher,
        source_type="Industry Publication",
    )

    assert (
        source_url
        == "https://example.com/article"
    )

    assert (
        domain
        == "example.com"
    )

    assert (
        publisher
        == "Example Publisher"
    )

    assert (
        assessment.source_url
        == source_url
    )

    print(
        "Input Immutability              : PASS"
    )

    # ======================================================
    # NO ANALYTICAL CALCULATION
    # ======================================================

    assert not hasattr(
        assessment,
        "confidence",
    )

    assert not hasattr(
        assessment,
        "evidence_score",
    )

    assert not hasattr(
        assessment,
        "source_quality",
    )

    assert not hasattr(
        assessment,
        "credibility_score",
    )

    assert not hasattr(
        assessment,
        "opportunity_score",
    )

    assert not hasattr(
        assessment,
        "valuation",
    )

    print(
        "Analytical Boundary             : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL SOURCE "
        "ASSESSMENT ENGINE : PASS"
    )


if __name__ == "__main__":
    main()