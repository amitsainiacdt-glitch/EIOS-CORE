"""Offline boundary tests for guarded public-document extraction."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition
from modules.external_intelligence.http_retriever import RetrievedContent


def text_pdf_bytes(text):
    from io import BytesIO
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
    writer = PdfWriter(); page = writer.add_blank_page(width=612, height=792)
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
    if text:
        stream = DecodedStreamObject(); stream.set_data(f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode("ascii"))
        page[NameObject("/Contents")] = writer._add_object(stream)
    output = BytesIO(); writer.write(output); return output.getvalue()


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        acquisitions = PublicSourceAcquisitionLedger(root / "acquisitions.jsonl")
        extractions = PublicDocumentExtractionLedger(root / "extractions.jsonl")
        now = datetime(2026, 8, 29, 12, tzinfo=timezone.utc)
        source = TrustedPublicSourceDefinition("TEST", "Test Exchange", ("example.com",))

        def result(identifier, body, content_type):
            from hashlib import sha256
            receipt = acquisitions.record(
                acquisition_id=identifier, cycle_id="cycle", job_id="job", research_intent="TEST",
                source_url=f"https://example.com/{identifier}", access_classification="PUBLIC",
                status="RETRIEVED", requested_at=now, completed_at=now,
                http_status=200, content_type=content_type, document_hash=sha256(body).hexdigest(),
                bytes_received=len(body), recorder="Acquirer",
            )
            text = body.decode("utf-8", errors="replace")
            return TrustedPublicAcquisitionResult(source, receipt, RetrievedContent(receipt.source_url, 200, text, content_type, {}), body)

        clock = lambda: now + timedelta(minutes=1)
        adapter = TrustedPublicDocumentExtractionAdapter(extractions, clock=clock, minimum_characters=20)
        html = result("HTML", b"<html><main><h1>Order awarded</h1><script>ignore</script><p>Public filing text.</p></main></html>", "text/html; charset=utf-8")
        success = adapter.extract(html, extraction_id="EXT-HTML", recorder="Extractor")
        assert success.receipt.status.value == "SUCCEEDED"
        assert success.extracted_text == "Order awarded Public filing text."

        short = adapter.extract(result("SHORT", b"brief", "text/plain"), extraction_id="EXT-SHORT", recorder="Extractor")
        assert short.receipt.status.value == "PARTIAL" and short.receipt.warnings

        pdf = adapter.extract(result("PDF", text_pdf_bytes("Official rainfall forecast text for public review"), "application/pdf"), extraction_id="EXT-PDF", recorder="Extractor")
        assert pdf.receipt.status.value == "SUCCEEDED" and pdf.receipt.page_count == 1
        assert pdf.receipt.extraction_method == "pypdf_text_layer_v1" and "rainfall forecast" in pdf.extracted_text
        image_only = adapter.extract(result("PDF-BLANK", text_pdf_bytes(""), "application/pdf"), extraction_id="EXT-PDF-BLANK", recorder="Extractor")
        assert image_only.receipt.status.value == "FAILED" and image_only.receipt.error_code == "PDF_NO_TEXT_LAYER"

        original = result("TAMPER", b"authentic public text document", "text/plain")
        tampered = replace(original, document_bytes=b"changed")
        mismatch = adapter.extract(tampered, extraction_id="EXT-TAMPER", recorder="Extractor")
        assert mismatch.receipt.error_code == "DOCUMENT_HASH_MISMATCH" and mismatch.extracted_text is None

        unsupported = adapter.extract(result("IMAGE", b"image bytes", "image/png"), extraction_id="EXT-IMAGE", recorder="Extractor")
        assert unsupported.receipt.error_code == "UNSUPPORTED_CONTENT_TYPE"
        assert len(extractions.read_all()) == 6

    print("TRUSTED PUBLIC DOCUMENT EXTRACTION ADAPTER: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
