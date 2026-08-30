"""Typed audit receipt for extraction from one acquired public document."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PublicDocumentExtractionStatus(str, Enum):
    SUCCEEDED = "SUCCEEDED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


@dataclass(frozen=True)
class PublicDocumentExtractionReceipt:
    schema_version: int
    extraction_id: str
    acquisition_id: str
    acquisition_fingerprint: str
    document_hash: str
    extraction_method: str
    status: PublicDocumentExtractionStatus
    extracted_content_fingerprint: str | None
    character_count: int
    page_count: int | None
    warnings: tuple[str, ...]
    error_code: str | None
    error_message: str | None
    extracted_at: datetime
    recorder: str


__all__ = ["PublicDocumentExtractionReceipt", "PublicDocumentExtractionStatus"]
