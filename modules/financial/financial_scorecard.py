"""
Financial Scorecard

Evaluates the overall financial strength of a company.
"""


class FinancialScorecard:

    def __init__(self):
        self.scorecard = {}

    def evaluate(
        self,
        revenue_growth,
        eps_growth,
        roce,
        roe,
        debt_to_equity,
        free_cash_flow,
    ):

        self.scorecard = {
            "Revenue Growth": revenue_growth,
            "EPS Growth": eps_growth,
            "ROCE": roce,
            "ROE": roe,
            "Debt to Equity": debt_to_equity,
            "Free Cash Flow": free_cash_flow,
        }

        return self.scorecard

    def summary(self):

        print("\nFinancial Scorecard")

        for metric, value in self.scorecard.items():
            print(f"{metric}: {value}")