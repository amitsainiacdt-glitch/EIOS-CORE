"""
Working Capital Engine

Analyzes working capital efficiency.
"""


class WorkingCapitalEngine:

    def working_capital(self, current_assets, current_liabilities):

        return current_assets - current_liabilities

    def current_ratio(self, current_assets, current_liabilities):

        if current_liabilities == 0:
            return 0

        return current_assets / current_liabilities

    def working_capital_turnover(self, revenue, working_capital):

        if working_capital == 0:
            return 0

        return revenue / working_capital

    def cash_conversion_cycle(
        self,
        inventory_days,
        receivable_days,
        payable_days,
    ):

        return (
            inventory_days
            + receivable_days
            - payable_days
        )