"""Offline tests for hash-bound IMD rainfall record extraction."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_rainfall_record_extractor import TrustedPublicRainfallRecordExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root, now = Path(directory), datetime(2026, 8, 30, tzinfo=timezone.utc)
        html = '''<p>Rainfall Recorded from 0830 hrs of 29-08-2026 to 0830 hrs of 30-08-2026</p><script>
        {"title":"REGION : EAST AND NORTH EAST INDIA","id":"0","info":"No Data","balloonText":"No Data"}
        {"title":"REGION : SOUTH PENINSULA","id":"0","balloonText":"<h6>REGION : SOUTH PENINSULA</h6> <p><em>Departure : -66%</br>Actual : 1.8 mm</br>Normal : 5.2 mm</em></p>"}
        {"title":"COUNTRY : INDIA","id":"0","balloonText":"<h6>COUNTRY : INDIA</h6> <p><em>Departure : -26%</br>Actual : 5.2 mm</br>Normal : 7.1 mm</em></p>"}
        </script>'''
        body = html.encode()
        source = TrustedPublicSourceDefinition("IMD", "IMD", ("imd.example",), source_type="WEATHER_AUTHORITY")
        registry = TrustedPublicSourceRegistry((source,))
        receipts = PublicSourceAcquisitionLedger(root / "a.jsonl")
        receipt = receipts.record(
            acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="OBSERVED_RAINFALL",
            source_url="https://imd.example/rainfall", status="RETRIEVED", requested_at=now, completed_at=now,
            http_status=200, content_type="text/html; charset=utf-8", document_hash=sha256(body).hexdigest(),
            bytes_received=len(body), recorder="test",
        )
        acquisition = TrustedPublicAcquisitionResult(
            registry.resolve(receipt.source_url), receipt, RetrievedContent(receipt.source_url, 200, html, receipt.content_type, {}), body,
        )
        extraction = PublicDocumentExtractionLedger(root / "e.jsonl").record(
            receipt, extraction_id="E1", extraction_method="deterministic_html_text_v1", status="SUCCEEDED",
            extracted_content="Rainfall Recorded from 29 to 30 August", extracted_at=now, recorder="test",
        )
        preview = TrustedPublicRainfallRecordExtractor().extract(acquisition, extraction)
        assert len(preview.records) == 2 and not preview.creates_observation and preview.requires_human_review
        south, india = preview.records
        assert south.area == "REGION : SOUTH PENINSULA" and south.departure_percent == -66
        assert (india.actual_mm, india.normal_mm) == (5.2, 7.1)
        assert html[india.passage_start:india.passage_end] == india.source_passage
        altered = TrustedPublicAcquisitionResult(acquisition.source, receipt, acquisition.retrieved_content, body + b"x")
        try:
            TrustedPublicRainfallRecordExtractor().extract(altered, extraction)
        except ValueError as exc:
            assert "bytes" in str(exc)
        else:
            raise AssertionError("altered rainfall page accepted")
        weekly_body = body.replace(b"Rainfall Recorded from 0830 hrs of 29-08-2026 to 0830 hrs of 30-08-2026", b"Weekly (30-08-2026)<script>var check=\"W\";</script>")
        weekly_receipt = PublicSourceAcquisitionLedger(root / "wa.jsonl").record(
            acquisition_id="WA1", cycle_id="C1", job_id="WJ1", research_intent="OBSERVED_RAINFALL",
            source_url="https://imd.example/rainfall?msg=W", status="RETRIEVED", requested_at=now, completed_at=now,
            http_status=200, content_type="text/html", document_hash=sha256(weekly_body).hexdigest(),
            bytes_received=len(weekly_body), recorder="test",
        )
        weekly_acquisition = TrustedPublicAcquisitionResult(
            registry.resolve(weekly_receipt.source_url), weekly_receipt,
            RetrievedContent(weekly_receipt.source_url, 200, weekly_body.decode(), "text/html", {}), weekly_body,
        )
        weekly_extraction = PublicDocumentExtractionLedger(root / "we.jsonl").record(
            weekly_receipt, extraction_id="WE1", extraction_method="deterministic_html_text_v1", status="SUCCEEDED",
            extracted_content="Weekly 30 August", extracted_at=now, recorder="test",
        )
        assert TrustedPublicRainfallRecordExtractor().extract(weekly_acquisition, weekly_extraction).period_label == "Weekly (30-08-2026)"
    print("TRUSTED PUBLIC RAINFALL RECORD EXTRACTOR: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
