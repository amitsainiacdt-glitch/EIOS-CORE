"""Automatic, fail-closed delivery from the governed local report inbox."""

import json
from pathlib import Path

from modules.company_intelligence.local_report_import import import_local_report
from modules.company_intelligence.official_document_fallback import (
    FallbackAcquisitionResult,
    OfficialDocumentDeliveryProvenance,
)
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


class LocalDocumentFallbackProvider:
    provider_id = "EIOS_GOVERNED_LOCAL_INBOX"

    def __init__(self, inbox, *, workspace, ledger):
        self.inbox = Path(inbox).resolve()
        self.workspace = Path(workspace).resolve()
        self.ledger = ledger

    def acquire_after_failure(self, primary_result, **request):
        requested_url = request["url"]
        matches = []
        if self.inbox.is_dir():
            for sidecar in self.inbox.glob("*.json"):
                payload = json.loads(sidecar.read_text(encoding="utf-8"))
                if payload.get("schema_version") == 1 and payload.get("source_url") == requested_url:
                    matches.append((sidecar, payload))
        if len(matches) != 1:
            return None
        sidecar, payload = matches[0]
        report = (self.inbox / payload["file"]).resolve()
        if self.inbox not in report.parents:
            raise ValueError("local inbox mapping leaves the governed inbox")
        registry = TrustedPublicSourceRegistry((primary_result.source,))
        acquired = import_local_report(
            report, workspace=self.workspace, source_url=requested_url,
            expected_sha256=payload["sha256"], registry=registry, ledger=self.ledger,
        )
        return FallbackAcquisitionResult(
            acquired.source, acquired.receipt, acquired.retrieved_content, acquired.document_bytes,
            OfficialDocumentDeliveryProvenance(
                self.provider_id, f"eios-local://inbox/{sidecar.name}", requested_url),
        )


__all__ = ["LocalDocumentFallbackProvider"]
