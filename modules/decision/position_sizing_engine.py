from dataclasses import dataclass

from .decision_models import ConvictionLevel


@dataclass(slots=True)
class PositionSizingResult:
    initial_weight: float
    target_weight: float
    maximum_weight: float
    capital_to_deploy: float
    remaining_cash: float
    notes: str


class PositionSizingEngine:
    """
    Determines how much capital should be allocated
    based on conviction and margin of safety.
    """

    def calculate(
        self,
        conviction: ConvictionLevel,
        margin_of_safety: float,
        available_cash: float,
        existing_weight: float = 0.0,
        portfolio_limit: float = 10.0,
    ) -> PositionSizingResult:

        if available_cash < 0:
            raise ValueError("Available cash cannot be negative.")

        if existing_weight < 0:
            raise ValueError("Existing weight cannot be negative.")

        if portfolio_limit <= 0:
            raise ValueError("Portfolio limit must be positive.")

        # Base target weight from conviction
        if conviction == ConvictionLevel.VERY_HIGH:
            target = 10.0

        elif conviction == ConvictionLevel.HIGH:
            target = 8.0

        elif conviction == ConvictionLevel.MEDIUM:
            target = 5.0

        elif conviction == ConvictionLevel.LOW:
            target = 2.5

        else:
            target = 0.0

        # Margin of Safety adjustment
        if margin_of_safety >= 40:
            target += 1.0
        elif margin_of_safety >= 25:
            target += 0.5
        elif margin_of_safety < 0:
            target -= 2.0

        target = max(0.0, min(target, portfolio_limit))

        additional_weight = max(0.0, target - existing_weight)

        capital = available_cash * (additional_weight / 100)

        remaining = available_cash - capital

        return PositionSizingResult(
            initial_weight=existing_weight,
            target_weight=round(target, 2),
            maximum_weight=portfolio_limit,
            capital_to_deploy=round(capital, 2),
            remaining_cash=round(remaining, 2),
            notes="Position sizing completed successfully.",
        )