"""Plain-language labels mapped from governed internal EIP states."""

from dataclasses import dataclass
from enum import Enum


class ReaderEIPClassification(str, Enum):
    RESEARCH_NOW = "RESEARCH_NOW"
    EARLY_WATCH = "EARLY_WATCH"
    EARLIEST_INVESTABLE_POINT = "EARLIEST_INVESTABLE_POINT"
    BUY_ZONE_CANDIDATE = "BUY_ZONE_CANDIDATE"
    WAIT = "WAIT"
    TOO_LATE = "TOO_LATE"
    REJECT = "REJECT"


@dataclass(frozen=True)
class ReaderEIPClassificationResult:
    packet_id: str
    packet_fingerprint: str
    classification: ReaderEIPClassification
    internal_eip_stage: str | None
    headline: str
    explanation: str
    reason_codes: tuple[str, ...]
    creates_investment_decision: bool
    non_authority_statement: str


__all__ = ["ReaderEIPClassification", "ReaderEIPClassificationResult"]
