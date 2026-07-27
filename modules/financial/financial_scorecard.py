"""
Financial Scorecard

Evaluates the financial strength of a company using configurable
rules defined in financial_rules.py.
"""

from modules.financial.financial_rules import FINANCIAL_RULES


class FinancialScorecard:

    def __init__(self):
        self.metrics = {}
        self.component_scores = {}
        self.total_score = 0
        self.max_score = 0

    def evaluate(
        self,
        revenue_growth,
        eps_growth,
        roce,
        roe,
        debt_to_equity,
        free_cash_flow,
    ):

        self.metrics = {
            "Revenue Growth": revenue_growth,
            "EPS Growth": eps_growth,
            "ROCE": roce,
            "ROE": roe,
            "Debt to Equity": debt_to_equity,
            "Free Cash Flow": free_cash_flow,
        }

        self.component_scores = {}
        self.total_score = 0
        self.max_score = 0

        for metric, value in self.metrics.items():

            rule = FINANCIAL_RULES[metric]

            score = self._calculate_metric_score(
                value=value,
                thresholds=rule["thresholds"],
                reverse=rule.get("reverse", False),
            )

            self.component_scores[metric] = score
            self.total_score += score
            self.max_score += rule["weight"]

        return {
            "Metrics": self.metrics,
            "Component Scores": self.component_scores,
            "Total Score": self.total_score,
            "Max Score": self.max_score,
        }

    def _calculate_metric_score(
        self,
        value,
        thresholds,
        reverse=False,
    ):
        """
        Evaluate one metric.

        reverse=False
            Higher values are better.

        reverse=True
            Lower values are better.
        """

        if reverse:

            thresholds = sorted(
                thresholds,
                key=lambda x: x[0],
            )

            for limit, score in thresholds:
                if value <= limit:
                    return score

            return 0

        thresholds = sorted(
            thresholds,
            key=lambda x: x[0],
            reverse=True,
        )

        for limit, score in thresholds:
            if value >= limit:
                return score

        return 0

    def summary(self):

        print("\nFinancial Scorecard")
        print("-" * 40)

        for metric in self.metrics:

            print(
                f"{metric:<25}"
                f"{self.metrics[metric]:>10}"
                f"   Score: {self.component_scores[metric]}"
            )

        print("-" * 40)
        print(f"Total Score : {self.total_score}/{self.max_score}")