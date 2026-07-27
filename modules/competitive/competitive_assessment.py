"""
EIOS
Everest Investment Operating System

Competitive Assessment Engine

Converts peer benchmarking results into an institutional
0-100 competitive strength score.
"""


class CompetitiveAssessmentEngine:
    """
    Evaluates the competitive strength of the researched
    company relative to its peers.
    """

    MAX_SCORE = 100
    CONFIDENCE = 85

    def evaluate(self, ranked_peers):

        if not ranked_peers:
            return {
                "Component Scores": {},
                "Total Score": 0,
                "Max Score": self.MAX_SCORE,
                "Confidence": self.CONFIDENCE,
            }

        company = ranked_peers[0]

        scores = {

            "Market Leadership":
                self._market_leadership(company),

            "Capital Efficiency":
                self._capital_efficiency(company),

            "Growth Leadership":
                self._growth(company),

            "Profitability":
                self._profitability(company),

            "Balance Sheet":
                self._balance_sheet(company),

            "Moat":
                self._moat(company),
        }

        total = sum(scores.values())

        return {

            "Component Scores": scores,

            "Total Score": total,

            "Max Score": self.MAX_SCORE,

            "Confidence": self.CONFIDENCE,
        }

    # -------------------------------------------------
    # Individual Assessment Areas
    # -------------------------------------------------

    def _market_leadership(self, company):

        if company.get("Rank", 99) == 1:
            return 15

        if company.get("Rank", 99) <= 3:
            return 10

        return 5

    def _capital_efficiency(self, company):

        roiic = company.get("ROIIC", 0)

        if roiic >= 25:
            return 20

        if roiic >= 20:
            return 17

        if roiic >= 15:
            return 14

        return 8

    def _growth(self, company):

        revenue = company.get("Revenue Growth", 0)
        eps = company.get("EPS Growth", 0)

        score = 0

        if revenue >= 20:
            score += 8
        elif revenue >= 15:
            score += 6
        else:
            score += 4

        if eps >= 25:
            score += 7
        elif eps >= 20:
            score += 5
        else:
            score += 3

        return score

    def _profitability(self, company):

        roce = company.get("ROCE", 0)

        if roce >= 25:
            return 15

        if roce >= 20:
            return 12

        if roce >= 15:
            return 9

        return 5

    def _balance_sheet(self, company):

        debt = company.get("Debt to Equity", 1)

        if debt <= 0.20:
            return 10

        if debt <= 0.50:
            return 8

        if debt <= 1.00:
            return 5

        return 2

    def _moat(self, company):

        margin = company.get("Operating Margin", 0)

        if margin >= 20:
            return 25

        if margin >= 15:
            return 20

        if margin >= 10:
            return 15

        return 10