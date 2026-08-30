"""Offline tests for guarded same-authority source discovery."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_source_discovery_service import TrustedPublicSourceDiscoveryService
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root, now = Path(directory), datetime(2026, 8, 30, tzinfo=timezone.utc)
        registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("CWC", "CWC", ("cwc.example",), ("/public/",)),))
        body = b'''<html><body>
          <a href="/public/reservoir-storage-2026-08-29.pdf">Current reservoir storage</a>
          <a href="report.csv">Reservoir bulletin data</a>
          <a href="https://evil.example/report.pdf">Reservoir external</a>
          <a href="javascript:alert(1)">Script</a><a href="mailto:x@example.com">Mail</a>
          <a href="/private/report.pdf">Outside allowed path</a>
          <a href="/public/about">About us</a>
        </body></html>'''
        acquisitions = PublicSourceAcquisitionLedger(root / "acq.jsonl")
        receipt = acquisitions.record(
            acquisition_id="ACQ-1", cycle_id="CYCLE", job_id="JOB", research_intent="HYDROLOGY",
            source_url="https://cwc.example/public/index.html", status="RETRIEVED", requested_at=now,
            completed_at=now, http_status=200, content_type="text/html; charset=utf-8",
            document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="test",
        )
        acquisition = TrustedPublicAcquisitionResult(
            registry.resolve(receipt.source_url), receipt,
            RetrievedContent(receipt.source_url, 200, body.decode(), receipt.content_type, {}), body,
        )
        extractions = PublicDocumentExtractionLedger(root / "ext.jsonl")
        extraction = extractions.record(
            receipt, extraction_id="EXT-1", extraction_method="deterministic_html_text_v1", status="SUCCEEDED",
            extracted_content="Current reservoir storage Reservoir bulletin data About us", extracted_at=now, recorder="test",
        )
        service = TrustedPublicSourceDiscoveryService(registry)
        preview = service.discover(acquisition, extraction, query_topics=("reservoir", "storage"))
        assert len(preview.candidates) == 2
        assert preview.candidates[0].document_type == "PDF"
        assert preview.candidates[0].date_tokens == ("2026-08-29",)
        assert preview.candidates[0].relevance_tier == "HIGH"
        assert preview.rejected_link_count == 4
        assert preview.creates_evidence is False and preview.creates_observation is False
        assert not (root / "observations.json").exists()
        assert service.discover(acquisition, extraction, query_topics=("storage", "reservoir")).candidates == preview.candidates

        altered = TrustedPublicAcquisitionResult(acquisition.source, receipt, acquisition.retrieved_content, body + b"changed")
        try:
            service.discover(altered, extraction, query_topics=("reservoir",))
        except ValueError as exc:
            assert "bytes" in str(exc)
        else:
            raise AssertionError("altered landing page accepted")

        wrong = PublicDocumentExtractionLedger(root / "wrong.jsonl").record(
            receipt, extraction_id="EXT-WRONG", extraction_method="deterministic_html_text_v1", status="SUCCEEDED",
            extracted_content="usable", extracted_at=now, recorder="test",
        )
        object.__setattr__(wrong, "acquisition_fingerprint", "0" * 64)
        try:
            service.discover(acquisition, wrong)
        except ValueError as exc:
            assert "fingerprint" in str(exc)
        else:
            raise AssertionError("stale extraction binding accepted")

    print("TRUSTED PUBLIC SOURCE DISCOVERY: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
