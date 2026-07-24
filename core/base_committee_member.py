"""
EIOS
Everest Investment Operating System

Base Committee Member
"""

from abc import ABC, abstractmethod

from modules.investment_committee.committee_response import CommitteeResponse


class BaseCommitteeMember(ABC):
    """
    Base class for all Investment Committee members.
    """

    MEMBER = "Unknown"

    PASS_THRESHOLD = 80
    WATCH_THRESHOLD = 60

    @abstractmethod
    def evaluate(self, research) -> CommitteeResponse:
        """
        Evaluate the assigned investment domain.
        """
        raise NotImplementedError

    def calculate_vote(self, score: int) -> str:

        self.validate_score(score)

        if score >= self.PASS_THRESHOLD:
            return "Pass"

        if score >= self.WATCH_THRESHOLD:
            return "Watch"

        return "Reject"

    def validate_score(self, score):

        if not isinstance(score, (int, float)):
            raise TypeError("Score must be numeric.")

        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100.")

    def validate_confidence(self, confidence):

        if not isinstance(confidence, (int, float)):
            raise TypeError("Confidence must be numeric.")

        if confidence < 0 or confidence > 100:
            raise ValueError("Confidence must be between 0 and 100.")

    def build_response(
        self,
        *,
        score,
        confidence,
        reason,
        evidence=None,
        warnings=None,
        metrics=None,
    ) -> CommitteeResponse:

        self.validate_score(score)
        self.validate_confidence(confidence)

        return CommitteeResponse(
            member=self.MEMBER,
            vote=self.calculate_vote(score),
            score=int(score),
            confidence=int(confidence),
            reason=reason,
            evidence=evidence or [],
            warnings=warnings or [],
            metrics=metrics or {},
        )