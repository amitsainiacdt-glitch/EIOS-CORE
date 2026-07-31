from modules.investment_committee.committee_response import CommitteeResponse


class ThesisMember:
    """
    Investment Thesis Committee Member
    """

    def __init__(self):
        self.name = "Thesis"

    def evaluate(self, research):

        dossier = research.master_dossier

        score = 0
        evidence = []
        risks = []

        # --------------------------------------------------
        # Business Quality
        # --------------------------------------------------

        if dossier.business:
            score += 25
            evidence.append("Business quality analysis completed")
        else:
            risks.append("Business quality unavailable")

        # --------------------------------------------------
        # Financial Analysis
        # --------------------------------------------------

        if dossier.financial:
            score += 20
            evidence.append("Financial analysis completed")
        else:
            risks.append("Financial analysis unavailable")

        # --------------------------------------------------
        # Valuation
        # --------------------------------------------------

        if dossier.valuation:
            score += 20
            evidence.append("Valuation completed")
        else:
            risks.append("Valuation unavailable")

        # --------------------------------------------------
        # Management
        # --------------------------------------------------

        if dossier.management:
            score += 15
            evidence.append("Management analysis completed")
        else:
            risks.append("Management analysis unavailable")

        # --------------------------------------------------
        # Risk
        # --------------------------------------------------

        if dossier.risk:
            score += 10
            evidence.append("Risk analysis completed")
        else:
            risks.append("Risk analysis unavailable")

        # --------------------------------------------------
        # Competitive
        # --------------------------------------------------

        if dossier.competitive:
            score += 10
            evidence.append("Competitive analysis completed")
        else:
            risks.append("Competitive analysis unavailable")

        # --------------------------------------------------
        # Vote
        # --------------------------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        confidence = min(score + 10, 100)

        return CommitteeResponse(
            member="Thesis",
            vote=vote,
            score=score,
            confidence=confidence,
            evidence=evidence,
            risks=risks,
            recommendation=f"Overall Thesis Score = {score}",
            reason="Investment thesis generated from completed research modules.",
        )