"""
EIOS
Everest Investment Operating System

Research Pipeline Backward Compatibility Test
"""

from modules.research.research_pipeline import (
    ResearchPipeline,
)


class DummyResearch:
    pass


def main() -> None:

    pipeline = ResearchPipeline(
        DummyResearch()
    )

    # ------------------------------------------------------
    # Legacy call
    #
    # No opportunity_questions supplied.
    # ------------------------------------------------------

    pipeline.question_engine.add(
        "Legacy question",
        10,
    )

    assert (
        len(pipeline.question_engine.questions)
        == 1
    )

    assert (
        pipeline.question_engine.questions[0].question
        == "Legacy question"
    )

    assert (
        pipeline.question_engine.questions[0].weight
        == 10
    )

    # ------------------------------------------------------
    # Opportunity question injection
    #
    # Verify the same QuestionEngine contract.
    # ------------------------------------------------------

    pipeline.question_engine.add(
        "Opportunity-specific question",
        20,
    )

    assert (
        len(pipeline.question_engine.questions)
        == 2
    )

    assert (
        pipeline.question_engine.questions[1].question
        == "Opportunity-specific question"
    )

    assert (
        pipeline.question_engine.questions[1].weight
        == 20
    )

    # ------------------------------------------------------
    # Total weight
    # ------------------------------------------------------

    assert (
        pipeline.question_engine.total_weight()
        == 30
    )

    print(
        "Legacy QuestionEngine Behaviour : PASS"
    )

    print(
        "Opportunity Question Contract    : PASS"
    )

    print(
        "Question Weight Preservation     : PASS"
    )

    print(
        "Backward Compatibility           : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS RESEARCH PIPELINE BACKWARD COMPATIBILITY : PASS"
    )


if __name__ == "__main__":
    main()