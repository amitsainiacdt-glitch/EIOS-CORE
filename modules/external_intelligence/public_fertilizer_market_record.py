"""Structured fertilizer requirement, availability, sale, and stock records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicFertilizerMarketRecord:
    record_id: str
    product: str
    period_label: str
    unit: str
    requirement: float
    availability: float
    dbt_sales: float
    closing_stock: float
    source_row: str
    acquisition_id: str
    document_hash: str
    source_url: str


@dataclass(frozen=True)
class PublicFertilizerMarketPreview:
    acquisition_id: str
    extraction_id: str
    period_label: str
    records: tuple[PublicFertilizerMarketRecord, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


__all__ = ["PublicFertilizerMarketRecord", "PublicFertilizerMarketPreview"]
