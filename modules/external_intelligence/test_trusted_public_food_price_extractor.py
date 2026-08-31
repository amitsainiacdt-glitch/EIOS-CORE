from datetime import datetime,timezone,date
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.food_price_transmission_readiness import assess_food_price_transmission
from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_food_price_extractor import TrustedPublicFoodPriceExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition,TrustedPublicSourceRegistry


def _fixture():
    rows=(
        ("Rice","45.53","45.08 (1.00)","45.04 (1.09)","42.99 (5.91)","42.59 (6.90)","43.74 (4.09)"),
        ("Wheat","31.80","31.75 (0.16)","31.70 (0.32)","31.65 (0.47)","31.62 (0.57)","31.50 (0.95)"),
        ("Atta","37.45","37.30 (0.40)","37.20 (0.67)","37.00 (1.22)","36.93 (1.41)","36.50 (2.60)"),
        ("Gram Dal","89.00","88.50 (0.56)","88.00 (1.14)","87.00 (2.30)","90.00 (-1.11)","92.00 (-3.26)"),
        ("Sugar","45.00","--","44.50 (1.12)","44.00 (2.27)","43.00 (4.65)","42.00 (7.14)"),
    )
    table="".join("<tr><td>%d</td>%s</tr>"%(i,"".join(f"<td>{value}</td>" for value in row)) for i,row in enumerate(rows,1))
    return f"<h1>Department Of Consumer Affairs Price Monitoring Division</h1><h2>Daily Average Retail Prices</h2><p>Date: 30/08/2026</p><table>{table}</table>"


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory); now=datetime(2026,8,31,tzinfo=timezone.utc); html=_fixture(); body=html.encode()
        registry=TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("CONSUMER_AFFAIRS_PRICES","Department of Consumer Affairs",("prices.example",),source_type="FOOD_PRICE_AUTHORITY"),)); ledger=PublicSourceAcquisitionLedger(root/"a.jsonl")
        receipt=ledger.record(acquisition_id="A",cycle_id="C",job_id="J",research_intent="FOOD_PRICE_MONITORING",source_url="https://prices.example/report",status="RETRIEVED",requested_at=now,completed_at=now,http_status=200,content_type="text/html",document_hash=sha256(body).hexdigest(),bytes_received=len(body),recorder="test")
        acquisition=TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url),receipt,RetrievedContent(receipt.source_url,200,html,"text/html",{}),body)
        extraction=PublicDocumentExtractionLedger(root/"e.jsonl").record(receipt,extraction_id="E",extraction_method="deterministic_html_table_v1",status="SUCCEEDED",extracted_content="prices",extracted_at=now,recorder="test")
        preview=TrustedPublicFoodPriceExtractor().extract(acquisition,extraction); assert len(preview.records)==5 and not preview.creates_observation and preview.requires_human_review
        rice=next(item for item in preview.records if item.commodity=="Rice"); assert rice.year_change_percent==6.9 and rice.unit=="INR_PER_KG"
        assessment=assess_food_price_transmission(rice,date(2026,8,31)); assert assessment.ready_for_meta and assessment.direction=="RISING" and len(assessment.blocked_claims)==4
        altered=TrustedPublicAcquisitionResult(acquisition.source,receipt,acquisition.retrieved_content,body+b"x")
        try: TrustedPublicFoodPriceExtractor().extract(altered,extraction)
        except ValueError as exc: assert "bytes" in str(exc)
        else: raise AssertionError("altered price page accepted")
        bad=html.replace("45.08 (1.00)","45.08 (9.00)"); bad_body=bad.encode(); bad_receipt=ledger.record(acquisition_id="B",cycle_id="C",job_id="J2",research_intent="FOOD_PRICE_MONITORING",source_url="https://prices.example/report2",status="RETRIEVED",requested_at=now,completed_at=now,http_status=200,content_type="text/html",document_hash=sha256(bad_body).hexdigest(),bytes_received=len(bad_body),recorder="test")
        bad_acquisition=TrustedPublicAcquisitionResult(registry.resolve(bad_receipt.source_url),bad_receipt,RetrievedContent(bad_receipt.source_url,200,bad,"text/html",{}),bad_body); bad_extraction=PublicDocumentExtractionLedger(root/"e.jsonl").record(bad_receipt,extraction_id="E2",extraction_method="deterministic_html_table_v1",status="SUCCEEDED",extracted_content="prices",extracted_at=now,recorder="test")
        try: TrustedPublicFoodPriceExtractor().extract(bad_acquisition,bad_extraction)
        except ValueError as exc: assert "reconcile" in str(exc)
        else: raise AssertionError("inconsistent published percentage accepted")
    print("TRUSTED PUBLIC FOOD PRICE EXTRACTOR: ALL TESTS PASSED")


if __name__=="__main__": main()
