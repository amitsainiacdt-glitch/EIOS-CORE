"""
===============================================================================
Module: ownership_scorecard.py

Purpose:
    Calculate Ownership Quality Score for EIOS.

Responsibilities:
    - Combine ownership engine scores
    - Apply weighted scoring
    - Produce overall ownership score

Author:
    EIOS
===============================================================================
"""

from dataclasses import dataclass

from .ownership_utils import clamp_score


@dataclass
class OwnershipScoreCard:
    """
    Final Ownership Quality Score.
    """

    promoter_score: float = 0.0
    fii_score: float = 0.0
    dii_score: float = 0.0
    insider_score: float = 0.0
    concentration_score: float = 0.0
    governance_score: float = 0.0

    total_score: float = 0.0
    rating: str = "Unknown"


class OwnershipScoreCalculator:
    """
    Calculates final ownership quality score.
    """

    WEIGHTS = {
        "promoter": 0.35,
        "fii": 0.20,
        "dii": 0.15,
        "insider": 0.10,
        "concentration": 0.10,
        "governance": 0.10,
    }

    def calculate(
        self,
        promoter_score: float,
        fii_score: float,
        dii_score: float,
        insider_score: float,
        concentration_score: float,
        governance_score: float,
    ) -> OwnershipScoreCard:

        total = (
            promoter_score * self.WEIGHTS["promoter"]
            + fii_score * self.WEIGHTS["fii"]
            + dii_score * self.WEIGHTS["dii"]
            + insider_score * self.WEIGHTS["insider"]
            + concentration_score * self.WEIGHTS["concentration"]
            + governance_score * self.WEIGHTS["governance"]
        )

        total = clamp_score(total)

        return OwnershipScoreCard(
            promoter_score=promoter_score,
            fii_score=fii_score,
            dii_score=dii_score,
            insider_score=insider_score,
            concentration_score=concentration_score,
            governance_score=governance_score,
            total_score=total,
            rating=self._rating(total),
        )

    def _rating(self, score: float) -> str:

        if score >= 90:
            return "Exceptional"

        if score >= 80:
            return "Excellent"

        if score >= 70:
            return "Strong"

        if score >= 60:
            return "Good"

        if score >= 50:
            return "Average"

        return "Weak"