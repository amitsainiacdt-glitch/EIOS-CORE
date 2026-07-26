from dataclasses import dataclass

from .decision_models import ConvictionLevel


@dataclass(slots=True)
class ConvictionResult:
    score: float
    level: ConvictionLevel
    explanation: str


class ConvictionEngine:
    """
    Combines research scores into a single institutional conviction score.

    Each input score must be between 0 and 100.
    """

    WEIGHTS = {
        "business": 0.25,
        "financial": 0.20,
        "management": 0.20,
        "competitive": 0.15,
        "risk": 0.10,
        "valuation": 0.10,
    }

    def calculate(
        self,
        business: float,
        financial: float,
        management: float,
        competitive: float,
        risk: float,
        valuation: float,
    ) -> ConvictionResult:

        scores = {
            "business": business,
            "financial": financial,
            "management": management,
            "competitive": competitive,
            "risk": risk,
            "valuation": valuation,
        }

        for name, value in scores.items():
            if not 0 <= value <= 100:
                raise ValueError(
                    f"{name} score must be between 0 and 100."
                )

        weighted_score = sum(
            scores[key] * self.WEIGHTS[key]
            for key in self.WEIGHTS
        )

        if weighted_score >= 90:
            level = ConvictionLevel.VERY_HIGH
            explanation = "Institutional-grade conviction."

        elif weighted_score >= 80:
            level = ConvictionLevel.HIGH
            explanation = "High confidence investment."

        elif weighted_score >= 65:
            level = ConvictionLevel.MEDIUM
            explanation = "Requires continued monitoring."

        elif weighted_score >= 50:
            level = ConvictionLevel.LOW
            explanation = "Weak investment case."

        else:
            level = ConvictionLevel.VERY_LOW
            explanation = "Investment should not proceed."

        return ConvictionResult(
            score=round(weighted_score, 2),
            level=level,
            explanation=explanation,
        )