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

        if not financial:
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

        revenue_growth = financial.get("Revenue Growth", 0)
        roce = financial.get("ROCE", 0)
        roe = financial.get("ROE", 0)
        debt = financial.get("Debt to Equity", 999)

        if revenue_growth >= 15:
            score += 25
            evidence.append("Strong revenue growth")
        else:
            risks.append("Weak revenue growth")

        if roce >= 20:
            score += 25
            evidence.append("High ROCE")
        else:
            risks.append("ROCE below target")

        if roe >= 18:
            score += 25
            evidence.append("Healthy ROE")
        else:
            risks.append("ROE below target")

        if debt <= 0.5:
            score += 25
            evidence.append("Low leverage")
        else:
            risks.append("High leverage")

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return CommitteeResponse(
            member="Financial",
            vote=vote,
            score=score,
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Financial Score = {score}",
            reason=f"Financial Score = {score}",
        )