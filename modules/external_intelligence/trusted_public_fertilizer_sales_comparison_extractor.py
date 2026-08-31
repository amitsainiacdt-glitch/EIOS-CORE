"""Hash-bound extraction of an explicit corresponding-period fertilizer comparison."""

import hashlib, re

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_fertilizer_sales_comparison import PublicFertilizerSalesComparison, PublicFertilizerSalesComparisonPreview
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


class TrustedPublicFertilizerSalesComparisonExtractor:
    COMPARISON=re.compile(
        r"During\s+the\s+ongoing\s+Kharif\s+2026\s+season\s*\([^)]*?(?P<end>\d{1,2}\s+July\s+2026)\)\s*,?\s*"
        r"total\s+consumption\s+of\s+major\s+fertilizers[^.]{0,160}?stood\s+at\s+(?P<current>\d+(?:\.\d+)?)\s*LMT\s*,?\s*"
        r"compared\s+to\s+(?P<prior>\d+(?:\.\d+)?)\s*LMT\s+during\s+the\s+corresponding\s+period\s+of\s+Kharif\s+2025",
        re.I | re.S,
    )

    def extract(self, acquisition, extraction_receipt):
        self._validate(acquisition,extraction_receipt)
        html=acquisition.document_bytes.decode(self._encoding(acquisition),errors="replace")
        plain=" ".join(re.sub(r"<[^>]+>"," ",html).split())
        if "Ministry of Chemicals and Fertilizers" not in plain: raise ValueError("release is not attributed to the fertilizer ministry")
        match=self.COMPARISON.search(plain)
        if not match: raise ValueError("explicit corresponding-period fertilizer comparison was not found")
        current=float(match.group("current")); prior=float(match.group("prior"))
        if current<=0 or prior<=0: raise ValueError("fertilizer consumption values must be positive")
        passage=match.group(0); identity=f"{acquisition.receipt.document_hash}\n{match.start()}\n{passage}"
        comparison=PublicFertilizerSalesComparison(
            hashlib.sha256(identity.encode()).hexdigest(),f"KHARIF 2026 THROUGH {match.group('end').upper()}",
            f"CORRESPONDING KHARIF 2025 PERIOD",current,prior,round(100*(current-prior)/prior,2),
            passage,match.start(),match.end(),acquisition.receipt.acquisition_id,acquisition.receipt.document_hash,acquisition.receipt.source_url,
        )
        return PublicFertilizerSalesComparisonPreview(acquisition.receipt.acquisition_id,extraction_receipt.extraction_id,comparison)

    @staticmethod
    def _validate(acquisition,extraction):
        if not isinstance(acquisition,TrustedPublicAcquisitionResult): raise ValueError("acquisition must be trusted")
        if not isinstance(extraction,PublicDocumentExtractionReceipt): raise ValueError("extraction receipt is required")
        receipt=acquisition.receipt
        if acquisition.source.source_id!="PIB" or acquisition.source.source_type!="GOVERNMENT_RELEASE_AUTHORITY": raise ValueError("fertilizer comparison requires PIB authority")
        if receipt.status!=PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None: raise ValueError("fertilizer comparison requires retrieved HTML")
        if hashlib.sha256(acquisition.document_bytes).hexdigest()!=receipt.document_hash: raise ValueError("fertilizer release bytes do not match receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED,PublicDocumentExtractionStatus.PARTIAL): raise ValueError("fertilizer comparison requires usable audited HTML")
        if extraction.acquisition_id!=receipt.acquisition_id or extraction.document_hash!=receipt.document_hash: raise ValueError("extraction receipt does not bind to fertilizer release")
        if extraction.acquisition_fingerprint!=PublicSourceAcquisitionLedger.receipt_fingerprint(receipt): raise ValueError("extraction receipt has stale acquisition fingerprint")
        if (receipt.content_type or "").split(";",1)[0].strip().casefold() not in ("text/html","application/xhtml+xml"): raise ValueError("fertilizer comparison requires HTML")

    @staticmethod
    def _encoding(acquisition):
        match=re.search(r"charset=([^;\s]+)",acquisition.receipt.content_type or "",re.I)
        return match.group(1).strip('"\'') if match else "utf-8"


__all__=["TrustedPublicFertilizerSalesComparisonExtractor"]
