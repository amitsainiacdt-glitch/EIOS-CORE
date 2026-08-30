"""Human review receipt for a stored governed Pre-Inflection preview."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PreInflectionReviewDecision(str, Enum):
    AUTHORIZE_PRICE_RECOGNITION_REVIEW = "AUTHORIZE_PRICE_RECOGNITION_REVIEW"
    HOLD_FOR_RESEARCH = "HOLD_FOR_RESEARCH"
    REJECT_ASSESSMENT = "REJECT_ASSESSMENT"


@dataclass(frozen=True)
class PreInflectionReviewReceipt:
    schema_version: int
    review_id: str
    preview_id: str
    preview_fingerprint: str
    decision: PreInflectionReviewDecision
    notes: str
    reviewed_at: datetime
    reviewer: str


__all__ = ["PreInflectionReviewDecision", "PreInflectionReviewReceipt"]
