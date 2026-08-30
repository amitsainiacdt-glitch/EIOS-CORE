"""Perform one guarded acquisition from an approved Indian public source."""

import argparse
from datetime import datetime, timezone

from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


def main(argv=None):
    parser = argparse.ArgumentParser(description="Acquire one document from an approved public institutional source.")
    for name in ("acquisition-id", "cycle-id", "job-id", "research-intent", "url", "ledger-path", "recorder"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--source-document-id")
    args = parser.parse_args(argv)
    try:
        result = TrustedPublicAcquisitionAdapter(
            TrustedPublicSourceRegistry.india_primary_sources(),
            PublicSourceAcquisitionLedger(args.ledger_path),
        ).acquire(
            acquisition_id=args.acquisition_id, cycle_id=args.cycle_id,
            job_id=args.job_id, research_intent=args.research_intent,
            url=args.url, recorder=args.recorder,
            requested_at=datetime.now(timezone.utc),
            source_document_id=args.source_document_id,
        )
    except (OSError, TypeError, ValueError) as exc:
        print(f"Trusted public acquisition blocked: {exc}")
        return 1
    receipt = result.receipt
    print(f"Source: {result.source.name}")
    print(f"Status: {receipt.status.value}")
    print(f"Requested URL: {receipt.requested_url}")
    print(f"Final URL: {receipt.source_url}")
    if receipt.document_hash:
        print(f"Document hash: {receipt.document_hash}")
        print(f"Bytes received: {receipt.bytes_received}")
    if receipt.error_message:
        print(f"Error: {receipt.error_message}")
    print("Audit receipt appended. No Observation, Evidence, Signal, or Meta analysis was created.")
    return 0 if result.retrieved_content is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
