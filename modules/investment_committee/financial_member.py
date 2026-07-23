class FinancialMember:
    """
    Financial Committee Member

    Reviews the Financial Analysis section of the Master Dossier
    and casts an independent committee vote.
    """

    def __init__(self):
        self.name = "Financial Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        financial = dossier.financial_analysis

        if not financial:
            return {
                "Member": "Financial",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Reason": "Financial Analysis not available."
            }

        score = 0
        evidence = []
        risks = []

        # -----------------------------
        # Revenue Growth
        # -----------------------------
        if financial.get("Revenue Growth"):
            score += 20
            evidence.append("Consistent revenue growth")
        else:
            risks.append("Revenue growth not established")

        # -----------------------------
        # Profit Growth
        # -----------------------------
        if financial.get("Profit Growth"):
            score += 20
            evidence.append("Healthy profit growth")
        else:
            risks.append("Weak profit growth")

        # -----------------------------
        # ROCE
        # -----------------------------
        if financial.get("ROCE"):
            score += 20
            evidence.append("Strong ROCE")
        else:
            risks.append("ROCE not satisfactory")

        # -----------------------------
        # Free Cash Flow
        # -----------------------------
        if financial.get("Free Cash Flow"):
            score += 20
            evidence.append("Positive free cash flow")
        else:
            risks.append("Weak free cash flow")

        # -----------------------------
        # Debt
        # -----------------------------
        if financial.get("Debt"):
            score += 20
            evidence.append("Comfortable debt profile")
        else:
            risks.append("Debt needs monitoring")

        # -----------------------------
        # Final Vote
        # -----------------------------
        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return {
            "Member": "Financial",
            "Vote": vote,
            "Score": score,
            "Confidence": 85,
            "Weight": 20,
            "Evidence": evidence,
            "Risks": risks,
            "Recommendation": f"Financial quality score = {score}",
            "Reason": f"Financial quality score = {score}"
        }