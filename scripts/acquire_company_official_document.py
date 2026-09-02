"""Acquire and archive one explicitly approved public company document."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


ROOT = Path(__file__).resolve().parents[1]


def workspace_path(value: str) -> Path:
    path = (ROOT / value).resolve()
    if ROOT.resolve() not in path.parents:
        raise ValueError("output paths must remain inside the EIOS workspace")
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Acquire a public issuer document into the EIOS immutable archive.")
    for name in ("company-id", "company-name", "issuer-domain", "document-id", "url", "acquisition-id", "cycle-id"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--recorder", default="EIOS_AUTOMATION")
    parser.add_argument("--archive-root", default="data/company_intelligence/document_archive")
    parser.add_argument("--archive-ledger", default="data/company_intelligence/document_archive_ledger.jsonl")
    parser.add_argument("--acquisition-ledger", default="data/company_intelligence/company_document_acquisition_ledger.jsonl")
    args = parser.parse_args(argv)

    registry = TrustedPublicSourceRegistry((
        TrustedPublicSourceDefinition(
            args.company_id, args.company_name, (args.issuer_domain,),
            source_type="COMPANY_PRIMARY",
        ),
    ))
    acquired_at = datetime.now(timezone.utc)
    result = TrustedPublicAcquisitionAdapter(
        registry,
        PublicSourceAcquisitionLedger(workspace_path(args.acquisition_ledger)),
    ).acquire(
        acquisition_id=args.acquisition_id,
        cycle_id=args.cycle_id,
        job_id=f"{args.company_id}-OFFICIAL-DOCUMENT",
        research_intent="OFFICIAL_DOCUMENT_DISCOVERY",
        url=args.url,
        recorder=args.recorder,
        requested_at=acquired_at,
        source_document_id=args.document_id,
    )
    if result.document_bytes is None:
        print(f"Official document acquisition failed: {result.receipt.error_message}")
        return 1

    version = CompanyDocumentArchive(
        workspace_path(args.archive_root),
        workspace_path(args.archive_ledger),
    ).preserve(
        result,
        company_id=args.company_id,
        document_id=args.document_id,
        acquired_at=acquired_at,
    )
    print(f"Archived {version.document_id} | version {version.version_number} | {version.change_status}")
    print(f"SHA-256: {version.document_hash}")
    print("No Evidence, verdict, recommendation or trade was created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
