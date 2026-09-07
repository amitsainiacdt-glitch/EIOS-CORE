"""Reuse a corroborated EIOS browser capture after direct acquisition fails."""

import json
from pathlib import Path

from modules.company_intelligence.local_report_import import import_local_report
from modules.company_intelligence.official_document_fallback import FallbackAcquisitionResult, OfficialDocumentDeliveryProvenance
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


class BrowserCaptureFallbackProvider:
    provider_id = "EIOS_CORROBORATED_BROWSER_CAPTURE"

    def __init__(self, root, *, workspace, ledger):
        self.root, self.workspace, self.ledger = Path(root).resolve(), Path(workspace).resolve(), ledger

    def acquire_after_failure(self, primary_result, **request):
        matches = []
        if self.root.is_dir():
            for path in self.root.glob("*/provenance.json"):
                record = json.loads(path.read_text(encoding="utf-8"))
                if (record.get("schema_version") == 1 and record.get("source_url") == request["url"]
                        and record.get("status") == "BROWSER_COPY_CORROBORATED_PENDING_REVIEW"
                        and record.get("creates_approved_facts") is False):
                    matches.append((path, record))
        if len(matches) != 1:
            return None
        provenance_path, record = matches[0]
        report = (provenance_path.parent / record["preserved_file"]).resolve()
        if provenance_path.parent.resolve() not in report.parents:
            raise ValueError("browser capture path leaves its provenance directory")
        acquired = import_local_report(report, workspace=self.workspace, source_url=request["url"],
            expected_sha256=record["document_hash"], registry=TrustedPublicSourceRegistry((primary_result.source,)), ledger=self.ledger)
        return FallbackAcquisitionResult(acquired.source, acquired.receipt, acquired.retrieved_content,
            acquired.document_bytes, OfficialDocumentDeliveryProvenance(self.provider_id,
            f"eios-local://browser-capture/{provenance_path.parent.name}", request["url"]))


__all__ = ["BrowserCaptureFallbackProvider"]
