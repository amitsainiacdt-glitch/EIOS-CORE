class RiskMember:
    """
    Risk Committee Member

    Reviews the Risk Analysis section of the Master Dossier
    and evaluates downside risk.
    """

    def __init__(self):
        self.name = "Risk Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        risk = dossier.risk_analysis

        if not risk:
            return {
                "Member": "Risk",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Weight": 20,
                "Evidence": [],
                "Risks": [],
                "Recommendation": "Risk analysis unavailable.",
                "Reason": "Risk analysis unavailable."
            }

        score = 100
        evidence = []
        risks = []

        # -----------------------------------
        # Business Risk
        # -----------------------------------

        if risk.get("Business Risk"):
            score -= 10
            risks.append("Business execution risk identified")
        else:
            evidence.append("Business risk appears manageable")

        # -----------------------------------
        # Financial Risk
        # -----------------------------------

        if risk.get("Financial Risk"):
            score -= 15
            risks.append("Financial risk detected")
        else:
            evidence.append("Financial risk appears low")

        # -----------------------------------
        # Governance Risk
        # -----------------------------------

        if risk.get("Governance Risk"):
            score -= 20
            risks.append("Governance concern identified")
        else:
            evidence.append("Governance appears satisfactory")

        # -----------------------------------
        # Industry Risk
        # -----------------------------------

        if risk.get("Industry Risk"):
            score -= 15
            risks.append("Industry headwinds present")
        else:
            evidence.append("Industry outlook acceptable")

        # -----------------------------------
        # Regulatory Risk
        # -----------------------------------

        if risk.get("Regulatory Risk"):
            score -= 20
            risks.append("Regulatory uncertainty")
        else:
            evidence.append("Regulatory environment stable")

        # -----------------------------------
        # Balance Score
        # -----------------------------------

        score = max(score, 0)

        if score >= 85:
            vote = "Pass"

        elif score >= 65:
            vote = "Watch"

        else:
            vote = "Reject"

        return {

            "Member": "Risk",

            "Vote": vote,

            "Score": score,

            "Confidence": 90,

            "Weight": 20,

            "Evidence": evidence,

            "Risks": risks,

            "Recommendation":
                f"Overall Risk Score = {score}",

            "Reason":
                f"Overall Risk Score = {score}"
        }