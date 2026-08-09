"""
EIOS
Everest Investment Operating System

Opportunity Research Question Builder

Purpose:
    Converts Discovery intelligence into
    Opportunity-specific research questions.

Architecture:
    Discovery Candidate
        ↓
    OpportunityResearchIntake
        ↓
    OpportunityResearchQuestionBuilder
        ↓
    Question objects
        ↓
    Existing Research QuestionEngine

Design Principles:
    - Generates questions only.
    - Does not answer questions.
    - Does not calculate scores.
    - Does not perform valuation.
    - Does not mutate the intake.
    - Does not duplicate QuestionEngine.
    - Does not invent company-specific facts.
"""

from typing import List

from modules.research.question_engine import Question

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)


class OpportunityResearchQuestionBuilder:
    """
    Builds Opportunity-specific research questions from
    Discovery intelligence.
    """

    # ==========================================================
    # BUILD
    # ==========================================================

    def build(
        self,
        intake: OpportunityResearchIntake,
    ) -> List[Question]:
        """
        Generate weighted research questions from the
        Discovery → Opportunity intake.

        Questions are derived only from information actually
        present in the intake.
        """

        questions: List[Question] = []

        # ------------------------------------------------------
        # Catalyst Validation
        # ------------------------------------------------------

        for catalyst in intake.catalysts:

            questions.append(
                Question(
                    question=(
                        f"Is the identified catalyst "
                        f"'{catalyst}' real, measurable, "
                        f"and supported by independent evidence?"
                    ),
                    weight=15,
                )
            )

            questions.append(
                Question(
                    question=(
                        f"How could the catalyst "
                        f"'{catalyst}' translate into "
                        f"revenue, margins, earnings or "
                        f"free cash flow?"
                    ),
                    weight=15,
                )
            )

        # ------------------------------------------------------
        # Concerns
        # ------------------------------------------------------

        for concern in intake.concerns:

            questions.append(
                Question(
                    question=(
                        f"Can the concern '{concern}' "
                        f"materially impair the investment thesis?"
                    ),
                    weight=15,
                )
            )

            questions.append(
                Question(
                    question=(
                        f"What evidence would confirm or "
                        f"disconfirm the concern '{concern}'?"
                    ),
                    weight=10,
                )
            )

        # ------------------------------------------------------
        # Risks
        # ------------------------------------------------------

        for risk in intake.risks:

            questions.append(
                Question(
                    question=(
                        f"What is the financial and business "
                        f"impact of the identified risk '{risk}'?"
                    ),
                    weight=15,
                )
            )

            questions.append(
                Question(
                    question=(
                        f"What observable evidence would "
                        f"indicate that the risk '{risk}' "
                        f"is becoming material?"
                    ),
                    weight=10,
                )
            )

        # ------------------------------------------------------
        # Strengths
        # ------------------------------------------------------

        for strength in intake.strengths:

            questions.append(
                Question(
                    question=(
                        f"Is the identified strength "
                        f"'{strength}' supported by durable "
                        f"evidence and competitive economics?"
                    ),
                    weight=10,
                )
            )

        # ------------------------------------------------------
        # Core Opportunity Questions
        # ------------------------------------------------------

        questions.extend(
            [
                Question(
                    question=(
                        "What does the market currently "
                        "appear to expect from this company?"
                    ),
                    weight=20,
                ),
                Question(
                    question=(
                        "What does EIOS believe could be "
                        "different from current market expectations?"
                    ),
                    weight=20,
                ),
                Question(
                    question=(
                        "How does the identified opportunity "
                        "translate into incremental earnings "
                        "and free cash flow?"
                    ),
                    weight=20,
                ),
                Question(
                    question=(
                        "What evidence would demonstrate that "
                        "the opportunity is being underestimated "
                        "by the market?"
                    ),
                    weight=20,
                ),
                Question(
                    question=(
                        "What evidence could disconfirm the "
                        "opportunity thesis?"
                    ),
                    weight=20,
                ),
                Question(
                    question=(
                        "What single observation should act as "
                        "the kill switch for the opportunity thesis?"
                    ),
                    weight=20,
                ),
            ]
        )

        return questions


__all__ = [
    "OpportunityResearchQuestionBuilder",
]