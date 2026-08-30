"""Human review receipt before governed EIP classification."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PriceRecognitionReviewDecision(str, Enum):
    AUTHORIZE_EIP_REVIEW = "AUTHORIZE_EIP_REVIEW"
    HOLD_FOR_MARKET_DATA = "HOLD_FOR_MARKET_DATA"
    REJECT_RECOGNITION_ASSESSMENT = "REJECT_RECOGNITION_ASSESSMENT"


@dataclass(frozen=True)
class PriceRecognitionReviewReceipt:
    schema_version: int
    review_id: str
    snapshot_id: str
    recognition_fingerprint: str
    decision: PriceRecognitionReviewDecision
    recognition_state: str
    notes: str
    reviewed_at: datetime
    reviewer: str


__all__ = ["PriceRecognitionReviewDecision", "PriceRecognitionReviewReceipt"]
