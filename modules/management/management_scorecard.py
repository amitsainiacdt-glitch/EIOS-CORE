class ManagementScorecard:

    def calculate(
        self,
        capital: dict,
        governance: dict,
        behaviour: dict,
        communication: dict,
    ):

        scores = [
            capital["Score"],
            governance["Score"],
            behaviour["Score"],
            communication["Score"],
        ]

        confidences = [
            capital["Confidence"],
            governance["Confidence"],
            behaviour["Confidence"],
            communication["Confidence"],
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