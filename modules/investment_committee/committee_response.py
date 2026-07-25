from dataclasses import dataclass, field


@dataclass
class CommitteeResponse:
    """
    Standard response returned by every Investment Committee member.
    Compatible with both the legacy EIOS framework and the new committee
    implementation.
    """

    member: str
    vote: str
    score: int
    confidence: int

    reason: str = ""

    evidence: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    risks: list = field(default_factory=list)

    recommendation: str = ""

    weight: int = 10

    def to_dict(self):

        return {
            "member": self.member,
            "vote": self.vote,
            "score": self.score,
            "confidence": self.confidence,
            "reason": self.reason,
            "evidence": self.evidence,
            "warnings": self.warnings,
            "metrics": self.metrics,
            "risks": self.risks,
            "recommendation": self.recommendation,
            "weight": self.weight,
        }

    @property
    def passed(self):
        return self.vote == "Pass"

    @property
    def watching(self):
        return self.vote == "Watch"

    @property
    def rejected(self):
        return self.vote == "Reject"

    def __str__(self):

        return (
            f"{self.member}: "
            f"{self.vote} "
            f"(Score={self.score}, "
            f"Confidence={self.confidence})"
        )