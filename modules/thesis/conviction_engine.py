class ConvictionEngine:

    def calculate(
        self,
        thesis,
        assumptions,
        supporting_evidence,
        contradicting_evidence,
        kill_conditions
    ):

        score = 50

        if supporting_evidence:
            score += 20

        if contradicting_evidence:
            score -= 10

        if assumptions:
            score += 10

        status = kill_conditions.get(
            "Overall Status",
            "Active"
        )

        if status != "Active":
            score = 0

        score = max(0, min(100, score))

        return {
            "Conviction Score": score,
            "Rating": self._rating(score),
            "Confidence": 40
        }

    def _rating(self, score):

        if score >= 90:
            return "Very High"

        if score >= 75:
            return "High"

        if score >= 60:
            return "Moderate"

        if score >= 40:
            return "Low"

        return "Very Low"