from modules.investment_committee.committee_response import CommitteeResponse


class RiskMember:
    """
    Risk Committee Member

    Evaluates business, financial, governance,
    industry and macro risks.
    """

    def __init__(self):
        self.name = "Risk"

    def evaluate(self, research):

        dossier = research.master_dossier
        risk = dossier.risk_analysis

        if not risk:
            return CommitteeResponse(
                member="Risk",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Risk analysis unavailable"],
                recommendation="Complete risk analysis first.",
                reason="Risk analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # ------------------------------------
        # Overall Risk
        # ------------------------------------

        overall = risk.get("Overall Risk", {})
        overall_score = overall.get("Overall Score", 0)

        if overall_score >= 85:
            score += 40
            evidence.append("Overall risk profile is excellent")
        elif overall_score >= 75:
            score += 30
            evidence.append("Risk profile is acceptable")
        else:
            risks.append("Overall risk profile is weak")

        # ------------------------------------
        # Financial Risk
        # ------------------------------------

        financial = risk.get("Financial Risk", {})
        if financial.get("Score", 0) >= 80:
            score += 20
            evidence.append("Financial risk is low")
        else:
            risks.append("Financial risk requires monitoring")

        # ------------------------------------
        # Governance Risk
        # ------------------------------------

        governance = risk.get("Governance Risk", {})
        if governance.get("Score", 0) >= 80:
            score += 20
            evidence.append("Governance risk is low")
        else:
            risks.append("Governance concerns")

        # ------------------------------------
        # Industry Risk
        # ------------------------------------

        industry = risk.get("Industry Risk", {})
        if industry.get("Score", 0) >= 80:
            score += 20
            evidence.append("Industry risk acceptable")
        else:
            risks.append("Industry risk elevated")

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
            member="Risk",
            vote=vote,
            score=score,
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Risk Score = {score}",
            reason=f"Risk Score = {score}",
        )