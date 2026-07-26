from .decision_models import (
    DecisionResult,
    PriorityLevel,
)

from .margin_of_safety_engine import MarginOfSafetyEngine
from .expected_return_engine import ExpectedReturnEngine
from .conviction_engine import ConvictionEngine
from .position_sizing_engine import PositionSizingEngine
from .decision_engine import DecisionEngine


class DecisionOffice:
    """
    Decision Office orchestrates all decision-related engines.

    Responsibilities:
        - Margin of Safety
        - Expected Return
        - Conviction
        - Position Sizing
        - Final Recommendation

    No calculations should exist in this class.
    """

    def __init__(self):
        self.margin_engine = MarginOfSafetyEngine()
        self.return_engine = ExpectedReturnEngine()
        self.conviction_engine = ConvictionEngine()
        self.position_engine = PositionSizingEngine()
        self.decision_engine = DecisionEngine()

    def evaluate(
        self,
        *,
        intrinsic_value: float,
        market_price: float,
        business_score: float,
        financial_score: float,
        management_score: float,
        competitive_score: float,
        risk_score: float,
        valuation_score: float,
        available_cash: float,
        existing_weight: float = 0.0,
        portfolio_limit: float = 10.0,
        kill_switch: bool = False,
    ) -> DecisionResult:

        margin = self.margin_engine.calculate(
            intrinsic_value,
            market_price,
        )

        expected_return = self.return_engine.calculate_5y(
            market_price,
            intrinsic_value,
        )

        conviction = self.conviction_engine.calculate(
            business_score,
            financial_score,
            management_score,
            competitive_score,
            risk_score,
            valuation_score,
        )

        position = self.position_engine.calculate(
            conviction.level,
            margin.margin_of_safety,
            available_cash,
            existing_weight,
            portfolio_limit,
        )

        final = self.decision_engine.evaluate(
            conviction,
            margin,
            expected_return,
            position,
            kill_switch,
        )

        return DecisionResult(
            recommendation=final.recommendation,
            conviction=conviction.level,
            priority=PriorityLevel.NORMAL,
            margin_of_safety=margin.margin_of_safety,
            expected_return_5y=expected_return.expected_cagr,
            position_size=position,
            confidence=final.score,
            summary=final.summary,
        )