"""
EIOS
Everest Investment Operating System

Discounted Cash Flow (DCF) Engine

Purpose:
Calculates intrinsic value using a standard Discounted Cash Flow model.
"""

from modules.valuation.valuation_models import ValuationResult


class DCFEngine:
    """
    Calculates intrinsic value using the Discounted Cash Flow method.
    """

    METHOD_NAME = "DCF"
    ASSUMPTION_KEY = "dcf"

    def evaluate(self, assumptions: dict) -> ValuationResult:
        """
        Parameters
        ----------
        assumptions : dict
            {
                "current_fcf": float,
                "growth_rate": float,
                "discount_rate": float,
                "terminal_growth_rate": float,
                "forecast_years": int
            }

        Returns
        -------
        ValuationResult
        """

        current_fcf = assumptions["current_fcf"]
        growth = assumptions["growth_rate"]
        discount = assumptions["discount_rate"]
        terminal_growth = assumptions["terminal_growth_rate"]
        years = assumptions.get("forecast_years", 10)

        discounted_cashflows = []

        fcf = current_fcf

        for year in range(1, years + 1):
            fcf *= (1 + growth)
            present_value = fcf / ((1 + discount) ** year)
            discounted_cashflows.append(present_value)

        terminal_fcf = fcf * (1 + terminal_growth)

        terminal_value = (
            terminal_fcf /
            (discount - terminal_growth)
        )

        discounted_terminal = (
            terminal_value /
            ((1 + discount) ** years)
        )

        intrinsic_value = (
            sum(discounted_cashflows)
            + discounted_terminal
        )

        return ValuationResult(
            method="Discounted Cash Flow",
            fair_value=round(intrinsic_value, 2),
            confidence=60,
            summary="Intrinsic value estimated using Discounted Cash Flow.",
            assumptions=[
                f"Growth Rate = {growth:.2%}",
                f"Discount Rate = {discount:.2%}",
                f"Terminal Growth = {terminal_growth:.2%}",
                f"Forecast Years = {years}"
            ],
            risks=[
                "DCF is highly sensitive to growth assumptions.",
                "Discount rate significantly affects valuation.",
                "Terminal value usually dominates valuation."
            ],
            evidence=[],
            metadata={
                "discounted_cashflows": discounted_cashflows,
                "terminal_value": discounted_terminal
            }
        )