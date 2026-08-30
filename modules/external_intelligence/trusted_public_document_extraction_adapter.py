"""Audited, non-analytical extraction from a guarded public acquisition."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import re

from pypdf import PdfReader

from modules.external_intelligence.external_content_normalizer import ExternalContentNormalizer
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


@dataclass(frozen=True)
class TrustedPublicDocumentExtractionResult:
    receipt: PublicDocumentExtractionReceipt
    extracted_text: str | None


class TrustedPublicDocumentExtractionAdapter:
    """Extracts text only; it performs no summarisation or investment analysis."""

    HTML_TYPES = ("text/html", "application/xhtml+xml")
    TEXT_TYPES = ("text/plain", "text/csv", "application/json", "application/xml", "text/xml")

    def __init__(self, ledger, *, normalizer=None, clock=None, minimum_characters=20, maximum_pdf_pages=500):
        if not isinstance(ledger, PublicDocumentExtractionLedger):
            raise ValueError("ledger must be a PublicDocumentExtractionLedger")
        if isinstance(minimum_characters, bool) or not isinstance(minimum_characters, int) or minimum_characters <= 0:
            raise ValueError("minimum_characters must be a positive integer")
        if isinstance(maximum_pdf_pages, bool) or not isinstance(maximum_pdf_pages, int) or maximum_pdf_pages <= 0:
            raise ValueError("maximum_pdf_pages must be a positive integer")
        self.ledger = ledger
        self.normalizer = normalizer or ExternalContentNormalizer()
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.minimum_characters = minimum_characters
        self.maximum_pdf_pages = maximum_pdf_pages

    def extract(self, acquisition, *, extraction_id, recorder):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        receipt = acquisition.receipt
        if receipt.status != PublicSourceAcquisitionStatus.RETRIEVED:
            raise ValueError("extraction requires a successfully retrieved acquisition")
        if acquisition.retrieved_content is None or acquisition.document_bytes is None:
            raise ValueError("retrieved acquisition is missing its document payload")

        actual_hash = sha256(acquisition.document_bytes).hexdigest()
        if actual_hash != receipt.document_hash:
            return self._failed(receipt, extraction_id, recorder, "DOCUMENT_HASH_MISMATCH", "Document bytes do not match the acquisition receipt.")

        media_type = self._media_type(receipt.content_type)
        if media_type == "application/pdf" or acquisition.document_bytes.startswith(b"%PDF-"):
            return self._extract_pdf(acquisition, extraction_id=extraction_id, recorder=recorder)
        if media_type not in self.HTML_TYPES + self.TEXT_TYPES:
            return self._failed(receipt, extraction_id, recorder, "UNSUPPORTED_CONTENT_TYPE", f"Unsupported public document content type: {media_type or 'unknown'}.")

        try:
            normalized = self.normalizer.normalize(acquisition.retrieved_content)
            text = normalized.normalized_text.strip()
        except Exception as exc:
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            return self._failed(receipt, extraction_id, recorder, "EXTRACTION_ERROR", str(exc) or type(exc).__name__)

        if not text:
            return self._failed(receipt, extraction_id, recorder, "EMPTY_EXTRACTION", "The document produced no readable text.")
        warnings = ()
        status = "SUCCEEDED"
        if len(text) < self.minimum_characters:
            status = "PARTIAL"
            warnings = (f"Extracted text is shorter than {self.minimum_characters} characters.",)
        extraction_receipt = self.ledger.record(
            receipt, extraction_id=extraction_id, extraction_method=self._method(media_type),
            status=status, extracted_content=text, warnings=warnings,
            extracted_at=self.clock(), recorder=recorder,
        )
        return TrustedPublicDocumentExtractionResult(extraction_receipt, text)

    def _extract_pdf(self, acquisition, *, extraction_id, recorder):
        receipt = acquisition.receipt
        try:
            reader = PdfReader(BytesIO(acquisition.document_bytes), strict=True)
            if reader.is_encrypted:
                return self._failed(receipt, extraction_id, recorder, "PDF_ENCRYPTED", "Encrypted public PDFs are not accepted for unattended extraction.")
            page_count = len(reader.pages)
            if page_count <= 0:
                return self._failed(receipt, extraction_id, recorder, "PDF_NO_PAGES", "The PDF contains no pages.")
            if page_count > self.maximum_pdf_pages:
                return self._failed(receipt, extraction_id, recorder, "PDF_PAGE_LIMIT_EXCEEDED", f"PDF has {page_count} pages; limit is {self.maximum_pdf_pages}.")
            page_texts, blank_pages = [], []
            for number, page in enumerate(reader.pages, 1):
                value = page.extract_text() or ""
                value = re.sub(r"\s+", " ", value).strip()
                if value: page_texts.append(value)
                else: blank_pages.append(number)
            text = "\n".join(page_texts).strip()
        except Exception as exc:
            if isinstance(exc, (KeyboardInterrupt, SystemExit)): raise
            return self._failed(receipt, extraction_id, recorder, "PDF_EXTRACTION_ERROR", str(exc) or type(exc).__name__)
        if not text:
            return self._failed(receipt, extraction_id, recorder, "PDF_NO_TEXT_LAYER", "The PDF produced no readable text; OCR is not authorized by this adapter.")
        warnings = []
        if blank_pages: warnings.append(f"{len(blank_pages)} of {page_count} PDF pages produced no text.")
        if len(text) < self.minimum_characters: warnings.append(f"Extracted text is shorter than {self.minimum_characters} characters.")
        status = "PARTIAL" if warnings else "SUCCEEDED"
        extraction_receipt = self.ledger.record(
            receipt, extraction_id=extraction_id, extraction_method="pypdf_text_layer_v1", status=status,
            extracted_content=text, page_count=page_count, warnings=tuple(warnings),
            extracted_at=self.clock(), recorder=recorder,
        )
        return TrustedPublicDocumentExtractionResult(extraction_receipt, text)

    def _failed(self, acquisition_receipt, extraction_id, recorder, code, message):
        receipt = self.ledger.record(
            acquisition_receipt, extraction_id=extraction_id, extraction_method="content_type_router_v1",
            status="FAILED", error_code=code, error_message=message,
            extracted_at=self.clock(), recorder=recorder,
        )
        return TrustedPublicDocumentExtractionResult(receipt, None)

    @staticmethod
    def _media_type(value):
        return (value or "").split(";", 1)[0].strip().casefold()

    @classmethod
    def _method(cls, media_type):
        return "deterministic_html_text_v1" if media_type in cls.HTML_TYPES else "deterministic_plain_text_v1"


__all__ = ["TrustedPublicDocumentExtractionAdapter", "TrustedPublicDocumentExtractionResult"]
