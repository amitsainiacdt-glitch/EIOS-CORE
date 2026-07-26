"""
EIOS
Everest Investment Operating System

Earnings Power Value (EPV) Engine

Purpose:
Calculates intrinsic value assuming no future growth.
"""

from modules.valuation.valuation_models import ValuationResult


class EPVEngine:
    """
    Earnings Power Value valuation.
    """

    METHOD_NAME = "EPV"
    ASSUMPTION_KEY = "epv"

    def evaluate(self, assumptions: dict):

        normalized_earnings = assumptions["normalized_earnings"]
        discount_rate = assumptions["discount_rate"]

        if discount_rate <= 0:
            raise ValueError("Discount rate must be greater than zero.")

        intrinsic_value = normalized_earnings / discount_rate

        return ValuationResult(
            method="Earnings Power Value",
            fair_value=round(intrinsic_value, 2),
            confidence=60,
            summary="Intrinsic value estimated using Earnings Power Value.",
            assumptions=[
                f"Normalized Earnings = {normalized_earnings}",
                f"Discount Rate = {discount_rate:.2%}"
            ],
            risks=[
                "Assumes no future growth.",
                "Sensitive to normalized earnings.",
                "Sensitive to discount rate."
            ],
            evidence=[],
            metadata={
                "normalized_earnings": normalized_earnings
            }
        )