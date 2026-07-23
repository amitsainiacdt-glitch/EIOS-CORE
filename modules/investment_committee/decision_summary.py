class DecisionSummary:

    def build(
        self,
        committee_vote,
        recommendation,
        confidence,
        portfolio_fit
    ):

        return {
            "Committee Vote":
                committee_vote,

            "Recommendation":
                recommendation,

            "Confidence":
                confidence,

            "Portfolio Fit":
                portfolio_fit,

            "Decision":
                recommendation["Recommendation"],

            "Confidence Score":
                confidence["Confidence Score"],

            "Confidence Level":
                confidence["Confidence Level"],

            "Position Size":
                portfolio_fit["Position Size"],

            "Portfolio Priority":
                portfolio_fit["Portfolio Priority"]
        }