"""Structured public Central Pool stock-versus-buffer records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicFoodgrainBufferRecord:
    record_id: str
    grain: str
    reporting_date: str
    norm_reference_date: str
    stock_lmt: float
    buffer_norm_lmt: float
    stock_to_norm_percent: float
    additional_unmilled_paddy_lmt: float | None
    source_passage: str
    acquisition_id: str
    document_hash: str
    source_url: str


@dataclass(frozen=True)
class PublicFoodgrainBufferPreview:
    acquisition_id: str
    extraction_id: str
    records: tuple[PublicFoodgrainBufferRecord,...]
    creates_observation: bool = False
    requires_human_review: bool = True


__all__=["PublicFoodgrainBufferRecord","PublicFoodgrainBufferPreview"]
