"""Append-only human review of stored mandatory Meta assessments."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MandatoryMetaReviewDecision(str, Enum):
    AUTHORIZE_PRE_INFLECTION_REVIEW = "AUTHORIZE_PRE_INFLECTION_REVIEW"
    HOLD_FOR_RESEARCH = "HOLD_FOR_RESEARCH"
    REJECT_ASSESSMENT = "REJECT_ASSESSMENT"


@dataclass(frozen=True)
class MandatoryMetaReviewReceipt:
    schema_version: int
    review_id: str
    assessment_id: str
    assessment_fingerprint: str
    decision: MandatoryMetaReviewDecision
    gate_decision: str
    gate_reason_codes: tuple[str, ...]
    notes: str
    reviewed_at: datetime
    reviewer: str


__all__ = ["MandatoryMetaReviewDecision", "MandatoryMetaReviewReceipt"]
