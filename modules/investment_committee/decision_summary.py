from modules.investment_committee.committee_vote_result import (
    CommitteeVoteResult,
)


class DecisionSummary:
    """
    Builds the final Investment Committee decision summary.
    """

    def build(
        self,
        vote_result: CommitteeVoteResult,
        recommendation: dict,
        confidence: dict,
        portfolio_vote: dict,
    ) -> dict:

        return {

            # -----------------------------
            # Committee Decision
            # -----------------------------

            "Overall Vote":
                vote_result.overall_vote,

            "Recommendation":
                recommendation["Recommendation"],

            "Recommendation Reason":
                recommendation["Reason"],

            # -----------------------------
            # Scores
            # -----------------------------

            "Average Score":
                vote_result.average_score,

            "Average Confidence":
                vote_result.average_confidence,

            "Confidence Score":
                confidence["Confidence Score"],

            "Confidence Level":
                confidence["Confidence Level"],

            "Committee Agreement":
                confidence["Committee Agreement"],

            # -----------------------------
            # Voting Statistics
            # -----------------------------

            "Pass Votes":
                vote_result.pass_count,

            "Watch Votes":
                vote_result.watch_count,

            "Reject Votes":
                vote_result.reject_count,

            "Member Votes":
                vote_result.member_votes,

            "Member Scores":
                vote_result.member_scores,

            "Member Confidences":
                vote_result.member_confidences,

            # -----------------------------
            # Portfolio
            # -----------------------------

            "Portfolio Fit":
                portfolio_vote,

        }