class ConfidenceEngine:

    def calculate(
        self,
        committee_vote,
        recommendation
    ):

        score = 50

        overall_vote = committee_vote.get(
            "Overall Vote",
            "Watch"
        )

        if overall_vote == "Strong Buy":
            score = 95

        elif overall_vote == "Buy":
            score = 85

        elif overall_vote == "Hold":
            score = 70

        elif overall_vote == "Reduce":
            score = 50

        elif overall_vote == "Reject":
            score = 30

        else:
            score = 60

        return {
            "Confidence Score": score,
            "Confidence Level": self._level(score),
            "Confidence": 40
        }

    def _level(self, score):

        if score >= 90:
            return "Very High"

        if score >= 75:
            return "High"

        if score >= 60:
            return "Moderate"

        if score >= 40:
            return "Low"

        return "Very Low"