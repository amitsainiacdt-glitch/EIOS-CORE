"""Typed audit receipt for one public-source acquisition attempt."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PublicSourceAcquisitionStatus(str, Enum):
    RETRIEVED = "RETRIEVED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class PublicSourceAcquisitionReceipt:
    schema_version: int
    acquisition_id: str
    cycle_id: str
    job_id: str
    research_intent: str
    requested_url: str
    source_url: str
    canonical_url: str
    source_domain: str
    access_classification: str
    status: PublicSourceAcquisitionStatus
    requested_at: datetime
    completed_at: datetime
    http_status: int | None
    content_type: str | None
    source_document_id: str | None
    document_hash: str | None
    bytes_received: int
    error_code: str | None
    error_message: str | None
    recorder: str


__all__ = ["PublicSourceAcquisitionReceipt", "PublicSourceAcquisitionStatus"]
