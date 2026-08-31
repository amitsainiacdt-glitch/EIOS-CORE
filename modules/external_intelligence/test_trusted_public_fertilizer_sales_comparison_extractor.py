from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_fertilizer_sales_comparison_extractor import TrustedPublicFertilizerSalesComparisonExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory); now=datetime(2026,8,31,tzinfo=timezone.utc)
        sentence="During the ongoing Kharif 2026 season (1 April 2026 to 14 July 2026), total consumption of major fertilizers—Urea, DAP, MOP and NPKS—stood at 151.74 LMT, compared to 157.05 LMT during the corresponding period of Kharif 2025."
        html=f"<h1>Ministry of Chemicals and Fertilizers</h1><p>{sentence}</p>"; body=html.encode()
        registry=TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("PIB","PIB",("pib.example",),source_type="GOVERNMENT_RELEASE_AUTHORITY"),))
        ledger=PublicSourceAcquisitionLedger(root/"a.jsonl"); receipt=ledger.record(acquisition_id="A",cycle_id="C",job_id="J",research_intent="FERTILIZER_MARKET_MONITORING",source_url="https://pib.example/release",status="RETRIEVED",requested_at=now,completed_at=now,http_status=200,content_type="text/html",document_hash=sha256(body).hexdigest(),bytes_received=len(body),recorder="test")
        acquisition=TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url),receipt,RetrievedContent(receipt.source_url,200,html,"text/html",{}),body)
        extraction=PublicDocumentExtractionLedger(root/"e.jsonl").record(receipt,extraction_id="E",extraction_method="deterministic_html_text_v1",status="SUCCEEDED",extracted_content=sentence,extracted_at=now,recorder="test")
        preview=TrustedPublicFertilizerSalesComparisonExtractor().extract(acquisition,extraction)
        assert preview.comparison.current_consumption_lmt==151.74 and preview.comparison.prior_consumption_lmt==157.05
        assert preview.comparison.year_over_year_percent==-3.38 and not preview.creates_observation
        altered=TrustedPublicAcquisitionResult(acquisition.source,receipt,acquisition.retrieved_content,body+b"x")
        try: TrustedPublicFertilizerSalesComparisonExtractor().extract(altered,extraction)
        except ValueError as exc: assert "bytes" in str(exc)
        else: raise AssertionError("altered fertilizer comparison accepted")
    print("TRUSTED PUBLIC FERTILIZER SALES COMPARISON: ALL TESTS PASSED")


if __name__=="__main__": main()
