from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_foodgrain_buffer_extractor import TrustedPublicFoodgrainBufferExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition,TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory); now=datetime(2026,8,31,tzinfo=timezone.utc)
        html="""<h1>Ministry of Consumer Affairs, Food and Public distribution</h1><p>As on 28 May 2026, wheat stock in the Central Pool stood at 513 Lakh Metric Tonnes (LMT) against the prescribed buffer norm of 275.80 LMT for 1 July.</p><p>Rice stock in the Central Pool stood at 397 LMT against the prescribed buffer norm of 135.40 LMT for 1 July. In addition, around 298 LMT of procured paddy is yet to be milled and added to rice stocks.</p>"""; body=html.encode()
        registry=TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("PIB","PIB",("pib.example",),source_type="GOVERNMENT_RELEASE_AUTHORITY"),)); ledger=PublicSourceAcquisitionLedger(root/"a.jsonl")
        receipt=ledger.record(acquisition_id="A",cycle_id="C",job_id="J",research_intent="FOOD_STOCK_MONITORING",source_url="https://pib.example/release",status="RETRIEVED",requested_at=now,completed_at=now,http_status=200,content_type="text/html",document_hash=sha256(body).hexdigest(),bytes_received=len(body),recorder="test")
        acquisition=TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url),receipt,RetrievedContent(receipt.source_url,200,html,"text/html",{}),body); extraction=PublicDocumentExtractionLedger(root/"e.jsonl").record(receipt,extraction_id="E",extraction_method="deterministic_html_text_v1",status="SUCCEEDED",extracted_content="food stocks",extracted_at=now,recorder="test")
        preview=TrustedPublicFoodgrainBufferExtractor().extract(acquisition,extraction); assert len(preview.records)==2
        rice=next(item for item in preview.records if item.grain=="RICE"); assert rice.stock_to_norm_percent==293.21 and rice.additional_unmilled_paddy_lmt==298
        assert not preview.creates_observation
        altered=TrustedPublicAcquisitionResult(acquisition.source,receipt,acquisition.retrieved_content,body+b"x")
        try: TrustedPublicFoodgrainBufferExtractor().extract(altered,extraction)
        except ValueError as exc: assert "bytes" in str(exc)
        else: raise AssertionError("altered foodgrain release accepted")
    print("TRUSTED PUBLIC FOODGRAIN BUFFER EXTRACTOR: ALL TESTS PASSED")


if __name__=="__main__": main()
