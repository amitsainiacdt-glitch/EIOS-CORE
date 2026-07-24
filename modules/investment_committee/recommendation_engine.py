from modules.investment_committee.committee_vote_result import (
    CommitteeVoteResult,
)


class RecommendationEngine:
    """
    Converts the Investment Committee vote into
    the final investment recommendation.
    """

    def recommend(
        self,
        vote_result: CommitteeVoteResult,
    ) -> dict:

        overall_vote = vote_result.overall_vote

        if overall_vote == "Strong Buy":

            recommendation = "Strong Buy"

            rationale = (
                "Strong committee consensus with high conviction."
            )

        elif overall_vote == "Buy":

            recommendation = "Buy"

            rationale = (
                "Positive committee consensus."
            )

        elif overall_vote == "Watch":

            recommendation = "Watch"

            rationale = (
                "Business requires further monitoring."
            )

        else:

            recommendation = "Reject"

            rationale = (
                "Committee identified unacceptable risks."
            )

        return {
            "Recommendation": recommendation,
            "Reason": rationale,
            "Average Score": vote_result.average_score,
            "Average Confidence": vote_result.average_confidence,
            "Overall Vote": vote_result.overall_vote,
        }