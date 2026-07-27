class RiskScorecard:

    def calculate(
        self,
        business,
        financial,
        governance,
        industry,
        macro,
        scenario,
    ):

        scores = [
            business["Score"],
            financial["Score"],
            governance["Score"],
            industry["Score"],
            macro["Score"],
            scenario["Score"],
        ]

        confidences = [
            business["Confidence"],
            financial["Confidence"],
            governance["Confidence"],
            industry["Confidence"],
            macro["Confidence"],
            scenario["Confidence"],
        ]

        raw_score = round(sum(scores) / len(scores), 2)

        confidence = round(
            sum(confidences) / len(confidences),
            2,
        )

        return {
            "Raw Score": raw_score,
            "Max Score": 100,
            "Confidence": confidence,
        }