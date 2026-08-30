"""Passive decision produced before any public document becomes an Observation."""

from dataclasses import dataclass
from enum import Enum


class PublicObservationAdmissionDecision(str, Enum):
    ADMIT = "ADMIT"
    DEFER = "DEFER"
    REJECT = "REJECT"


@dataclass(frozen=True)
class PublicObservationAdmissionPreview:
    decision: PublicObservationAdmissionDecision
    reason_codes: tuple[str, ...]
    acquisition_id: str
    extraction_id: str
    source_id: str | None
    source_quality_tier: str | None
    document_hash: str | None
    extracted_content_fingerprint: str | None
    character_count: int
    duplicate_observation_indexes: tuple[int, ...]
    title: str
    entity: str
    category: str
    confidence: float

    @property
    def admissible(self):
        return self.decision == PublicObservationAdmissionDecision.ADMIT


__all__ = ["PublicObservationAdmissionDecision", "PublicObservationAdmissionPreview"]
