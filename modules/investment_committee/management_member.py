class ManagementMember:
    """
    Management Committee Member

    Reviews the Management Analysis section of the Master Dossier
    and casts an independent committee vote.
    """

    def __init__(self):
        self.name = "Management Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        management = dossier.management_analysis

        if not management:
            return {
                "Member": "Management",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Weight": 20,
                "Evidence": [],
                "Risks": [],
                "Recommendation": "Management analysis unavailable.",
                "Reason": "Management analysis unavailable."
            }

        score = 0
        evidence = []
        risks = []

        # -----------------------------------
        # Capital Allocation
        # -----------------------------------

        if management.get("Capital Allocation"):
            score += 20
            evidence.append("Good capital allocation")

        else:
            risks.append("Capital allocation unclear")

        # -----------------------------------
        # Governance
        # -----------------------------------

        if management.get("Governance"):
            score += 20
            evidence.append("Good governance")

        else:
            risks.append("Governance concerns")

        # -----------------------------------
        # Promoter Integrity
        # -----------------------------------

        if management.get("Promoter Integrity"):
            score += 20
            evidence.append("Promoter integrity satisfactory")

        else:
            risks.append("Promoter integrity uncertain")

        # -----------------------------------
        # Shareholding
        # -----------------------------------

        if management.get("Shareholding"):
            score += 20
            evidence.append("Healthy promoter holding")

        else:
            risks.append("Shareholding requires monitoring")

        # -----------------------------------
        # Execution
        # -----------------------------------

        if management.get("Execution"):
            score += 20
            evidence.append("Strong execution history")

        else:
            risks.append("Execution record not established")

        # -----------------------------------
        # Final Vote
        # -----------------------------------

        if score >= 85:
            vote = "Pass"

        elif score >= 65:
            vote = "Watch"

        else:
            vote = "Reject"

        return {

            "Member": "Management",

            "Vote": vote,

            "Score": score,

            "Confidence": 85,

            "Weight": 20,

            "Evidence": evidence,

            "Risks": risks,

            "Recommendation":
                f"Management quality score = {score}",

            "Reason":
                f"Management quality score = {score}"
        }