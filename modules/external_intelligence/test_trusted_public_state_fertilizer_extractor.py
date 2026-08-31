from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition,TrustedPublicSourceRegistry
from modules.external_intelligence.trusted_public_state_fertilizer_extractor import TrustedPublicStateFertilizerExtractor


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory); now=datetime(2026,8,31,tzinfo=timezone.utc)
        def row(number,state):
            values=(3.80,6.78,2.96,3.81,0.82,1.81,0.91,0.91,0.41,0.75,0.33,0.42,2.21,6.85,2.81,4.04)
            return "<tr><td>%s</td><td>%s</td>%s</tr>"%(number,state,"".join(f"<td>{v:.2f}</td>" for v in values))
        html="<h1>Department of Fertilizers</h1><h2>STATE WISE REQUIREMENT, AVAILABILITY & SALES & CLOSING STOCK OF FERTILIZERS DURING THE ONGOING KHARIF 2026 (FROM 01.04.26 TO 29.07.26)</h2><table>"+row(1,"Alpha")+row(2,"Beta")+"</table>"
        body=html.encode(); registry=TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("PIB","PIB",("pib.example",),source_type="GOVERNMENT_RELEASE_AUTHORITY"),))
        ledger=PublicSourceAcquisitionLedger(root/"a.jsonl"); receipt=ledger.record(acquisition_id="A",cycle_id="C",job_id="J",research_intent="FERTILIZER_MARKET_MONITORING",source_url="https://pib.example/release",status="RETRIEVED",requested_at=now,completed_at=now,http_status=200,content_type="text/html",document_hash=sha256(body).hexdigest(),bytes_received=len(body),recorder="test")
        acquisition=TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url),receipt,RetrievedContent(receipt.source_url,200,html,"text/html",{}),body)
        extraction=PublicDocumentExtractionLedger(root/"e.jsonl").record(receipt,extraction_id="E",extraction_method="deterministic_html_text_v1",status="SUCCEEDED",extracted_content="state fertilizer table",extracted_at=now,recorder="test")
        preview=TrustedPublicStateFertilizerExtractor(minimum_states=2).extract(acquisition,extraction)
        assert len(preview.records)==8 and {item.state for item in preview.records}=={"Alpha","Beta"}
        assert {item.geography_scope for item in preview.records}=={"STATE"}
        assert next(item for item in preview.records if item.state=="Alpha" and item.product=="DAP").dbt_sales==0.91
        altered=TrustedPublicAcquisitionResult(acquisition.source,receipt,acquisition.retrieved_content,body+b"x")
        try: TrustedPublicStateFertilizerExtractor(minimum_states=2).extract(altered,extraction)
        except ValueError as exc: assert "bytes" in str(exc)
        else: raise AssertionError("altered state fertilizer release accepted")
    print("TRUSTED PUBLIC STATE FERTILIZER EXTRACTOR: ALL TESTS PASSED")


if __name__=="__main__": main()
