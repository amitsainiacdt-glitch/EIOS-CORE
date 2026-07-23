"""
ROIIC Engine

Calculates Return on Incremental Invested Capital (ROIIC).
"""


class ROIICEngine:
    """
    Return on Incremental Invested Capital

    ROIIC = Incremental NOPAT / Incremental Invested Capital
    """

    def calculate(
        self,
        current_nopat,
        previous_nopat,
        current_invested_capital,
        previous_invested_capital,
    ):

        incremental_nopat = current_nopat - previous_nopat

        incremental_capital = (
            current_invested_capital
            - previous_invested_capital
        )

        if incremental_capital == 0:
            return 0

        return (
            incremental_nopat
            / incremental_capital
        ) * 100

    def interpret(self, roiic):

        if roiic >= 30:
            return "Excellent"

        if roiic >= 20:
            return "Very Good"

        if roiic >= 15:
            return "Good"

        if roiic >= 10:
            return "Average"

        if roiic >= 0:
            return "Weak"

        return "Value Destructive"