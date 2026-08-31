"""Hash-bound state-by-product extraction from an official Kharif table."""

import hashlib, re
from html import unescape
from html.parser import HTMLParser

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.public_state_fertilizer_record import PublicStateFertilizerPreview, PublicStateFertilizerRecord
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class _Rows(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.rows=[]; self.row=[]; self.cell=[]; self.in_row=False; self.in_cell=False
    def handle_starttag(self,tag,attrs):
        if tag.casefold()=="tr": self.in_row=True; self.row=[]
        elif tag.casefold() in ("td","th") and self.in_row: self.in_cell=True; self.cell=[]
    def handle_data(self,data):
        if self.in_cell: self.cell.append(data)
    def handle_endtag(self,tag):
        tag=tag.casefold()
        if tag in ("td","th") and self.in_cell: self.row.append(" ".join("".join(self.cell).split())); self.in_cell=False
        elif tag=="tr" and self.in_row:
            if self.row: self.rows.append(tuple(self.row))
            self.in_row=False


class TrustedPublicStateFertilizerExtractor:
    PERIOD=re.compile(r"FROM\s+(\d{2}\.\d{2}\.\d{2,4})\s+TO\s+(\d{2}\.\d{2}\.\d{2,4})",re.I)
    NUMBER=re.compile(r"^\d+(?:\.\d+)?$"); PRODUCTS=("UREA","DAP","MOP","NPKS")

    def __init__(self,minimum_states=20):
        if isinstance(minimum_states,bool) or not isinstance(minimum_states,int) or minimum_states<=0: raise ValueError("minimum_states must be positive")
        self.minimum_states=minimum_states

    def extract(self,acquisition,extraction_receipt):
        self._validate(acquisition,extraction_receipt)
        html=acquisition.document_bytes.decode(self._encoding(acquisition),errors="replace")
        plain=" ".join(unescape(re.sub(r"<[^>]+>"," ",html)).split())
        if "Department of Fertilizers" not in plain: raise ValueError("release is not attributed to the Department of Fertilizers")
        heading=re.search(r"STATE\s+WISE\s+REQUIREMENT\s*[,|&]?\s*AVAILABILITY\s*[,|&]?\s*SALES\s*&?\s*CLOSING\s+STOCK.*?ONGOING\s+KHARIF\s+2026",plain,re.I)
        period_match=self.PERIOD.search(plain)
        if not heading or not period_match: raise ValueError("state fertilizer table or reporting period was not found")
        period=f"{period_match.group(1)} TO {period_match.group(2)}"
        parser=_Rows(); parser.feed(html); records=[]; seen=set(); states=set()
        for row in parser.rows:
            if len(row)<18: continue
            state_candidates=[(i,value) for i,value in enumerate(row) if value and not self.NUMBER.fullmatch(value)]
            if not state_candidates: continue
            state_index,state=state_candidates[-1]
            values=[float(value) for value in row[state_index+1:] if self.NUMBER.fullmatch(value)]
            if len(values)!=16: continue
            source_row=" | ".join(row); state_records=[]
            for product,offset in zip(self.PRODUCTS,range(0,16,4)):
                requirement,availability,sales,closing=values[offset:offset+4]
                if abs((availability-sales)-closing)>0.06: raise ValueError(f"state fertilizer stock reconciliation failed for {state} {product}")
                identity=f"{acquisition.receipt.document_hash}\n{period}\n{state}\n{product}\n{source_row}"; record_id=hashlib.sha256(identity.encode()).hexdigest()
                if record_id in seen: continue
                seen.add(record_id); state_records.append(PublicStateFertilizerRecord(record_id,state,"ALL_INDIA" if state.casefold()=="all india" else "STATE",product,period,"LMT",requirement,availability,sales,closing,source_row,acquisition.receipt.acquisition_id,acquisition.receipt.document_hash,acquisition.receipt.source_url))
            if len(state_records)==4: states.add(state); records.extend(state_records)
        if len(states)<self.minimum_states: raise ValueError(f"state fertilizer table contained only {len(states)} complete states")
        if len(records)!=len(states)*4: raise ValueError("each state must contain exactly four fertilizer products")
        return PublicStateFertilizerPreview(acquisition.receipt.acquisition_id,extraction_receipt.extraction_id,period,tuple(records))

    @staticmethod
    def _validate(acquisition,extraction):
        if not isinstance(acquisition,TrustedPublicAcquisitionResult): raise ValueError("acquisition must be trusted")
        if not isinstance(extraction,PublicDocumentExtractionReceipt): raise ValueError("extraction receipt is required")
        receipt=acquisition.receipt
        if acquisition.source.source_id!="PIB" or acquisition.source.source_type!="GOVERNMENT_RELEASE_AUTHORITY": raise ValueError("state fertilizer extraction requires PIB authority")
        if receipt.status!=PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None: raise ValueError("state fertilizer extraction requires retrieved HTML")
        if hashlib.sha256(acquisition.document_bytes).hexdigest()!=receipt.document_hash: raise ValueError("state fertilizer bytes do not match receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED,PublicDocumentExtractionStatus.PARTIAL): raise ValueError("state fertilizer extraction requires usable audited HTML")
        if extraction.acquisition_id!=receipt.acquisition_id or extraction.document_hash!=receipt.document_hash: raise ValueError("extraction receipt does not bind to state fertilizer release")
        if extraction.acquisition_fingerprint!=PublicSourceAcquisitionLedger.receipt_fingerprint(receipt): raise ValueError("extraction receipt has stale acquisition fingerprint")
        if (receipt.content_type or "").split(";",1)[0].strip().casefold() not in ("text/html","application/xhtml+xml"): raise ValueError("state fertilizer extraction requires HTML")
    @staticmethod
    def _encoding(acquisition):
        match=re.search(r"charset=([^;\s]+)",acquisition.receipt.content_type or "",re.I); return match.group(1).strip('"\'') if match else "utf-8"


__all__=["TrustedPublicStateFertilizerExtractor"]
