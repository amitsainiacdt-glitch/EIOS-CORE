"""Acquire and extract one approved public document without admitting it to EIOS."""

import argparse
from datetime import datetime, timezone

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


def main(argv=None):
    parser = argparse.ArgumentParser(description="Acquire and extract one approved public document.")
    for name in ("acquisition-id", "extraction-id", "cycle-id", "job-id", "research-intent", "url", "acquisition-ledger-path", "extraction-ledger-path", "recorder"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--source-document-id")
    args = parser.parse_args(argv)
    acquisition = TrustedPublicAcquisitionAdapter(
        TrustedPublicSourceRegistry.india_primary_sources(),
        PublicSourceAcquisitionLedger(args.acquisition_ledger_path),
    ).acquire(
        acquisition_id=args.acquisition_id, cycle_id=args.cycle_id, job_id=args.job_id,
        research_intent=args.research_intent, url=args.url, recorder=args.recorder,
        requested_at=datetime.now(timezone.utc), source_document_id=args.source_document_id,
    )
    print(f"Acquisition: {acquisition.receipt.status.value}")
    if acquisition.retrieved_content is None:
        print(f"Acquisition error: {acquisition.receipt.error_message}")
        return 1
    extraction = TrustedPublicDocumentExtractionAdapter(
        PublicDocumentExtractionLedger(args.extraction_ledger_path)
    ).extract(acquisition, extraction_id=args.extraction_id, recorder=args.recorder)
    print(f"Extraction: {extraction.receipt.status.value}")
    print(f"Method: {extraction.receipt.extraction_method}")
    print(f"Characters: {extraction.receipt.character_count}")
    if extraction.receipt.warnings:
        print("Warnings: " + "; ".join(extraction.receipt.warnings))
    if extraction.receipt.error_message:
        print(f"Extraction error: {extraction.receipt.error_message}")
    print("Audit receipts appended. No Observation, Evidence, Signal, or Meta analysis was created.")
    return 0 if extraction.extracted_text is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
