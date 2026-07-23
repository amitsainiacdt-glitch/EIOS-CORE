class CommitteeVote:

    def vote(self, committee_data: dict):

        return {
            "Business Quality":
                committee_data.get(
                    "business_quality",
                    "Watch"
                ),

            "Financial Quality":
                committee_data.get(
                    "financial_quality",
                    "Watch"
                ),

            "Management":
                committee_data.get(
                    "management",
                    "Watch"
                ),

            "Risk":
                committee_data.get(
                    "risk",
                    "Watch"
                ),

            "Competitive Position":
                committee_data.get(
                    "competitive_position",
                    "Watch"
                ),

            "Valuation":
                committee_data.get(
                    "valuation",
                    "Watch"
                ),

            "Investment Thesis":
                committee_data.get(
                    "investment_thesis",
                    "Watch"
                ),

            "Overall Vote":
                committee_data.get(
                    "overall_vote",
                    "Watch"
                ),

            "Confidence":
                40
        }