class BusinessMember:
    """
    Business Committee Member

    Evaluates overall business quality before casting
    the committee vote.
    """

    def evaluate(self, research):

        dossier = research.master_dossier

        business = dossier.business_quality

        if not business:
            return {
                "Member": "Business",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Reason":
                    "Business Quality analysis unavailable."
            }

        score = 50

        if business.get("Business Model"):
            score += 10

        if business.get("Moat"):
            score += 15

        if business.get("Growth Drivers"):
            score += 10

        if business.get("Market Size"):
            score += 10

        risks = business.get("Key Risks", [])

        if len(risks) <= 2:
            score += 5

        if score >= 80:
            vote = "Pass"

        elif score >= 60:
            vote = "Watch"

        else:
            vote = "Reject"

        return {

            "Member": "Business",

            "Vote": vote,

            "Score": score,

            "Confidence": 80,

            "Reason":
                f"Business quality score = {score}"
        }