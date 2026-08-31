"""Offline checks for hash-bound crop-area table extraction."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_crop_area_extractor import TrustedPublicCropAreaExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root, now = Path(directory), datetime(2026, 8, 31, tzinfo=timezone.utc)
        html = '''<h1>Ministry of Agriculture & Farmers Welfare</h1>
        <h2>All India: Progressive Crop Area Sown Report - Kharif Weekly area coverage as on 21.08.2026</h2>
        <p>Area in Lakh Ha</p><table><tr><th>No.</th><th>Crop</th><th>Normal</th><th>2026-27</th><th>2025-26</th><th>Difference</th></tr>
        <tr><td>1</td><td>Rice</td><td>412.00</td><td>446.70</td><td>405.10</td><td>418.29</td><td>-13.19</td></tr>
        <tr><td>2</td><td>Pulses</td><td>123.64</td><td>113.63</td><td>112.14</td><td>1.49</td></tr>
        <tr><td>2</td><td>Pulses</td><td>123.64</td><td>113.63</td><td>112.14</td><td>1.49</td></tr></table>'''
        body = html.encode(); registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("PIB", "PIB", ("pib.example",), source_type="GOVERNMENT_RELEASE_AUTHORITY"),))
        ledger = PublicSourceAcquisitionLedger(root / "a.jsonl")
        receipt = ledger.record(acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="CROP_PROGRESS", source_url="https://pib.example/release", status="RETRIEVED", requested_at=now, completed_at=now, http_status=200, content_type="text/html; charset=utf-8", document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="test")
        acquisition = TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url), receipt, RetrievedContent(receipt.source_url, 200, html, receipt.content_type, {}), body)
        extraction = PublicDocumentExtractionLedger(root / "e.jsonl").record(receipt, extraction_id="E1", extraction_method="deterministic_html_text_v1", status="SUCCEEDED", extracted_content="Ministry crop area", extracted_at=now, recorder="test")
        preview = TrustedPublicCropAreaExtractor().extract(acquisition, extraction)
        assert preview.period_label == "21.08.2026" and len(preview.records) == 2
        assert preview.records[0].crop == "Rice" and preview.records[0].normal_area == 412.00 and preview.records[0].difference_from_prior_year == -13.19
        assert preview.records[1].crop == "Total Pulses" and preview.records[1].current_area == 113.63 and not preview.creates_observation
        iso_body = body.replace(b"21.08.2026", b"2026-08-21")
        iso_receipt = PublicSourceAcquisitionLedger(root / "ia.jsonl").record(acquisition_id="IA1", cycle_id="C1", job_id="J1", research_intent="CROP_PROGRESS", source_url="https://pib.example/iso", status="RETRIEVED", requested_at=now, completed_at=now, http_status=200, content_type="text/html", document_hash=sha256(iso_body).hexdigest(), bytes_received=len(iso_body), recorder="test")
        iso_acquisition = TrustedPublicAcquisitionResult(registry.resolve(iso_receipt.source_url), iso_receipt, RetrievedContent(iso_receipt.source_url, 200, iso_body.decode(), "text/html", {}), iso_body)
        iso_extraction = PublicDocumentExtractionLedger(root / "ie.jsonl").record(iso_receipt, extraction_id="IE1", extraction_method="deterministic_html_text_v1", status="SUCCEEDED", extracted_content="Ministry crop area", extracted_at=now, recorder="test")
        assert TrustedPublicCropAreaExtractor().extract(iso_acquisition, iso_extraction).period_label == "2026-08-21"
        altered = TrustedPublicAcquisitionResult(acquisition.source, receipt, acquisition.retrieved_content, body + b"x")
        try: TrustedPublicCropAreaExtractor().extract(altered, extraction)
        except ValueError as exc: assert "bytes" in str(exc)
        else: raise AssertionError("altered crop-area release accepted")
    print("TRUSTED PUBLIC CROP AREA EXTRACTOR: ALL TESTS PASSED")


if __name__ == "__main__": main()
