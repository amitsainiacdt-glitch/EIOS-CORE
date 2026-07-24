from modules.investment_committee.committee_vote_result import (
    CommitteeVoteResult,
)


class ConfidenceEngine:
    """
    Calculates overall confidence in the committee's
    recommendation based on voting consensus and
    average member confidence.
    """

    def calculate(
        self,
        vote_result: CommitteeVoteResult,
        recommendation: dict,
    ) -> dict:

        agreement = max(
            vote_result.pass_count,
            vote_result.watch_count,
            vote_result.reject_count,
        ) / vote_result.total_members

        consensus_bonus = agreement * 10

        confidence_score = min(
            100,
            round(
                vote_result.average_confidence +
                consensus_bonus
            ),
        )

        return {
            "Confidence Score": confidence_score,
            "Confidence Level": self._level(confidence_score),
            "Committee Agreement": round(
                agreement * 100,
                2,
            ),
            "Average Confidence":
                vote_result.average_confidence,
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