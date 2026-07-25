from modules.investment_committee.committee_response import CommitteeResponse


class PortfolioMember:
    """
    Portfolio Committee Member

    Evaluates whether the company deserves
    inclusion in the EIOS portfolio.
    """

    def __init__(self):
        self.name = "Portfolio"

    def evaluate(self, research):

        dossier = research.master_dossier

        business = dossier.business_analysis
        financial = dossier.financial_analysis
        valuation = dossier.valuation_analysis

        score = 0
        evidence = []
        risks = []

        # ------------------------------------
        # Business Quality
        # ------------------------------------

        if business:
            score += 30
            evidence.append("Business analysis completed")
        else:
            risks.append("Business analysis missing")

        # ------------------------------------
        # Financial Quality
        # ------------------------------------

        if financial:
            score += 30
            evidence.append("Financial analysis completed")
        else:
            risks.append("Financial analysis missing")

        # ------------------------------------
        # Valuation
        # ------------------------------------

        if valuation:
            score += 40
            evidence.append("Valuation available")
        else:
            risks.append("Valuation not completed")

        # ------------------------------------
        # Final Vote
        # ------------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return CommitteeResponse(
            member="Portfolio",
            vote=vote,
            score=score,
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Portfolio Score = {score}",
            reason=f"Portfolio Score = {score}",
        )