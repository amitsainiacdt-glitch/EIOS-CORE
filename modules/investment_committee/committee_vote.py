from collections import Counter


class CommitteeVote:
    """
    Final Investment Committee Decision

    Aggregates committee member responses into a
    single committee recommendation.
    """

    def __init__(self, responses):

        self.responses = responses

        self.member_votes = {
            response.member: response.vote
            for response in responses
        }

        self.average_score = (
            sum(r.score for r in responses) / len(responses)
            if responses else 0
        )

        self.average_confidence = (
            sum(r.confidence for r in responses) / len(responses)
            if responses else 0
        )

        vote_counter = Counter(r.vote for r in responses)

        if vote_counter:
            self.final_vote = vote_counter.most_common(1)[0][0]
        else:
            self.final_vote = "Watch"

    @property
    def passed(self):
        return self.final_vote == "Pass"

    def to_dict(self):

        return {
            "Final Vote": self.final_vote,
            "Average Score": round(self.average_score, 1),
            "Average Confidence": round(self.average_confidence, 1),
            "Member Votes": self.member_votes,
        }

    def __str__(self):

        return (
            "\n"
            "Investment Committee Summary\n"
            "----------------------------\n"
            f"Final Vote          : {self.final_vote}\n"
            f"Average Score       : {self.average_score:.1f}\n"
            f"Average Confidence  : {self.average_confidence:.1f}\n"
        )