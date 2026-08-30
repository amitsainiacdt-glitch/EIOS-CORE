"""Passive public-market snapshot and governed recognition preview."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass(frozen=True)
class PublicMarketRecognitionSnapshot:
    schema_version: int
    snapshot_id: str
    entity: str
    observed_at: datetime
    public_information_only: bool
    source_ids: tuple[str, ...]
    anchor_price: float
    current_price: float
    return_1m_pct: float | None
    return_3m_pct: float | None
    return_6m_pct: float | None
    return_12m_pct: float | None
    sector_relative_return_pct: float | None
    week_52_low: float | None
    week_52_high: float | None
    abnormal_volume_ratio: float | None
    valuation_rerating_pct: float | None
    analyst_revision_breadth: float | None
    media_attention_change_pct: float | None


class PriceRecognitionState(str, Enum):
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNRECOGNIZED = "UNRECOGNIZED"
    EARLY_RECOGNITION = "EARLY_RECOGNITION"
    PARTIALLY_RECOGNIZED = "PARTIALLY_RECOGNIZED"
    FULLY_RECOGNIZED_POTENTIALLY_LATE = "FULLY_RECOGNIZED_POTENTIALLY_LATE"


@dataclass(frozen=True)
class PriceRecognitionPreview:
    snapshot_id: str
    pre_inflection_preview_id: str
    pre_inflection_fingerprint: str
    pre_inflection_review_id: str
    state: PriceRecognitionState
    price_change_since_anchor_pct: float
    week_52_position: float | None
    recognized_dimensions: tuple[str, ...]
    available_dimensions: tuple[str, ...]
    missing_dimensions: tuple[str, ...]
    reason_codes: tuple[str, ...]
    uncertainty_statement: str
    eligible_for_eip_review: bool
    non_authority_statement: str


__all__ = ["PriceRecognitionPreview", "PriceRecognitionState", "PublicMarketRecognitionSnapshot"]
