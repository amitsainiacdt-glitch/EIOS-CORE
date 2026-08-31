"""Hash-bound extraction of official wheat/rice stock against buffer norms."""

import hashlib,re
from html import unescape

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt,PublicDocumentExtractionStatus
from modules.external_intelligence.public_foodgrain_buffer_record import PublicFoodgrainBufferPreview,PublicFoodgrainBufferRecord
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class TrustedPublicFoodgrainBufferExtractor:
    WHEAT=re.compile(r"As\s+on\s+(?P<date>\d{1,2}\s+May\s+2026)\s*,?\s*wheat\s+stock\s+in\s+the\s+Central\s+Pool\s+stood\s+at\s+(?P<stock>\d+(?:\.\d+)?)\s+Lakh\s+Metric\s+Tonnes\s*\(LMT\)\s+against\s+the\s+prescribed\s+buffer\s+norm\s+of\s+(?P<norm>\d+(?:\.\d+)?)\s+LMT\s+for\s+(?P<normdate>1\s+July)",re.I)
    RICE=re.compile(r"Rice\s+stock\s+in\s+the\s+Central\s+Pool\s+stood\s+at\s+(?P<stock>\d+(?:\.\d+)?)\s+LMT\s+against\s+the\s+prescribed\s+buffer\s+norm\s+of\s+(?P<norm>\d+(?:\.\d+)?)\s+LMT\s+for\s+(?P<normdate>1\s+July)\.\s+In\s+addition\s*,?\s*around\s+(?P<paddy>\d+(?:\.\d+)?)\s+LMT\s+of\s+procured\s+paddy\s+is\s+yet\s+to\s+be\s+milled",re.I)

    def extract(self,acquisition,extraction_receipt):
        self._validate(acquisition,extraction_receipt)
        html=acquisition.document_bytes.decode(self._encoding(acquisition),errors="replace"); plain=" ".join(unescape(re.sub(r"<[^>]+>"," ",html)).split())
        if not re.search(r"Ministry of Consumer Affairs\s*,\s*Food\s+(?:&|and)\s+Public\s+Distribution",plain,re.I): raise ValueError("release is not attributed to the food-distribution ministry")
        wheat=self.WHEAT.search(plain); rice=self.RICE.search(plain)
        if not wheat or not rice: raise ValueError("complete wheat and rice stock-versus-norm statements were not found")
        records=[]
        for grain,match,paddy in (("WHEAT",wheat,None),("RICE",rice,float(rice.group("paddy")))):
            stock=float(match.group("stock")); norm=float(match.group("norm")); passage=match.group(0); identity=f"{acquisition.receipt.document_hash}\n{grain}\n{passage}"
            records.append(PublicFoodgrainBufferRecord(hashlib.sha256(identity.encode()).hexdigest(),grain,wheat.group("date").upper(),match.group("normdate").upper(),stock,norm,round(100*stock/norm,2),paddy,passage,acquisition.receipt.acquisition_id,acquisition.receipt.document_hash,acquisition.receipt.source_url))
        return PublicFoodgrainBufferPreview(acquisition.receipt.acquisition_id,extraction_receipt.extraction_id,tuple(records))

    @staticmethod
    def _validate(acquisition,extraction):
        if not isinstance(acquisition,TrustedPublicAcquisitionResult): raise ValueError("acquisition must be trusted")
        if not isinstance(extraction,PublicDocumentExtractionReceipt): raise ValueError("extraction receipt is required")
        receipt=acquisition.receipt
        if acquisition.source.source_id!="PIB" or acquisition.source.source_type!="GOVERNMENT_RELEASE_AUTHORITY": raise ValueError("foodgrain extraction requires PIB authority")
        if receipt.status!=PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None: raise ValueError("foodgrain extraction requires retrieved HTML")
        if hashlib.sha256(acquisition.document_bytes).hexdigest()!=receipt.document_hash: raise ValueError("foodgrain release bytes do not match receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED,PublicDocumentExtractionStatus.PARTIAL): raise ValueError("foodgrain extraction requires usable audited HTML")
        if extraction.acquisition_id!=receipt.acquisition_id or extraction.document_hash!=receipt.document_hash: raise ValueError("extraction receipt does not bind to foodgrain release")
        if extraction.acquisition_fingerprint!=PublicSourceAcquisitionLedger.receipt_fingerprint(receipt): raise ValueError("extraction receipt has stale acquisition fingerprint")
        if (receipt.content_type or "").split(";",1)[0].strip().casefold() not in ("text/html","application/xhtml+xml"): raise ValueError("foodgrain extraction requires HTML")
    @staticmethod
    def _encoding(acquisition):
        match=re.search(r"charset=([^;\s]+)",acquisition.receipt.content_type or "",re.I); return match.group(1).strip('"\'') if match else "utf-8"


__all__=["TrustedPublicFoodgrainBufferExtractor"]
