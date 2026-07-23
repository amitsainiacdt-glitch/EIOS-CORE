class RecommendationEngine:

    def recommend(self, committee_vote: dict):

        overall_vote = committee_vote.get(
            "Overall Vote",
            "Watch"
        )

        if overall_vote == "Strong Buy":
            recommendation = "Strong Buy"

        elif overall_vote == "Buy":
            recommendation = "Buy"

        elif overall_vote == "Hold":
            recommendation = "Hold"

        elif overall_vote == "Reduce":
            recommendation = "Reduce"

        elif overall_vote == "Reject":
            recommendation = "Reject"

        else:
            recommendation = "Watch"

        return {
            "Recommendation": recommendation,
            "Confidence": 40
        }