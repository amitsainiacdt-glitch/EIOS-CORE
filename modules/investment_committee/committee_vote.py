from collections import Counter

from modules.investment_committee.committee_vote_result import (
    CommitteeVoteResult,
)
from modules.investment_committee.committee_response import (
    CommitteeResponse,
)


class CommitteeVote:
    """
    Aggregates votes from all Investment Committee members.
    """

    def vote(
        self,
        responses: list[CommitteeResponse],
    ) -> CommitteeVoteResult:

        if not responses:
            raise ValueError("No committee responses supplied.")

        member_votes = {}
        member_scores = {}
        member_confidences = {}

        vote_counter = Counter()

        total_score = 0
        total_confidence = 0

        for response in responses:

            member_votes[response.member] = response.vote
            member_scores[response.member] = response.score
            member_confidences[response.member] = response.confidence

            vote_counter[response.vote] += 1

            total_score += response.score
            total_confidence += response.confidence

        total_members = len(responses)

        average_score = round(total_score / total_members, 2)
        average_confidence = round(
            total_confidence / total_members,
            2,
        )

        pass_count = vote_counter["Pass"]
        watch_count = vote_counter["Watch"]
        reject_count = vote_counter["Reject"]

        overall_vote = self._overall_vote(
            pass_count,
            watch_count,
            reject_count,
            total_members,
        )

        return CommitteeVoteResult(
            overall_vote=overall_vote,

            average_score=average_score,
            average_confidence=average_confidence,

            pass_count=pass_count,
            watch_count=watch_count,
            reject_count=reject_count,

            total_members=total_members,

            member_votes=member_votes,
            member_scores=member_scores,
            member_confidences=member_confidences,
        )

    def _overall_vote(
        self,
        pass_count: int,
        watch_count: int,
        reject_count: int,
        total_members: int,
    ) -> str:

        if reject_count >= 3:
            return "Reject"

        if pass_count >= int(total_members * 0.75):
            return "Strong Buy"

        if pass_count > watch_count:
            return "Buy"

        if watch_count >= pass_count:
            return "Watch"

        return "Reject"