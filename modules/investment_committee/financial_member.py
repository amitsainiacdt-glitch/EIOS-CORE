from modules.investment_committee.committee_response import CommitteeResponse


class FinancialMember:
    """
    Financial Committee Member

    Reviews the financial quality of the business.
    """

    def __init__(self):
        self.name = "Financial"

    def evaluate(self, research):

        dossier = research.master_dossier
        financial = dossier.financial_analysis

        if financial is None:
            return CommitteeResponse(
                member="Financial",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Financial analysis unavailable"],
                recommendation="Complete financial analysis first.",
                reason="Financial analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # ---------------------------------------------------------
        # Read FinancialSection attributes
        # ---------------------------------------------------------

        revenue_growth = financial.revenue_growth
        roce = financial.roce
        roe = financial.roe
        debt = financial.debt_to_equity

        # ---------------------------------------------------------
        # Revenue Growth
        # ---------------------------------------------------------

        if revenue_growth >= 15:
            score += 25
            evidence.append(
                f"Strong revenue growth ({revenue_growth:.2f}%)"
            )
        else:
            risks.append(
                f"Weak revenue growth ({revenue_growth:.2f}%)"
            )

        # ---------------------------------------------------------
        # ROCE
        # ---------------------------------------------------------

        if roce >= 20:
            score += 25
            evidence.append(
                f"High ROCE ({roce:.2f}%)"
            )
        else:
            risks.append(
                f"ROCE below target ({roce:.2f}%)"
            )

        # ---------------------------------------------------------
        # ROE
        # ---------------------------------------------------------

        if roe >= 18:
            score += 25
            evidence.append(
                f"Healthy ROE ({roe:.2f}%)"
            )
        else:
            risks.append(
                f"ROE below target ({roe:.2f}%)"
            )

        # ---------------------------------------------------------
        # Debt
        # ---------------------------------------------------------

        if debt <= 0.50:
            score += 25
            evidence.append(
                f"Low leverage (D/E {debt:.2f})"
            )
        else:
            risks.append(
                f"High leverage (D/E {debt:.2f})"
            )

        # ---------------------------------------------------------
        # Vote
        # ---------------------------------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        confidence = min(100, score + 10)

        return CommitteeResponse(
            member="Financial",
            vote=vote,
            score=score,
            confidence=confidence,
            evidence=evidence,
            risks=risks,
            recommendation=f"Financial Score = {score}",
            reason=f"Revenue Growth={revenue_growth:.2f}%, ROCE={roce:.2f}%, ROE={roe:.2f}%, Debt/Equity={debt:.2f}",
        )