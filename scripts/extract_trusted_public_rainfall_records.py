"""Acquire and extract IMD observed-rainfall records without admitting facts."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_rainfall_record_extractor import TrustedPublicRainfallRecordExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


def main(argv=None):
    parser = argparse.ArgumentParser(description="Extract structured observed rainfall from an official IMD page.")
    for name in ("acquisition-id", "extraction-id", "cycle-id", "job-id", "url", "acquisition-ledger-path", "extraction-ledger-path", "output-path", "recorder"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args(argv)
    registry = TrustedPublicSourceRegistry.india_primary_sources()
    acquisition = TrustedPublicAcquisitionAdapter(registry, PublicSourceAcquisitionLedger(args.acquisition_ledger_path)).acquire(
        acquisition_id=args.acquisition_id, cycle_id=args.cycle_id, job_id=args.job_id,
        research_intent="OBSERVED_RAINFALL", url=args.url, recorder=args.recorder,
        requested_at=datetime.now(timezone.utc),
    )
    if acquisition.retrieved_content is None:
        print(f"Acquisition blocked: {acquisition.receipt.error_message}")
        return 1
    extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(args.extraction_ledger_path)).extract(
        acquisition, extraction_id=args.extraction_id, recorder=args.recorder,
    )
    if extraction.extracted_text is None:
        print(f"HTML extraction blocked: {extraction.receipt.error_message}")
        return 1
    preview = TrustedPublicRainfallRecordExtractor().extract(acquisition, extraction.receipt)
    payload = {
        "schema_version": 1, "acquisition_id": preview.acquisition_id, "extraction_id": preview.extraction_id,
        "period_label": preview.period_label, "creates_observation": preview.creates_observation,
        "requires_human_review": preview.requires_human_review,
        "records": [item.__dict__ for item in preview.records],
    }
    output = Path(args.output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Period: {preview.period_label}")
    print(f"Observed rainfall records: {len(preview.records)}")
    print(f"Output: {output}")
    print("No Observation, Evidence, Meta conclusion, Signal, recommendation, or trade was created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
