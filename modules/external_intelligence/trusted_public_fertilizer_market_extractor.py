"""Hash-bound structured extraction of an official Kharif fertilizer table."""

import hashlib
import re
from html.parser import HTMLParser

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_fertilizer_market_record import PublicFertilizerMarketPreview, PublicFertilizerMarketRecord
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class _Rows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.rows=[]; self.row=[]; self.cell=[]; self.in_row=False; self.in_cell=False
    def handle_starttag(self, tag, attrs):
        if tag.casefold()=="tr": self.in_row=True; self.row=[]
        elif tag.casefold() in ("td","th") and self.in_row: self.in_cell=True; self.cell=[]
    def handle_data(self, data):
        if self.in_cell: self.cell.append(data)
    def handle_endtag(self, tag):
        tag=tag.casefold()
        if tag in ("td","th") and self.in_cell: self.row.append(" ".join("".join(self.cell).split())); self.in_cell=False
        elif tag=="tr" and self.in_row:
            if self.row: self.rows.append(tuple(self.row))
            self.in_row=False


class TrustedPublicFertilizerMarketExtractor:
    PERIOD = re.compile(r"FROM\s+(\d{2}\.\d{2}\.\d{2})\s+TO\s+(\d{2}\.\d{2}\.\d{2})", re.I)
    NUMBER = re.compile(r"^\d+(?:\.\d+)?$")
    PRODUCTS = {"UREA", "DAP", "MOP", "NPKS"}

    def extract(self, acquisition, extraction_receipt):
        self._validate(acquisition, extraction_receipt)
        html = acquisition.document_bytes.decode(self._encoding(acquisition), errors="replace")
        plain = " ".join(re.sub(r"<[^>]+>", " ", html).split())
        if "Ministry of Chemicals and Fertilizers" not in plain:
            raise ValueError("release is not attributed to the fertilizer ministry")
        start_match = re.search(r"FERTILIZERS DURING THE ONGOING KHARIF 2026", html, re.I)
        if not start_match: raise ValueError("ongoing Kharif fertilizer section was not found")
        end_match = re.search(r"FERTILIZERS DURING THE FY", html[start_match.end():], re.I)
        end = start_match.end() + end_match.start() if end_match else len(html)
        section = html[start_match.start():end]
        section_plain = " ".join(re.sub(r"<[^>]+>", " ", section).split())
        period_match = self.PERIOD.search(section_plain)
        if not period_match: raise ValueError("Kharif fertilizer reporting period was not found")
        period = f"{period_match.group(1)} TO {period_match.group(2)}"
        parser=_Rows(); parser.feed(section); records=[]; seen=set()
        for row in parser.rows:
            product = next((value.upper() for value in row if value.upper() in self.PRODUCTS), None)
            if product is None: continue
            product_index = next(index for index,value in enumerate(row) if value.upper()==product)
            values=[float(value) for value in row[product_index+1:] if self.NUMBER.fullmatch(value)]
            if len(values) < 4: continue
            requirement, availability, sales, closing = values[:4]
            if abs((availability-sales)-closing) > 0.05:
                raise ValueError(f"fertilizer stock reconciliation failed for {product}")
            source_row=" | ".join(row); identity=f"{acquisition.receipt.document_hash}\n{period}\n{source_row}"
            record_id=hashlib.sha256(identity.encode()).hexdigest()
            if record_id in seen: continue
            seen.add(record_id)
            records.append(PublicFertilizerMarketRecord(record_id,product,period,"LMT",requirement,availability,sales,closing,source_row,acquisition.receipt.acquisition_id,acquisition.receipt.document_hash,acquisition.receipt.source_url))
        if {item.product for item in records} != self.PRODUCTS:
            raise ValueError("Kharif fertilizer table must contain exactly UREA, DAP, MOP, and NPKS")
        return PublicFertilizerMarketPreview(acquisition.receipt.acquisition_id, extraction_receipt.extraction_id, period, tuple(sorted(records,key=lambda item:item.product)))

    @staticmethod
    def _validate(acquisition, extraction):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult): raise ValueError("acquisition must be trusted")
        if not isinstance(extraction, PublicDocumentExtractionReceipt): raise ValueError("extraction receipt is required")
        receipt=acquisition.receipt
        if acquisition.source.source_id!="PIB" or acquisition.source.source_type!="GOVERNMENT_RELEASE_AUTHORITY": raise ValueError("fertilizer extraction requires PIB authority")
        if receipt.status!=PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None: raise ValueError("fertilizer extraction requires retrieved HTML")
        if hashlib.sha256(acquisition.document_bytes).hexdigest()!=receipt.document_hash: raise ValueError("fertilizer release bytes do not match receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED,PublicDocumentExtractionStatus.PARTIAL): raise ValueError("fertilizer extraction requires usable audited HTML")
        if extraction.acquisition_id!=receipt.acquisition_id or extraction.document_hash!=receipt.document_hash: raise ValueError("extraction receipt does not bind to fertilizer release")
        if extraction.acquisition_fingerprint!=PublicSourceAcquisitionLedger.receipt_fingerprint(receipt): raise ValueError("extraction receipt has stale acquisition fingerprint")
        if (receipt.content_type or "").split(";",1)[0].strip().casefold() not in ("text/html","application/xhtml+xml"): raise ValueError("fertilizer extraction requires HTML")

    @staticmethod
    def _encoding(acquisition):
        match=re.search(r"charset=([^;\s]+)",acquisition.receipt.content_type or "",re.I)
        return match.group(1).strip('"\'') if match else "utf-8"


__all__=["TrustedPublicFertilizerMarketExtractor"]
