"""
EIOS
Everest Investment Operating System

Opportunity Questions → Research Pipeline Integration Test
"""

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)

from modules.opportunity.research_question_builder import (
    OpportunityResearchQuestionBuilder,
)

from modules.research.research_pipeline import (
    ResearchPipeline,
)


class DummyResearch:
    """
    Minimal research object for integration testing.
    """
    pass


def main() -> None:

    # ======================================================
    # DISCOVERY → OPPORTUNITY INTAKE
    # ======================================================

    intake = OpportunityResearchIntake(
        company="Integration Company",
        ticker="INT",
        sector="Industrial",
        industry="Engineering",

        discovery_score=88.0,
        discovery_confidence=85.0,

        catalysts=[
            "Capacity expansion",
        ],

        risks=[
            "Execution risk",
        ],

        concerns=[
            "Valuation requires validation",
        ],

        strengths=[
            "Strong competitive position",
        ],
    )

    # ======================================================
    # OPPORTUNITY QUESTIONS
    # ======================================================

    builder = (
        OpportunityResearchQuestionBuilder()
    )

    opportunity_questions = builder.build(
        intake
    )

    assert len(opportunity_questions) > 0

    # ======================================================
    # EXISTING RESEARCH PIPELINE
    # ======================================================

    pipeline = ResearchPipeline(
        DummyResearch()
    )

    # We are deliberately testing the question injection
    # without executing the full institutional research flow.

    for question in opportunity_questions:

        pipeline.question_engine.add(
            question.question,
            question.weight,
        )

    # Existing generic questions are not required here.
    # We are validating that Opportunity questions can enter
    # the existing QuestionEngine contract unchanged.

    stored_questions = (
        pipeline.question_engine.questions
    )

    assert len(stored_questions) == (
        len(opportunity_questions)
    )

    # ======================================================
    # QUESTION PRESERVATION
    # ======================================================

    for original, stored in zip(
        opportunity_questions,
        stored_questions,
    ):

        assert stored.question == (
            original.question
        )

        assert stored.weight == (
            original.weight
        )

    # ======================================================
    # WEIGHT PRESERVATION
    # ======================================================

    expected_weight = sum(
        question.weight
        for question in opportunity_questions
    )

    assert (
        pipeline.question_engine.total_weight()
        == expected_weight
    )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Opportunity Questions → QuestionEngine : PASS"
    )

    print(
        "Question Text Preservation              : PASS"
    )

    print(
        "Question Weight Preservation             : PASS"
    )

    print(
        "Question Total Weight                    : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS OPPORTUNITY QUESTIONS → RESEARCH PIPELINE : PASS"
    )


if __name__ == "__main__":
    main()