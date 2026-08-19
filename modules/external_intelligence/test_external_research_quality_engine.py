"""
EIOS
Everest Investment Operating System

External Research Quality Engine Test
======================================
"""

from modules.external_intelligence.external_content_normalizer import (
    NormalizedExternalContent,
)

from modules.external_intelligence.external_research_quality_engine import (
    ExternalResearchQualityEngine,
)

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)


def make_query():

    return ExternalResearchQuery(
        company="Tata Motors",
        ticker="TATAMOTORS",
        question=(
            "Is automotive demand improving "
            "and supported by independent evidence?"
        ),
        query=(
            '"Tata Motors" automotive demand improving'
        ),
        intent="OPPORTUNITY_RESEARCH",
    )


def make_content(
    text=(
        "Tata Motors reported improving automotive demand "
        "with stronger order activity during the period. "
        "This is synthetic research content for testing."
    ),
):

    return NormalizedExternalContent(
        url=(
            "https://example.com/"
            "tata-motors-demand"
        ),
        status_code=200,
        original_content=text,
        normalized_text=text,
        content_type="text/html",
    )


def make_source():

    return ExternalSourceAssessment(
        source_url=(
            "https://example.com/"
            "tata-motors-demand"
        ),
        domain="example.com",
        publisher="Mock Provider",
        source_type="Secondary",
        is_primary_source=False,
        publication_date=None,
        provenance_complete=True,
    )


def main():

    print("=" * 60)
    print(
        "EIOS EXTERNAL RESEARCH QUALITY ENGINE TEST"
    )
    print("=" * 60)

    engine = (
        ExternalResearchQualityEngine()
    )

    # ==================================================
    # TEST 1 — ENGINE CREATION
    # ==================================================

    assert engine is not None

    print(
        "Test 1 — Engine Creation             : PASS"
    )

    # ==================================================
    # TEST 2 — VALID RESEARCH ACCEPTED
    # ==================================================

    result = engine.assess(
        query=make_query(),
        normalized_content=make_content(),
        source_assessment=make_source(),
    )

    assert result.accepted is True
    assert result.content_valid is True
    assert result.source_valid is True
    assert result.research_context_valid is True

    print(
        "Test 2 — Valid Research Accepted      : PASS"
    )

    # ==================================================
    # TEST 3 — ACCEPTANCE REASON
    # ==================================================

    assert result.reason

    print(
        "Test 3 — Acceptance Reason             : PASS"
    )

    # ==================================================
    # TEST 4 — EMPTY CONTENT REJECTED
    # ==================================================

    empty_content = make_content(
        text=""
    )

    result = engine.assess(
        query=make_query(),
        normalized_content=empty_content,
        source_assessment=make_source(),
    )

    assert result.accepted is False
    assert result.content_valid is False

    print(
        "Test 4 — Empty Content Rejected        : PASS"
    )

    # ==================================================
    # TEST 5 — SHORT CONTENT REJECTED
    # ==================================================

    short_content = make_content(
        text="Too short."
    )

    result = engine.assess(
        query=make_query(),
        normalized_content=short_content,
        source_assessment=make_source(),
    )

    assert result.accepted is False
    assert result.content_valid is False

    print(
        "Test 5 — Short Content Rejected        : PASS"
    )

    # ==================================================
    # TEST 6 — INVALID SOURCE REJECTED
    # ==================================================

    invalid_source = ExternalSourceAssessment(
        source_url=(
            "https://example.com/"
            "tata-motors-demand"
        ),
        domain="example.com",
        publisher="Mock Provider",
        source_type="Secondary",
        is_primary_source=False,
        publication_date=None,
        provenance_complete=False,
    )

    result = engine.assess(
        query=make_query(),
        normalized_content=make_content(),
        source_assessment=invalid_source,
    )

    assert result.accepted is False
    assert result.source_valid is False

    print(
        "Test 6 — Invalid Source Rejected       : PASS"
    )

    # ==================================================
    # TEST 7 — SOURCE URL MISMATCH
    # ==================================================

    mismatched_source = ExternalSourceAssessment(
        source_url="https://example.com/other",
        domain="example.com",
        publisher="Mock Provider",
        source_type="Secondary",
        is_primary_source=False,
        publication_date=None,
        provenance_complete=True,
    )

    result = engine.assess(
        query=make_query(),
        normalized_content=make_content(),
        source_assessment=mismatched_source,
    )

    assert result.accepted is False
    assert result.source_valid is False

    print(
        "Test 7 — Source Mismatch Rejected      : PASS"
    )

    # ==================================================
    # TEST 8 — BAD HTTP STATUS REJECTED
    # ==================================================

    bad_status_content = (
        NormalizedExternalContent(
            url=(
                "https://example.com/"
                "tata-motors-demand"
            ),
            status_code=404,
            original_content=(
                "Tata Motors research content."
            ),
            normalized_text=(
                "Tata Motors reported improving "
                "automotive demand with stronger "
                "order activity during the period."
            ),
            content_type="text/html",
        )
    )

    result = engine.assess(
        query=make_query(),
        normalized_content=bad_status_content,
        source_assessment=make_source(),
    )

    assert result.accepted is False
    assert result.source_valid is False

    print(
        "Test 8 — Bad HTTP Status Rejected      : PASS"
    )

    # ==================================================
    # TEST 9 — INVALID QUERY CONTEXT
    # ==================================================

    invalid_query = ExternalResearchQuery(
        company="",
        ticker="TATAMOTORS",
        question=(
            "Is automotive demand improving?"
        ),
        query=(
            '"Tata Motors" automotive demand'
        ),
        intent="OPPORTUNITY_RESEARCH",
    )

    result = engine.assess(
        query=invalid_query,
        normalized_content=make_content(),
        source_assessment=make_source(),
    )

    assert result.accepted is False
    assert result.research_context_valid is False

    print(
        "Test 9 — Invalid Query Rejected        : PASS"
    )

    # ==================================================
    # TEST 10 — IMMUTABILITY
    # ==================================================

    result = engine.assess(
        query=make_query(),
        normalized_content=make_content(),
        source_assessment=make_source(),
    )

    try:
        result.accepted = False

        raise AssertionError(
            "ResearchQualityResult must be immutable"
        )

    except AttributeError:
        pass

    print(
        "Test 10 — Result Immutability           : PASS"
    )

    # ==================================================
    # FINAL
    # ==================================================

    print()
    print(
        "EIOS EXTERNAL RESEARCH QUALITY ENGINE "
        ": ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()