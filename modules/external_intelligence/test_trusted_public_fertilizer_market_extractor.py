"""Offline checks for the official fertilizer-market table extractor."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_fertilizer_market_extractor import TrustedPublicFertilizerMarketExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory); now=datetime(2026,8,31,tzinfo=timezone.utc)
        html='''<h1>Ministry of Chemicals and Fertilizers</h1><h2>FERTILIZERS DURING THE ONGOING KHARIF 2026 (FROM 01.04.26 TO 19.07.26)</h2><table>
        <tr><th>No</th><th>Product</th><th>Requirement</th><th>Availability</th><th>DBT Sales</th><th>Closing</th></tr>
        <tr><td>1</td><td>UREA</td><td>109.40</td><td>163.78</td><td>94.78</td><td>69.01</td></tr>
        <tr><td>2</td><td>DAP</td><td>31.57</td><td>39.54</td><td>22.82</td><td>16.72</td></tr>
        <tr><td>3</td><td>MOP</td><td>10.06</td><td>13.81</td><td>5.20</td><td>8.63</td></tr>
        <tr><td>4</td><td>NPKS</td><td>48.48</td><td>84.57</td><td>39.36</td><td>45.21</td></tr></table>
        <h2>FERTILIZERS DURING THE FY 2025-26</h2><table><tr><td>UREA</td><td>381.45</td><td>450.79</td><td>396.60</td><td>54.22</td></tr></table>'''
        body=html.encode(); registry=TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("PIB","PIB",("pib.example",),source_type="GOVERNMENT_RELEASE_AUTHORITY"),))
        ledger=PublicSourceAcquisitionLedger(root/"a.jsonl"); receipt=ledger.record(acquisition_id="A",cycle_id="C",job_id="J",research_intent="FERTILIZER_MARKET_MONITORING",source_url="https://pib.example/release",status="RETRIEVED",requested_at=now,completed_at=now,http_status=200,content_type="text/html",document_hash=sha256(body).hexdigest(),bytes_received=len(body),recorder="test")
        acquisition=TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url),receipt,RetrievedContent(receipt.source_url,200,html,"text/html",{}),body)
        extraction=PublicDocumentExtractionLedger(root/"e.jsonl").record(receipt,extraction_id="E",extraction_method="deterministic_html_text_v1",status="SUCCEEDED",extracted_content="fertilizer table",extracted_at=now,recorder="test")
        preview=TrustedPublicFertilizerMarketExtractor().extract(acquisition,extraction)
        assert preview.period_label=="01.04.26 TO 19.07.26" and len(preview.records)==4
        urea=next(item for item in preview.records if item.product=="UREA")
        assert urea.requirement==109.40 and urea.closing_stock==69.01 and not preview.creates_observation
        altered=TrustedPublicAcquisitionResult(acquisition.source,receipt,acquisition.retrieved_content,body+b"x")
        try: TrustedPublicFertilizerMarketExtractor().extract(altered,extraction)
        except ValueError as exc: assert "bytes" in str(exc)
        else: raise AssertionError("altered fertilizer release accepted")
    print("TRUSTED PUBLIC FERTILIZER MARKET EXTRACTOR: ALL TESTS PASSED")


if __name__=="__main__": main()
