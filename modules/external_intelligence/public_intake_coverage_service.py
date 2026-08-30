"""Read-only coverage reconciliation for public intake receipts."""

import hashlib
import json

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_intake_coverage_preview import PublicIntakeCoveragePreview
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionReceipt, PublicSourceAcquisitionStatus


class PublicIntakeCoverageService:
    def preview(self, acquisitions, extractions):
        if not isinstance(acquisitions, (list, tuple)) or any(not isinstance(item, PublicSourceAcquisitionReceipt) for item in acquisitions):
            raise ValueError("acquisitions must contain acquisition receipts")
        if not isinstance(extractions, (list, tuple)) or any(not isinstance(item, PublicDocumentExtractionReceipt) for item in extractions):
            raise ValueError("extractions must contain extraction receipts")
        by_id = {item.acquisition_id: item for item in acquisitions}
        if len(by_id) != len(acquisitions): raise ValueError("duplicate acquisition IDs")
        extracted_acquisitions = set()
        for extraction in extractions:
            acquisition = by_id.get(extraction.acquisition_id)
            if acquisition is None: raise ValueError("orphan extraction receipt")
            if extraction.acquisition_fingerprint != PublicSourceAcquisitionLedger.receipt_fingerprint(acquisition): raise ValueError("stale extraction acquisition fingerprint")
            if extraction.document_hash != acquisition.document_hash: raise ValueError("extraction document hash mismatch")
            if extraction.acquisition_id in extracted_acquisitions: raise ValueError("duplicate extraction for acquisition")
            extracted_acquisitions.add(extraction.acquisition_id)
        retrieved = [item for item in acquisitions if item.status == PublicSourceAcquisitionStatus.RETRIEVED]
        acquisition_failures = tuple(sorted(item.acquisition_id for item in acquisitions if item.status == PublicSourceAcquisitionStatus.FAILED))
        successes = [item for item in extractions if item.status == PublicDocumentExtractionStatus.SUCCEEDED]
        partials = tuple(sorted(item.extraction_id for item in extractions if item.status == PublicDocumentExtractionStatus.PARTIAL))
        failures = tuple(sorted(item.extraction_id for item in extractions if item.status == PublicDocumentExtractionStatus.FAILED))
        missing = tuple(sorted(item.acquisition_id for item in retrieved if item.acquisition_id not in extracted_acquisitions))
        warnings = []
        if acquisition_failures: warnings.append(f"{len(acquisition_failures)} public-source acquisitions failed.")
        if partials: warnings.append(f"{len(partials)} document extractions are partial.")
        if failures: warnings.append(f"{len(failures)} document extractions failed.")
        if missing: warnings.append(f"{len(missing)} retrieved documents have no extraction receipt.")
        payload = {
            "acquisition_count": len(acquisitions), "retrieved_count": len(retrieved),
            "acquisition_failure_count": len(acquisition_failures), "extraction_count": len(extractions),
            "extraction_success_count": len(successes), "extraction_partial_count": len(partials),
            "extraction_failure_count": len(failures), "retrieved_without_extraction_count": len(missing),
            "failed_acquisition_ids": acquisition_failures, "partial_extraction_ids": partials,
            "failed_extraction_ids": failures, "retrieved_without_extraction_ids": missing,
            "warnings": warnings,
        }
        fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return PublicIntakeCoveragePreview(
            fingerprint, len(acquisitions), len(retrieved), len(acquisition_failures),
            len(extractions), len(successes), len(partials), len(failures), len(missing),
            acquisition_failures, partials, failures, missing, tuple(warnings),
        )


__all__ = ["PublicIntakeCoverageService"]
