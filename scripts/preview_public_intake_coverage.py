"""Print a read-only public acquisition and extraction coverage preview."""

import argparse
import json
from pathlib import Path

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_intake_coverage_service import PublicIntakeCoverageService
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger


def main(argv=None):
    parser = argparse.ArgumentParser(description="Preview public-source acquisition and extraction coverage.")
    parser.add_argument("--acquisition-ledger-path", required=True)
    parser.add_argument("--extraction-ledger-path", required=True)
    args = parser.parse_args(argv)
    acquisition_path, extraction_path = Path(args.acquisition_ledger_path), Path(args.extraction_ledger_path)
    try:
        before = {path: path.read_bytes() for path in (acquisition_path, extraction_path)}
        preview = PublicIntakeCoverageService().preview(
            PublicSourceAcquisitionLedger(acquisition_path).read_all(),
            PublicDocumentExtractionLedger(extraction_path).read_all(),
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Public intake coverage error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Public intake coverage error: a source ledger changed.")
        return 1
    payload = {**preview.__dict__}
    for key in (
        "failed_acquisition_ids", "partial_extraction_ids", "failed_extraction_ids",
        "retrieved_without_extraction_ids", "warnings",
    ):
        payload[key] = list(payload[key])
    print(json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False))
    print("Read-only preview: Meta-Analysis and downstream engines were not invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
