class CompetitiveMember:
    """
    Competitive Intelligence Committee Member

    Reviews competitive positioning, moat, industry dynamics,
    and peer comparison before casting a vote.
    """

    def __init__(self):
        self.name = "Competitive Intelligence Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        competitive = dossier.competitive_intelligence

        if not competitive:
            return {
                "Member": "Competitive",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Weight": 20,
                "Evidence": [],
                "Risks": [],
                "Recommendation": "Competitive analysis unavailable.",
                "Reason": "Competitive analysis unavailable."
            }

        score = 0
        evidence = []
        risks = []

        # -----------------------------------
        # Competitive Moat
        # -----------------------------------

        if competitive.get("Moat"):
            score += 25
            evidence.append("Durable competitive moat")
        else:
            risks.append("Moat not established")

        # -----------------------------------
        # Market Position
        # -----------------------------------

        if competitive.get("Market Position"):
            score += 20
            evidence.append("Strong market position")
        else:
            risks.append("Weak market position")

        # -----------------------------------
        # Competitive Advantage
        # -----------------------------------

        if competitive.get("Competitive Advantage"):
            score += 20
            evidence.append("Clear competitive advantage")
        else:
            risks.append("Competitive advantage unclear")

        # -----------------------------------
        # Switching Cost
        # -----------------------------------

        if competitive.get("Switching Cost"):
            score += 15
            evidence.append("High customer switching cost")
        else:
            risks.append("Low switching cost")

        # -----------------------------------
        # Entry Barrier
        # -----------------------------------

        if competitive.get("Entry Barrier"):
            score += 20
            evidence.append("High barriers to entry")
        else:
            risks.append("Industry easy to enter")

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

            "Member": "Competitive",

            "Vote": vote,

            "Score": score,

            "Confidence": 88,

            "Weight": 20,

            "Evidence": evidence,

            "Risks": risks,

            "Recommendation":
                f"Competitive Position Score = {score}",

            "Reason":
                f"Competitive Position Score = {score}"
        }