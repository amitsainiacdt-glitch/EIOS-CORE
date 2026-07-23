class ThesisMember:
    """
    Thesis Committee Member

    Reviews the complete investment thesis and determines
    whether the evidence supports long-term investment.
    """

    def __init__(self):
        self.name = "Thesis Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        thesis = dossier.investment_thesis

        if not thesis:
            return {
                "Member": "Thesis",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Weight": 25,
                "Evidence": [],
                "Risks": [],
                "Recommendation": "Investment thesis unavailable.",
                "Reason": "Investment thesis unavailable."
            }

        score = 0
        evidence = []
        risks = []

        # -----------------------------------
        # Thesis Clarity
        # -----------------------------------

        if thesis.get("Core Thesis"):
            score += 20
            evidence.append("Clear investment thesis")
        else:
            risks.append("Investment thesis not clearly defined")

        # -----------------------------------
        # Growth Drivers
        # -----------------------------------

        if thesis.get("Growth Drivers"):
            score += 20
            evidence.append("Long-term growth drivers identified")
        else:
            risks.append("Growth drivers weak or missing")

        # -----------------------------------
        # Competitive Advantage
        # -----------------------------------

        if thesis.get("Competitive Advantage"):
            score += 20
            evidence.append("Competitive advantage supports thesis")
        else:
            risks.append("Competitive advantage not convincing")

        # -----------------------------------
        # Key Risks
        # -----------------------------------

        thesis_risks = thesis.get("Key Risks", [])

        if len(thesis_risks) <= 3:
            score += 20
            evidence.append("Risks appear manageable")
        else:
            score += 10
            risks.append("Multiple risks could weaken thesis")

        # -----------------------------------
        # Kill Switch
        # -----------------------------------

        if thesis.get("Kill Switch"):
            score += 20
            evidence.append("Thesis invalidation criteria defined")
        else:
            risks.append("No clear thesis invalidation criteria")

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

            "Member": "Thesis",

            "Vote": vote,

            "Score": score,

            "Confidence": 92,

            "Weight": 25,

            "Evidence": evidence,

            "Risks": risks,

            "Recommendation":
                f"Investment Thesis Score = {score}",

            "Reason":
                f"Investment Thesis Score = {score}"
        }