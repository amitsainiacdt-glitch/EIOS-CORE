"""
Financial Metrics

Calculates primary financial metrics.
"""


class FinancialMetrics:

    def revenue_growth(self, current, previous):

        if previous == 0:
            return 0

        return ((current - previous) / previous) * 100

    def eps_growth(self, current, previous):

        if previous == 0:
            return 0

        return ((current - previous) / previous) * 100

    def profit_growth(self, current, previous):

        if previous == 0:
            return 0

        return ((current - previous) / previous) * 100

    def free_cash_flow(self, operating_cash_flow, capex):

        return operating_cash_flow - capex