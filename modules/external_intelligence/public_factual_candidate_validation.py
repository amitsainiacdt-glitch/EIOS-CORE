"""Passive validation decision for one source-grounded factual candidate."""

from dataclasses import dataclass
from enum import Enum


class PublicFactualCandidateValidationDecision(str, Enum):
    VALIDATED = "VALIDATED"
    DEFER = "DEFER"
    REJECT = "REJECT"


@dataclass(frozen=True)
class PublicFactualCandidateValidation:
    candidate_id: str
    decision: PublicFactualCandidateValidationDecision
    reason_codes: tuple[str, ...]
    event_type: str
    statement_posture: str
    subject_grounded: bool
    event_mechanics_grounded: bool
    requires_corroboration: bool
    source_passage: str
    document_hash: str
    extracted_content_fingerprint: str

    @property
    def validated(self):
        return self.decision == PublicFactualCandidateValidationDecision.VALIDATED


__all__ = ["PublicFactualCandidateValidation", "PublicFactualCandidateValidationDecision"]
