"""Hash-bound table extraction for official Kharif crop-area releases."""

import hashlib
import re
from html.parser import HTMLParser

from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview, PublicCropAreaRecord
from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class _TableRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell, self.in_row, self.in_cell = [], [], [], False, False

    def handle_starttag(self, tag, attrs):
        if tag.casefold() == "tr": self.in_row, self.row = True, []
        elif tag.casefold() in ("td", "th") and self.in_row: self.in_cell, self.cell = True, []

    def handle_data(self, data):
        if self.in_cell: self.cell.append(data)

    def handle_endtag(self, tag):
        tag = tag.casefold()
        if tag in ("td", "th") and self.in_cell:
            self.row.append(" ".join("".join(self.cell).split())); self.in_cell = False
        elif tag == "tr" and self.in_row:
            if self.row: self.rows.append(tuple(self.row))
            self.in_row = False


class TrustedPublicCropAreaExtractor:
    PERIOD = re.compile(
        r"(?:area coverage|area sown report).*?as on\s+"
        r"(\d{4}[./-]\d{1,2}[./-]\d{1,2}|\d{1,2}[./-]\d{1,2}[./-]\d{4})",
        re.I | re.S,
    )
    NUMBER = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
    CROP_ALIASES = {
        "pulses": "Total Pulses", "total pulses": "Total Pulses",
        "oilseeds": "Total Oilseeds", "total oilseeds": "Total Oilseeds",
        "shri anna cum coarse cereals": "Shri Anna cum Coarse Cereals",
        "total": "Grand Total", "grand total": "Grand Total",
        "arhar": "Tur", "tur": "Tur", "urdbean": "Urad", "urd bean": "Urad", "urad": "Urad",
        "moongbean": "Moong", "moong bean": "Moong", "moong": "Moong",
        "mothbean": "Moth Bean", "moth bean": "Moth Bean", "bajra**": "Bajra", "bajra": "Bajra",
        "niger": "Nigerseed", "nigerseed": "Nigerseed", "castor": "Castorseed", "castorseed": "Castorseed",
        "jute & mesta": "Total Jute and Mesta", "total jute and mesta": "Total Jute and Mesta",
    }

    def extract(self, acquisition, extraction_receipt):
        self._validate(acquisition, extraction_receipt)
        html = acquisition.document_bytes.decode(self._encoding(acquisition), errors="replace")
        plain = " ".join(re.sub(r"<[^>]+>", " ", html).split())
        if "Ministry of Agriculture" not in plain:
            raise ValueError("release is not attributed to the Ministry of Agriculture")
        period_match = self.PERIOD.search(plain)
        if not period_match:
            raise ValueError("crop-area reporting period was not found")
        period = period_match.group(1)
        parser = _TableRows(); parser.feed(html)
        records, seen_rows = [], set()
        for row in parser.rows:
            numeric = [(index, float(value.replace(",", ""))) for index, value in enumerate(row) if self.NUMBER.fullmatch(value.replace(",", ""))]
            if len(numeric) < 4:
                continue
            crop_indexes = [index for index, value in enumerate(row) if value and not self.NUMBER.fullmatch(value.replace(",", ""))]
            if not crop_indexes:
                continue
            crop_index = crop_indexes[-1]
            values = [value for index, value in numeric if index > crop_index]
            if len(values) < 4:
                continue
            names = [row[crop_index]]
            if not names:
                continue
            crop = self.CROP_ALIASES.get(names[-1].casefold(), names[-1])
            normal, current, prior, difference = values[0], values[-3], values[-2], values[-1]
            if abs((current - prior) - difference) > 0.02:
                raise ValueError(f"crop-area arithmetic mismatch for {crop}")
            source_row = " | ".join(row)
            identity = f"{acquisition.receipt.document_hash}\n{period}\n{source_row}"
            record_id = hashlib.sha256(identity.encode()).hexdigest()
            if record_id in seen_rows:
                continue
            seen_rows.add(record_id)
            records.append(PublicCropAreaRecord(
                record_id, crop, period, "LAKH_HECTARE",
                normal, current, prior, difference, source_row,
                acquisition.receipt.acquisition_id, acquisition.receipt.document_hash,
                acquisition.receipt.source_url,
            ))
        if not records:
            raise ValueError("official release contained no internally consistent crop-area rows")
        return PublicCropAreaPreview(acquisition.receipt.acquisition_id, extraction_receipt.extraction_id, period, tuple(records))

    @staticmethod
    def _validate(acquisition, extraction):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult): raise ValueError("acquisition must be trusted")
        if not isinstance(extraction, PublicDocumentExtractionReceipt): raise ValueError("extraction receipt is required")
        receipt = acquisition.receipt
        if acquisition.source.source_id != "PIB" or acquisition.source.source_type != "GOVERNMENT_RELEASE_AUTHORITY":
            raise ValueError("crop-area extraction requires the configured PIB authority")
        if receipt.status != PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None:
            raise ValueError("crop-area extraction requires a retrieved release")
        if hashlib.sha256(acquisition.document_bytes).hexdigest() != receipt.document_hash:
            raise ValueError("crop-area release bytes do not match acquisition receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED, PublicDocumentExtractionStatus.PARTIAL):
            raise ValueError("crop-area extraction requires usable audited HTML")
        if extraction.acquisition_id != receipt.acquisition_id or extraction.document_hash != receipt.document_hash:
            raise ValueError("extraction receipt does not bind to crop-area release")
        if extraction.acquisition_fingerprint != PublicSourceAcquisitionLedger.receipt_fingerprint(receipt):
            raise ValueError("extraction receipt has a stale acquisition fingerprint")
        if (receipt.content_type or "").split(";", 1)[0].strip().casefold() not in ("text/html", "application/xhtml+xml"):
            raise ValueError("crop-area extraction requires HTML")

    @staticmethod
    def _encoding(acquisition):
        match = re.search(r"charset=([^;\s]+)", acquisition.receipt.content_type or "", re.I)
        return match.group(1).strip('"\'') if match else "utf-8"


__all__ = ["TrustedPublicCropAreaExtractor"]
