from dataclasses import dataclass

from .decision_models import Recommendation
from .conviction_engine import ConvictionResult
from .margin_of_safety_engine import MarginOfSafetyResult
from .expected_return_engine import ExpectedReturnResult
from .position_sizing_engine import PositionSizingResult


@dataclass(slots=True)
class DecisionEngineResult:
    recommendation: Recommendation
    score: float
    summary: str


class DecisionEngine:
    """
    Converts all research outputs into a final investment recommendation.
    """

    def evaluate(
        self,
        conviction: ConvictionResult,
        margin: MarginOfSafetyResult,
        expected_return: ExpectedReturnResult,
        position: PositionSizingResult,
        kill_switch: bool = False,
    ) -> DecisionEngineResult:

        # Immediate rejection
        if kill_switch:
            return DecisionEngineResult(
                recommendation=Recommendation.REJECT,
                score=0.0,
                summary="Investment rejected due to Kill Switch."
            )

        score = 0.0

        # Conviction (40%)
        score += conviction.score * 0.40

        # Margin of Safety (30%)
        mos = max(0.0, min(margin.margin_of_safety, 50.0))
        score += (mos / 50.0) * 30.0

        # Expected Return (30%)
        cagr = max(0.0, min(expected_return.expected_cagr, 30.0))
        score += (cagr / 30.0) * 30.0

        score = round(score, 2)

        if score >= 85:
            recommendation = Recommendation.STRONG_BUY

        elif score >= 70:
            recommendation = Recommendation.BUY

        elif score >= 55:
            recommendation = Recommendation.WATCH

        elif score >= 40:
            recommendation = Recommendation.SELL

        else:
            recommendation = Recommendation.REJECT

        summary = (
            f"Decision Score: {score:.2f}/100 | "
            f"Recommendation: {recommendation.value} | "
            f"Suggested Target Weight: {position.target_weight:.2f}%"
        )

        return DecisionEngineResult(
            recommendation=recommendation,
            score=score,
            summary=summary,
        )