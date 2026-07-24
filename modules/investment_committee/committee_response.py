from dataclasses import dataclass, field


@dataclass(slots=True)
class CommitteeResponse:
    """
    Standard response returned by every
    Investment Committee member.
    """

    member: str
    vote: str
    score: int
    confidence: int
    reason: str

    evidence: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def to_dict(self) -> dict:

        return {
            "Member": self.member,
            "Vote": self.vote,
            "Score": self.score,
            "Confidence": self.confidence,
            "Reason": self.reason,
            "Evidence": self.evidence,
            "Warnings": self.warnings,
            "Metrics": self.metrics,
        }