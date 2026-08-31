"""Hash-bound extraction of IMD's server-rendered rainfall map records."""

from __future__ import annotations

import hashlib
import re

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_rainfall_record import PublicRainfallRecord, PublicRainfallRecordPreview
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class TrustedPublicRainfallRecordExtractor:
    CHECK = re.compile(r'var\s+check\s*=\s*["\'](?P<view>[DWMC])["\']', re.IGNORECASE)
    PERIODS = {
        "D": re.compile(r"Rainfall Recorded from\s+([^<\r\n]+)", re.IGNORECASE),
        "W": re.compile(r"(Weekly\s*\([^<]+\))", re.IGNORECASE),
        "M": re.compile(r"(Monthly\s*\([^<]+\))", re.IGNORECASE),
        "C": re.compile(r"(Cumulative\s*\([^<]+\))", re.IGNORECASE),
    }
    OBJECT = re.compile(r"\{[^{}]*\}", re.DOTALL)
    TITLE = re.compile(r'"title"\s*:\s*"(?P<area>(?:\\.|[^"])*)"', re.IGNORECASE)
    BALLOON = re.compile(r'"balloonText"\s*:\s*"(?P<passage>(?:\\.|[^"])*)"', re.IGNORECASE)
    METRICS = re.compile(
        r"Departure\s*:\s*(?P<departure>-?\d+(?:\.\d+)?)%.*?"
        r"Actual\s*:\s*(?P<actual>\d+(?:\.\d+)?)\s*mm.*?"
        r"Normal\s*:\s*(?P<normal>\d+(?:\.\d+)?)\s*mm",
        re.IGNORECASE | re.DOTALL,
    )

    def extract(self, acquisition, extraction_receipt):
        self._validate(acquisition, extraction_receipt)
        html = acquisition.document_bytes.decode(self._encoding(acquisition), errors="replace")
        check_match = self.CHECK.search(html)
        view = check_match.group("view").upper() if check_match else "D"
        period_match = self.PERIODS[view].search(html)
        if not period_match:
            raise ValueError("official rainfall period label was not found")
        period = " ".join(re.sub(r"<[^>]+>", " ", period_match.group(1)).split())
        records = []
        for object_match in self.OBJECT.finditer(html):
            title_match = self.TITLE.search(object_match.group(0))
            balloon_match = self.BALLOON.search(object_match.group(0))
            if title_match is None or balloon_match is None:
                continue
            metrics = self.METRICS.search(balloon_match.group("passage"))
            if metrics is None:
                continue
            area = " ".join(title_match.group("area").split())
            passage = balloon_match.group("passage")
            passage_start = object_match.start() + balloon_match.start("passage")
            passage_end = object_match.start() + balloon_match.end("passage")
            identity = f"{acquisition.receipt.document_hash}\n{passage_start}\n{area}\n{period}"
            records.append(PublicRainfallRecord(
                hashlib.sha256(identity.encode()).hexdigest(), area, period,
                float(metrics.group("departure")), float(metrics.group("actual")), float(metrics.group("normal")),
                passage, passage_start, passage_end, acquisition.receipt.acquisition_id,
                acquisition.receipt.document_hash, acquisition.receipt.source_url,
            ))
        if not records:
            raise ValueError("official rainfall page contained no parseable map records")
        return PublicRainfallRecordPreview(
            acquisition.receipt.acquisition_id, extraction_receipt.extraction_id, period, tuple(records),
        )

    @staticmethod
    def _validate(acquisition, extraction):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        if not isinstance(extraction, PublicDocumentExtractionReceipt):
            raise ValueError("extraction_receipt must be a PublicDocumentExtractionReceipt")
        receipt = acquisition.receipt
        if acquisition.source.source_id != "IMD" or acquisition.source.source_type != "WEATHER_AUTHORITY":
            raise ValueError("rainfall record extraction requires the configured IMD authority")
        if receipt.status != PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None:
            raise ValueError("rainfall extraction requires a retrieved page")
        if hashlib.sha256(acquisition.document_bytes).hexdigest() != receipt.document_hash:
            raise ValueError("rainfall page bytes do not match acquisition receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED, PublicDocumentExtractionStatus.PARTIAL):
            raise ValueError("rainfall extraction requires a usable audited HTML extraction")
        if extraction.acquisition_id != receipt.acquisition_id or extraction.document_hash != receipt.document_hash:
            raise ValueError("HTML extraction receipt does not bind to rainfall page")
        if extraction.acquisition_fingerprint != PublicSourceAcquisitionLedger.receipt_fingerprint(receipt):
            raise ValueError("HTML extraction receipt has a stale acquisition fingerprint")
        media = (receipt.content_type or "").split(";", 1)[0].strip().casefold()
        if media not in ("text/html", "application/xhtml+xml"):
            raise ValueError("rainfall record extraction requires HTML")

    @staticmethod
    def _encoding(acquisition):
        match = re.search(r"charset=([^;\s]+)", acquisition.receipt.content_type or "", re.I)
        return match.group(1).strip('"\'') if match else "utf-8"


__all__ = ["TrustedPublicRainfallRecordExtractor"]
