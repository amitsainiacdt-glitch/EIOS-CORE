class RiskScorecard:

    def calculate(
        self,
        business,
        financial,
        governance,
        industry,
        macro,
        scenario
    ):

        scores = [
            business["Score"],
            financial["Score"],
            governance["Score"],
            industry["Score"],
            macro["Score"],
            scenario["Score"]
        ]

        confidence = [
            business["Confidence"],
            financial["Confidence"],
            governance["Confidence"],
            industry["Confidence"],
            macro["Confidence"],
            scenario["Confidence"]
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
            return "Very Low Risk"

        elif score >= 80:
            return "Low Risk"

        elif score >= 70:
            return "Moderate Risk"

        elif score >= 60:
            return "High Risk"

        else:
            return "Very High Risk"