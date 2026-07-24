from dataclasses import dataclass, field


@dataclass(slots=True)
class CommitteeVoteResult:
    """
    Final aggregated result of the Investment Committee.
    """

    overall_vote: str

    average_score: float
    average_confidence: float

    pass_count: int
    watch_count: int
    reject_count: int

    total_members: int

    member_votes: dict[str, str] = field(default_factory=dict)
    member_scores: dict[str, int] = field(default_factory=dict)
    member_confidences: dict[str, int] = field(default_factory=dict)

    def passed(self) -> bool:
        return self.overall_vote in ("Strong Buy", "Buy")

    def rejected(self) -> bool:
        return self.overall_vote == "Reject"

    def watch(self) -> bool:
        return self.overall_vote == "Watch"