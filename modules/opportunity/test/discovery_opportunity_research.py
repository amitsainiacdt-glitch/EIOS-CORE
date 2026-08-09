"""
EIOS
Everest Investment Operating System

Discovery → Opportunity Research Preparation Integration Test
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.opportunity.discovery_opportunity_adapter import (
    DiscoveryOpportunityAdapter,
)

from modules.opportunity.research_question_builder import (
    OpportunityResearchQuestionBuilder,
)


def main() -> None:

    # ======================================================
    # DISCOVERY CANDIDATE
    # ======================================================

    candidate = DiscoveryCandidate(
        company_name="Test Company",
        ticker="TEST",
        sector="Industrial",
        industry="Engineering",

        overall_score=88.0,
        status="Passed",
        confidence=85.0,

        strengths=[
            "Strong competitive position",
        ],

        concerns=[
            "Valuation requires validation",
        ],

        catalysts=[
            "Capacity expansion",
            "Industry demand growth",
        ],

        risks=[
            "Execution risk",
        ],

        discovery_notes=[
            "Candidate identified by Discovery Office."
        ],

        source="EIOS Discovery",
    )

    # ======================================================
    # DISCOVERY → OPPORTUNITY INTAKE
    # ======================================================

    adapter = DiscoveryOpportunityAdapter()

    intake = adapter.create_intake(
        candidate
    )

    assert intake.company == "Test Company"
    assert intake.discovery_score == 88.0

    # ======================================================
    # INTAKE → RESEARCH QUESTIONS
    # ======================================================

    builder = (
        OpportunityResearchQuestionBuilder()
    )

    questions = builder.build(
        intake
    )

    assert len(questions) > 0

    question_text = [
        question.question
        for question in questions
    ]

    # ======================================================
    # DISCOVERY INTELLIGENCE MUST SURVIVE
    # ======================================================

    assert any(
        "Capacity expansion" in question
        for question in question_text
    )

    assert any(
        "Industry demand growth" in question
        for question in question_text
    )

    assert any(
        "Execution risk" in question
        for question in question_text
    )

    assert any(
        "Valuation requires validation" in question
        for question in question_text
    )

    # ======================================================
    # CORE OPPORTUNITY QUESTIONS
    # ======================================================

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

    # ======================================================
    # NO ANALYSIS HAS BEEN INVENTED
    # ======================================================

    assert intake.research_status == (
        "NOT_STARTED"
    )

    # ======================================================
    # SOURCE IMMUTABILITY
    # ======================================================

    assert candidate.overall_score == 88.0
    assert candidate.confidence == 85.0

    assert candidate.catalysts == [
        "Capacity expansion",
        "Industry demand growth",
    ]

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Discovery → Intake             : PASS"
    )

    print(
        "Intake → Research Questions    : PASS"
    )

    print(
        "Catalyst Intelligence Preserved : PASS"
    )

    print(
        "Risk / Concern Intelligence     : PASS"
    )

    print(
        "Core Opportunity Questions      : PASS"
    )

    print(
        "No Invented Analysis             : PASS"
    )

    print(
        "Source Immutability              : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS DISCOVERY → OPPORTUNITY RESEARCH PREPARATION : PASS"
    )


if __name__ == "__main__":
    main()