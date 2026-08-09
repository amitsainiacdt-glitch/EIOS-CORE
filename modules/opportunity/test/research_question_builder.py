"""
EIOS
Everest Investment Operating System

Opportunity Research Question Builder Test
"""

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)

from modules.opportunity.research_question_builder import (
    OpportunityResearchQuestionBuilder,
)


def main() -> None:

    intake = OpportunityResearchIntake(
        company="Test Company",
        ticker="TEST",
        sector="Industrial",
        industry="Engineering",

        discovery_score=85.0,
        discovery_confidence=80.0,

        strengths=[
            "Strong competitive position",
        ],

        concerns=[
            "Valuation may be demanding",
        ],

        catalysts=[
            "Capacity expansion",
            "Industry upcycle",
        ],

        risks=[
            "Execution risk",
        ],

        discovery_notes=[
            "Candidate identified through Discovery."
        ],
    )

    builder = (
        OpportunityResearchQuestionBuilder()
    )

    questions = builder.build(intake)

    assert len(questions) > 0

    question_text = [
        question.question
        for question in questions
    ]

    # ------------------------------------------------------
    # Catalyst questions
    # ------------------------------------------------------

    assert any(
        "Capacity expansion" in question
        for question in question_text
    )

    assert any(
        "Industry upcycle" in question
        for question in question_text
    )

    # ------------------------------------------------------
    # Concern
    # ------------------------------------------------------

    assert any(
        "Valuation may be demanding" in question
        for question in question_text
    )

    # ------------------------------------------------------
    # Risk
    # ------------------------------------------------------

    assert any(
        "Execution risk" in question
        for question in question_text
    )

    # ------------------------------------------------------
    # Core Opportunity Questions
    # ------------------------------------------------------

    assert any(
        "market currently" in question
        for question in question_text
    )

    assert any(
        "disconfirm" in question
        for question in question_text
    )

    assert any(
        "kill switch" in question
        for question in question_text
    )

    # ------------------------------------------------------
    # Weighted questions
    # ------------------------------------------------------

    assert all(
        question.weight > 0
        for question in questions
    )

    # ------------------------------------------------------
    # Intake immutability
    # ------------------------------------------------------

    assert intake.company == "Test Company"
    assert intake.catalysts == [
        "Capacity expansion",
        "Industry upcycle",
    ]

    assert intake.risks == [
        "Execution risk",
    ]

    print(
        "Catalyst Questions       : PASS"
    )

    print(
        "Concern Questions        : PASS"
    )

    print(
        "Risk Questions           : PASS"
    )

    print(
        "Core Opportunity Questions : PASS"
    )

    print(
        "Weighted Questions       : PASS"
    )

    print(
        "Intake Immutability      : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS OPPORTUNITY RESEARCH QUESTION BUILDER : PASS"
    )


if __name__ == "__main__":
    main()