"""
===============================================================================
EIOS
Everest Investment Operating System

Opportunity Score Engine

Purpose:
    Calculates the institutional Opportunity Score.

Rules:
    - Performs scoring only.
    - No persistence.
    - No UI logic.
===============================================================================
"""

from modules.opportunity.opportunity_models import OpportunityScore


class OpportunityScoreEngine:
    """
    Calculates Opportunity Scores.
    """

    MAX_SCORE = 100.0

    def calculate(
        self,
        *,
        catalyst: float,
        earnings: float,
        sector: float,
        valuation: float,
        institutional: float,
        expansion: float,
        risk: float,
    ) -> OpportunityScore:

        score = OpportunityScore()

        score.catalyst = catalyst
        score.earnings = earnings
        score.sector = sector
        score.valuation = valuation
        score.institutional = institutional
        score.expansion = expansion
        score.risk = risk

        score.total = (
            catalyst
            + earnings
            + sector
            + valuation
            + institutional
            + expansion
            + risk
        )

        score.total = min(
            self.MAX_SCORE,
            max(0.0, score.total),
        )

        score.confidence = score.total

        return score