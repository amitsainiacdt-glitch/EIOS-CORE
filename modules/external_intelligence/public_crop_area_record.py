"""Structured crop-area records from an official public release."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicCropAreaRecord:
    record_id: str
    crop: str
    period_label: str
    unit: str
    normal_area: float
    current_area: float
    prior_year_area: float
    difference_from_prior_year: float
    source_row: str
    acquisition_id: str
    document_hash: str
    source_url: str


@dataclass(frozen=True)
class PublicCropAreaPreview:
    acquisition_id: str
    extraction_id: str
    period_label: str
    records: tuple[PublicCropAreaRecord, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


__all__ = ["PublicCropAreaRecord", "PublicCropAreaPreview"]
