"""Passive coverage summary for public acquisition and extraction receipts."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicIntakeCoveragePreview:
    preview_fingerprint: str
    acquisition_count: int
    retrieved_count: int
    acquisition_failure_count: int
    extraction_count: int
    extraction_success_count: int
    extraction_partial_count: int
    extraction_failure_count: int
    retrieved_without_extraction_count: int
    failed_acquisition_ids: tuple[str, ...]
    partial_extraction_ids: tuple[str, ...]
    failed_extraction_ids: tuple[str, ...]
    retrieved_without_extraction_ids: tuple[str, ...]
    warnings: tuple[str, ...]


__all__ = ["PublicIntakeCoveragePreview"]
