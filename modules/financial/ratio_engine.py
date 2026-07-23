"""
Ratio Engine

Calculates financial ratios.
"""


class RatioEngine:

    def roce(self, ebit, capital_employed):

        if capital_employed == 0:
            return 0

        return (ebit / capital_employed) * 100

    def roe(self, net_profit, shareholder_equity):

        if shareholder_equity == 0:
            return 0

        return (net_profit / shareholder_equity) * 100

    def debt_to_equity(self, total_debt, shareholder_equity):

        if shareholder_equity == 0:
            return 0

        return total_debt / shareholder_equity

    def interest_coverage(self, ebit, interest_expense):

        if interest_expense == 0:
            return 0

        return ebit / interest_expense

    def asset_turnover(self, revenue, total_assets):

        if total_assets == 0:
            return 0

        return revenue / total_assets