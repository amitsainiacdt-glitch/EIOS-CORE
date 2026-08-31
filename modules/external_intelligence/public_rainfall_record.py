"""Structured observed-rainfall records extracted from a trusted public page."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicRainfallRecord:
    record_id: str
    area: str
    period_label: str
    departure_percent: float
    actual_mm: float
    normal_mm: float
    source_passage: str
    passage_start: int
    passage_end: int
    acquisition_id: str
    document_hash: str
    source_url: str


@dataclass(frozen=True)
class PublicRainfallRecordPreview:
    acquisition_id: str
    extraction_id: str
    period_label: str
    records: tuple[PublicRainfallRecord, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


__all__ = ["PublicRainfallRecord", "PublicRainfallRecordPreview"]
