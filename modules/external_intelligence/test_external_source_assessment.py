"""
EIOS
Everest Investment Operating System

External Source Assessment Test
================================
"""

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)


def main() -> None:

    # ======================================================
    # MODEL
    # ======================================================

    assessment = ExternalSourceAssessment(
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
        "External Source Assessment : PASS"
    )

    # ======================================================
    # FIELD PRESERVATION
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
        "Field Preservation          : PASS"
    )

    # ======================================================
    # IMMUTABILITY
    # ======================================================

    try:

        assessment.domain = "changed.com"

        raise AssertionError(
            "Frozen assessment was mutable"
        )

    except AttributeError:

        pass

    print(
        "Immutability                 : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FIELDS
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
        "Analytical Boundary          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL SOURCE "
        "ASSESSMENT : PASS"
    )


if __name__ == "__main__":
    main()