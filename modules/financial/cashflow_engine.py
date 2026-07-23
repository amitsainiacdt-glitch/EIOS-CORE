"""
Cash Flow Engine

Analyzes cash generation and cash flow quality.
"""


class CashFlowEngine:

    def free_cash_flow(self, operating_cash_flow, capital_expenditure):

        return operating_cash_flow - capital_expenditure

    def operating_cash_conversion(self, operating_cash_flow, net_profit):

        if net_profit == 0:
            return 0

        return operating_cash_flow / net_profit

    def cash_quality(self, operating_cash_flow, net_profit):

        conversion = self.operating_cash_conversion(
            operating_cash_flow,
            net_profit
        )

        if conversion >= 1.2:
            return "Excellent"

        if conversion >= 1.0:
            return "Good"

        if conversion >= 0.8:
            return "Average"

        return "Weak"