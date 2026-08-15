"""
EIOS
Everest Investment Operating System

External Research Query Builder Test
"""

from modules.research.question_engine import (
    Question,
)

from modules.external_intelligence.research_query_builder import (
    ExternalResearchQueryBuilder,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)


def main() -> None:

    # ======================================================
    # SOURCE QUESTION
    # ======================================================

    question = Question(
        question=(
            "Is the identified catalyst "
            "'Capacity expansion' real, measurable, "
            "and supported by independent evidence?"
        ),
        weight=15,
    )

    original_question = question.question
    original_weight = question.weight

    # ======================================================
    # BUILD
    # ======================================================

    builder = ExternalResearchQueryBuilder()

    result = builder.build(
        company="Test Company",
        ticker="TEST",
        question=question,
        intent="CATALYST_VALIDATION",
    )

    assert isinstance(
        result,
        ExternalResearchQuery,
    )

    print(
        "External Research Query    : PASS"
    )

    # ======================================================
    # IDENTITY
    # ======================================================

    assert result.company == "Test Company"
    assert result.ticker == "TEST"

    print(
        "Identity Preservation      : PASS"
    )

    # ======================================================
    # QUESTION PRESERVATION
    # ======================================================

    assert result.question == original_question

    print(
        "Question Preservation      : PASS"
    )

    # ======================================================
    # QUERY GENERATION
    # ======================================================

    assert "Test Company" in result.query
    assert "TEST" in result.query
    assert "Capacity expansion" in result.query

    print(
        "Query Generation           : PASS"
    )

    # ======================================================
    # INTENT
    # ======================================================

    assert (
        result.intent
        == "CATALYST_VALIDATION"
    )

    print(
        "Intent Preservation        : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    result_2 = builder.build(
        company="Test Company",
        ticker="TEST",
        question=question,
        intent="CATALYST_VALIDATION",
    )

    assert result == result_2

    print(
        "Deterministic Output       : PASS"
    )

    # ======================================================
    # SOURCE IMMUTABILITY
    # ======================================================

    assert question.question == original_question
    assert question.weight == original_weight

    print(
        "Source Question Immutability : PASS"
    )

    # ======================================================
    # INVALID INPUT PROTECTION
    # ======================================================

    try:
        builder.build(
            company="",
            ticker="TEST",
            question=question,
        )

        raise AssertionError(
            "Empty company was accepted"
        )

    except ValueError:
        pass

    try:
        builder.build(
            company="Test Company",
            ticker="",
            question=question,
        )

        raise AssertionError(
            "Empty ticker was accepted"
        )

    except ValueError:
        pass

    print(
        "Invalid Input Protection   : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        result,
        "evidence_score",
    )

    assert not hasattr(
        result,
        "confidence",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    assert not hasattr(
        result,
        "valuation",
    )

    print(
        "No Analytical Fabrication   : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL RESEARCH QUERY BUILDER : PASS"
    )


if __name__ == "__main__":
    main()