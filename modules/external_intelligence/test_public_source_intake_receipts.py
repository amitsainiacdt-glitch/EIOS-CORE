"""Offline tests for public-only acquisition and extraction audit receipts."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_intake_coverage_service import PublicIntakeCoverageService
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        acquisition_ledger = PublicSourceAcquisitionLedger(root / "acquisitions.jsonl")
        extraction_ledger = PublicDocumentExtractionLedger(root / "extractions.jsonl")
        start = datetime(2026, 8, 29, 9, tzinfo=timezone.utc)

        def acquired(identifier, suffix):
            content = f"public document {identifier}".encode()
            return acquisition_ledger.record(
                acquisition_id=identifier, cycle_id="cycle-1", job_id="public-source-job",
                research_intent="EARLY_INTELLIGENCE", source_url=f"https://exchange.example.com/{suffix}",
                access_classification="PUBLIC", status="RETRIEVED", requested_at=start,
                completed_at=start + timedelta(minutes=1), http_status=200,
                content_type="application/pdf", source_document_id=identifier,
                document_hash=sha256(content).hexdigest(), bytes_received=len(content),
                recorder="Acquisition Adapter",
            )

        complete_acquisition = acquired("ACQ-1", "one.pdf")
        partial_acquisition = acquired("ACQ-2", "two.pdf")
        failed_extraction_acquisition = acquired("ACQ-3", "three.pdf")
        missing_extraction_acquisition = acquired("ACQ-4", "four.pdf")
        failed_acquisition = acquisition_ledger.record(
            acquisition_id="ACQ-5", cycle_id="cycle-1", job_id="public-source-job",
            research_intent="EARLY_INTELLIGENCE", source_url="https://exchange.example.com/missing.pdf",
            access_classification="PUBLIC", status="FAILED", requested_at=start,
            completed_at=start + timedelta(minutes=1), http_status=404,
            bytes_received=0, error_code="HTTP_404", error_message="Document not found.",
            recorder="Acquisition Adapter",
        )

        complete = extraction_ledger.record(
            complete_acquisition, extraction_id="EXT-1", extraction_method="pdf_text",
            status="SUCCEEDED", extracted_content="Complete public filing text.", page_count=3,
            extracted_at=start + timedelta(minutes=2), recorder="Extraction Adapter",
        )
        partial = extraction_ledger.record(
            partial_acquisition, extraction_id="EXT-2", extraction_method="pdf_text",
            status="PARTIAL", extracted_content="Only readable first page.", page_count=1,
            warnings=["Two scanned pages were unreadable."],
            extracted_at=start + timedelta(minutes=2), recorder="Extraction Adapter",
        )
        failed = extraction_ledger.record(
            failed_extraction_acquisition, extraction_id="EXT-3", extraction_method="pdf_text",
            status="FAILED", error_code="ENCRYPTED_PDF", error_message="Document is encrypted.",
            extracted_at=start + timedelta(minutes=2), recorder="Extraction Adapter",
        )

        assert acquisition_ledger.read_all() == (
            complete_acquisition, partial_acquisition, failed_extraction_acquisition,
            missing_extraction_acquisition, failed_acquisition,
        )
        assert extraction_ledger.read_all() == (complete, partial, failed)
        preview = PublicIntakeCoverageService().preview(
            acquisition_ledger.read_all(), extraction_ledger.read_all()
        )
        assert preview.acquisition_count == 5 and preview.retrieved_count == 4
        assert preview.acquisition_failure_count == 1
        assert preview.extraction_success_count == 1
        assert preview.extraction_partial_count == 1
        assert preview.extraction_failure_count == 1
        assert preview.retrieved_without_extraction_ids == ("ACQ-4",)
        assert len(preview.warnings) == 4

        tampered_payload = acquisition_ledger._payload(complete_acquisition)
        tampered_payload["canonical_url"] = "https://attacker.example.com/changed"
        try:
            acquisition_ledger._parse(tampered_payload)
        except ValueError as exc:
            assert "URL identity" in str(exc)
        else:
            raise AssertionError("tampered acquisition identity accepted")

        try:
            acquisition_ledger.record(
                acquisition_id="PRIVATE-1", cycle_id="cycle-1", job_id="job",
                research_intent="TEST", source_url="https://private.example.com/document",
                access_classification="UPSI", status="FAILED", requested_at=start,
                completed_at=start, error_code="BLOCKED", error_message="Not public.",
                recorder="Adapter",
            )
        except ValueError as exc:
            assert "PUBLIC" in str(exc)
        else:
            raise AssertionError("non-public information accepted")

        try:
            extraction_ledger.record(
                failed_acquisition, extraction_id="EXT-FAIL", extraction_method="pdf_text",
                status="FAILED", error_code="NO_DOCUMENT", error_message="Nothing retrieved.",
                extracted_at=start + timedelta(minutes=2), recorder="Adapter",
            )
        except ValueError as exc:
            assert "successfully retrieved" in str(exc)
        else:
            raise AssertionError("failed acquisition reached extraction")

        stale = replace(complete, acquisition_fingerprint="0" * 64)
        try:
            PublicIntakeCoverageService().preview(
                acquisition_ledger.read_all(), [stale, partial, failed]
            )
        except ValueError as exc:
            assert "stale" in str(exc)
        else:
            raise AssertionError("stale extraction binding accepted")

    print("PUBLIC SOURCE INTAKE RECEIPTS: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
