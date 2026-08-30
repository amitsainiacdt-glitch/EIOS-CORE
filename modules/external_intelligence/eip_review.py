"""Final human review receipt before existing downstream Evidence governance."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EIPReviewDecision(str, Enum):
    AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW = "AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW"
    HOLD_EIP_RESEARCH = "HOLD_EIP_RESEARCH"
    REJECT_EIP_CLASSIFICATION = "REJECT_EIP_CLASSIFICATION"


@dataclass(frozen=True)
class EIPReviewReceipt:
    schema_version: int
    review_id: str
    classification_id: str
    classification_fingerprint: str
    stage: str
    decision: EIPReviewDecision
    notes: str
    reviewed_at: datetime
    reviewer: str


__all__ = ["EIPReviewDecision", "EIPReviewReceipt"]
