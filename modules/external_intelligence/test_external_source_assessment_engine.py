"""
EIOS
Everest Investment Operating System

External Source Assessment Engine Test
=======================================
"""

from datetime import datetime

from modules.external_intelligence.external_content_normalizer import (
    ExternalContentNormalizer,
)

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)

from modules.external_intelligence.external_source_assessment_engine import (
    ExternalSourceAssessmentEngine,
)

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.external_intelligence.source_selection import (
    SelectedSource,
)


def make_selected_source() -> SelectedSource:

    return SelectedSource(
        result=ExternalSearchResult(
            title="Industrial Demand Research",
            url="https://example.com/article",
            snippet="Industrial demand research.",
            source="Example Publisher",
        ),
        selection_reason="Selected for research.",
    )


def make_retrieved_content() -> RetrievedContent:

    return RetrievedContent(
        url="https://example.com/article",
        status_code=200,
        content=(
            "<html>"
            "<body>"
            "<h1>Industrial Demand</h1>"
            "<p>Industrial demand is improving.</p>"
            "</body>"
            "</html>"
        ),
        content_type="text/html; charset=utf-8",
        headers={
            "Content-Type": (
                "text/html; charset=utf-8"
            )
        },
    )


def make_normalized_content() -> object:

    normalizer = ExternalContentNormalizer()

    return normalizer.normalize(
        make_retrieved_content()
    )


def main() -> None:

    engine = ExternalSourceAssessmentEngine()

    selected_source = (
        make_selected_source()
    )

    retrieved_content = (
        make_retrieved_content()
    )

    normalized_content = (
        make_normalized_content()
    )

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
        selected_source=selected_source,
        retrieved_content=retrieved_content,
        normalized_content=normalized_content,
        source_type="Industry Publication",
        is_primary_source=False,
        publication_date="2026-08-17",
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
    # URL PROVENANCE
    # ======================================================

    assert (
        assessment.source_url
        == selected_source.result.url
    )

    assert (
        retrieved_content.url
        == selected_source.result.url
    )

    assert (
        normalized_content.url
        == selected_source.result.url
    )

    print(
        "URL Provenance                 : PASS"
    )

    # ======================================================
    # DOMAIN EXTRACTION
    # ======================================================

    assert (
        assessment.domain
        == "example.com"
    )

    print(
        "Domain Extraction              : PASS"
    )

    # ======================================================
    # PUBLISHER PRESERVATION
    # ======================================================

    assert (
        assessment.publisher
        == selected_source.result.source
    )

    print(
        "Publisher Preservation         : PASS"
    )

    # ======================================================
    # INPUT VALIDATION
    # ======================================================

    try:

        engine.assess(
            selected_source=None,
            retrieved_content=retrieved_content,
            normalized_content=normalized_content,
        )

        raise AssertionError(
            "None selected source accepted"
        )

    except ValueError:

        pass

    try:

        engine.assess(
            selected_source=selected_source,
            retrieved_content=None,
            normalized_content=normalized_content,
        )

        raise AssertionError(
            "None retrieved content accepted"
        )

    except ValueError:

        pass

    try:

        engine.assess(
            selected_source=selected_source,
            retrieved_content=retrieved_content,
            normalized_content=None,
        )

        raise AssertionError(
            "None normalized content accepted"
        )

    except ValueError:

        pass

    print(
        "Input Validation               : PASS"
    )

    # ======================================================
    # TYPE VALIDATION
    # ======================================================

    try:

        engine.assess(
            selected_source="invalid",
            retrieved_content=retrieved_content,
            normalized_content=normalized_content,
        )

        raise AssertionError(
            "Invalid selected source accepted"
        )

    except ValueError:

        pass

    try:

        engine.assess(
            selected_source=selected_source,
            retrieved_content="invalid",
            normalized_content=normalized_content,
        )

        raise AssertionError(
            "Invalid retrieved content accepted"
        )

    except ValueError:

        pass

    try:

        engine.assess(
            selected_source=selected_source,
            retrieved_content=retrieved_content,
            normalized_content="invalid",
        )

        raise AssertionError(
            "Invalid normalized content accepted"
        )

    except ValueError:

        pass

    print(
        "Type Validation                : PASS"
    )

    # ======================================================
    # URL MISMATCH PROTECTION
    # ======================================================

    mismatched_retrieved = (
        RetrievedContent(
            url="https://different.example.com/article",
            status_code=200,
            content="Test content.",
            content_type="text/plain",
            headers={
                "Content-Type": "text/plain"
            },
        )
    )

    try:

        engine.assess(
            selected_source=selected_source,
            retrieved_content=mismatched_retrieved,
            normalized_content=normalized_content,
        )

        raise AssertionError(
            "Mismatched retrieved URL accepted"
        )

    except ValueError:

        pass

    print(
        "Retrieved URL Protection       : PASS"
    )

    # ======================================================
    # NORMALIZED URL MISMATCH
    # ======================================================

    mismatched_normalized = (
        ExternalContentNormalizer().normalize(
            RetrievedContent(
                url="https://different.example.com/article",
                status_code=200,
                content="Test content.",
                content_type="text/plain",
                headers={
                    "Content-Type": "text/plain"
                },
            )
        )
    )

    try:

        engine.assess(
            selected_source=selected_source,
            retrieved_content=retrieved_content,
            normalized_content=mismatched_normalized,
        )

        raise AssertionError(
            "Mismatched normalized URL accepted"
        )

    except ValueError:

        pass

    print(
        "Normalized URL Protection      : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    assert (
        selected_source.result.url
        == "https://example.com/article"
    )

    assert (
        selected_source.result.source
        == "Example Publisher"
    )

    assert (
        retrieved_content.content
        != ""
    )

    assert (
        normalized_content.original_content
        == retrieved_content.content
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