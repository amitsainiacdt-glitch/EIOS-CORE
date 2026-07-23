class ManagementScorecard:

    def calculate(
        self,
        capital: dict,
        governance: dict,
        behaviour: dict,
        communication: dict
    ):

        scores = [
            capital["Score"],
            governance["Score"],
            behaviour["Score"],
            communication["Score"]
        ]

        confidence = [
            capital["Confidence"],
            governance["Confidence"],
            behaviour["Confidence"],
            communication["Confidence"]
        ]

        overall_score = round(sum(scores) / len(scores), 2)
        overall_confidence = round(sum(confidence) / len(confidence), 2)

        return {
            "Overall Score": overall_score,
            "Confidence": overall_confidence,
            "Rating": self._rating(overall_score)
        }

    def _rating(self, score):

        if score >= 90:
            return "Excellent"

        elif score >= 80:
            return "Good"

        elif score >= 70:
            return "Average"

        else:
            return "Weak"