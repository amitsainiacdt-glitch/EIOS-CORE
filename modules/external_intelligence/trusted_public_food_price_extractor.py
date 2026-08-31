"""Hash-bound extraction of official Consumer Affairs price comparisons."""

import hashlib
import re
from html.parser import HTMLParser

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_food_price_comparison_record import PublicFoodPriceComparisonPreview, PublicFoodPriceComparisonRecord
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self._row=None; self._cell=None
    def handle_starttag(self, tag, attrs):
        if tag.casefold()=="tr": self._row=[]
        elif tag.casefold() in ("td","th") and self._row is not None: self._cell=[]
    def handle_data(self, data):
        if self._cell is not None: self._cell.append(data)
    def handle_endtag(self, tag):
        if tag.casefold() in ("td","th") and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split())); self._cell=None
        elif tag.casefold()=="tr" and self._row is not None:
            if self._row: self.rows.append(tuple(self._row))
            self._row=None


class TrustedPublicFoodPriceExtractor:
    VALUE=re.compile(r"^\s*(?P<price>\d+(?:\.\d+)?)\s*(?:\(\s*(?P<pct>[+-]?\d+(?:\.\d+)?)\s*%?\s*\))?\s*$")
    DATE=re.compile(r"(?:Date|As\s+on)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",re.I)

    def extract(self, acquisition, extraction_receipt, *, market_level="RETAIL", minimum_records=5):
        self._validate(acquisition,extraction_receipt)
        market=market_level.upper()
        if market not in ("RETAIL","WHOLESALE"): raise ValueError("market level must be RETAIL or WHOLESALE")
        html=acquisition.document_bytes.decode(self._encoding(acquisition),errors="replace")
        compact=" ".join(re.sub(r"<[^>]+>"," ",html).split())
        if not re.search(r"Department\s+(?:Of|of)\s+Consumer\s+Affairs",compact,re.I) or not re.search(r"Price\s+Monitoring\s+Division",compact,re.I):
            raise ValueError("page is not attributed to the Consumer Affairs Price Monitoring Division")
        expected="Daily Average Retail Prices" if market=="RETAIL" else "Daily Average Wholesale Prices"
        if expected.casefold() not in compact.casefold(): raise ValueError(f"page is not the expected {market.lower()} report")
        date=self.DATE.search(compact)
        if not date: raise ValueError("reporting date was not found")
        parser=_TableParser(); parser.feed(html); records=[]; seen=set()
        for row in parser.rows:
            parsed=self._parse_row(row)
            if parsed is None: continue
            commodity,current,comparisons=parsed
            key=commodity.casefold()
            if key in seen: raise ValueError(f"duplicate commodity row: {commodity}")
            seen.add(key); self._reconcile(current,comparisons,commodity)
            identity=f"{acquisition.receipt.document_hash}\n{market}\n{'|'.join(row)}"
            flat=[]
            for price,pct in comparisons: flat.extend((price,pct))
            records.append(PublicFoodPriceComparisonRecord(hashlib.sha256(identity.encode()).hexdigest(),market,commodity,date.group(1),"INR_PER_KG" if market=="RETAIL" else "INR_PER_QUINTAL",current,*flat,row,acquisition.receipt.acquisition_id,acquisition.receipt.document_hash,acquisition.receipt.source_url))
        if len(records)<minimum_records: raise ValueError(f"only {len(records)} valid commodity rows found; expected at least {minimum_records}")
        return PublicFoodPriceComparisonPreview(acquisition.receipt.acquisition_id,extraction_receipt.extraction_id,tuple(records))

    def _parse_row(self,row):
        # Optional serial-number column, commodity, current, then five comparison cells.
        cells=list(row); start=1 if cells and re.fullmatch(r"\d+",cells[0]) else 0
        if len(cells)-start<7: return None
        commodity=cells[start].strip(); current=self._value(cells[start+1])
        comparisons=[self._value(cell,allow_missing=True) for cell in cells[start+2:start+7]]
        if not commodity or current is None or isinstance(current,tuple): return None
        return commodity,current,comparisons

    def _value(self,text,allow_missing=False):
        if text.strip() in ("--","-",""): return (None,None) if allow_missing else None
        match=self.VALUE.match(text.replace(",",""))
        if not match: return None if not allow_missing else (None,None)
        price=float(match.group("price")); pct=float(match.group("pct")) if match.group("pct") is not None else None
        return (price,pct) if allow_missing else price

    @staticmethod
    def _reconcile(current,comparisons,commodity):
        for prior,pct in comparisons:
            if prior is None or pct is None: continue
            calculated=100*(current/prior-1)
            if abs(calculated-pct)>0.08: raise ValueError(f"published percentage does not reconcile for {commodity}")

    @staticmethod
    def _validate(acquisition,extraction):
        if not isinstance(acquisition,TrustedPublicAcquisitionResult): raise ValueError("acquisition must be trusted")
        if not isinstance(extraction,PublicDocumentExtractionReceipt): raise ValueError("extraction receipt is required")
        receipt=acquisition.receipt
        if acquisition.source.source_id!="CONSUMER_AFFAIRS_PRICES" or acquisition.source.source_type!="FOOD_PRICE_AUTHORITY": raise ValueError("price extraction requires Consumer Affairs price authority")
        if receipt.status!=PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None: raise ValueError("price extraction requires retrieved HTML")
        if hashlib.sha256(acquisition.document_bytes).hexdigest()!=receipt.document_hash: raise ValueError("price page bytes do not match receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED,PublicDocumentExtractionStatus.PARTIAL): raise ValueError("price extraction requires usable audited HTML")
        if extraction.acquisition_id!=receipt.acquisition_id or extraction.document_hash!=receipt.document_hash: raise ValueError("extraction receipt does not bind to price page")
        if extraction.acquisition_fingerprint!=PublicSourceAcquisitionLedger.receipt_fingerprint(receipt): raise ValueError("extraction receipt has stale acquisition fingerprint")
        if (receipt.content_type or "").split(";",1)[0].strip().casefold() not in ("text/html","application/xhtml+xml"): raise ValueError("price extraction requires HTML")
    @staticmethod
    def _encoding(acquisition):
        match=re.search(r"charset=([^;\s]+)",acquisition.receipt.content_type or "",re.I); return match.group(1).strip('"\'') if match else "utf-8"


__all__=["TrustedPublicFoodPriceExtractor"]
