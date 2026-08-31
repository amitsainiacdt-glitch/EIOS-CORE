"""Structured official daily food-price comparison records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicFoodPriceComparisonRecord:
    record_id: str
    market_level: str
    commodity: str
    reporting_date: str
    unit: str
    current_price: float
    week_price: float | None
    week_change_percent: float | None
    month_price: float | None
    month_change_percent: float | None
    six_month_price: float | None
    six_month_change_percent: float | None
    year_price: float | None
    year_change_percent: float | None
    two_year_price: float | None
    two_year_change_percent: float | None
    source_row: tuple[str, ...]
    acquisition_id: str
    document_hash: str
    source_url: str


@dataclass(frozen=True)
class PublicFoodPriceComparisonPreview:
    acquisition_id: str
    extraction_id: str
    records: tuple[PublicFoodPriceComparisonRecord, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


__all__ = ["PublicFoodPriceComparisonRecord", "PublicFoodPriceComparisonPreview"]
