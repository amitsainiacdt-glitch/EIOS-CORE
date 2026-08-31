"""Acquire and structure official foodgrain buffers without admission."""

import argparse,json
from datetime import datetime,timezone
from pathlib import Path
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_foodgrain_buffer_extractor import TrustedPublicFoodgrainBufferExtractor
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


def main(argv=None):
    parser=argparse.ArgumentParser()
    for name in ("acquisition-id","extraction-id","cycle-id","job-id","url","acquisition-ledger-path","extraction-ledger-path","output-path","recorder"): parser.add_argument("--"+name,required=True)
    args=parser.parse_args(argv); acquisition=TrustedPublicAcquisitionAdapter(TrustedPublicSourceRegistry.india_primary_sources(),PublicSourceAcquisitionLedger(args.acquisition_ledger_path)).acquire(acquisition_id=args.acquisition_id,cycle_id=args.cycle_id,job_id=args.job_id,research_intent="FOOD_STOCK_MONITORING",url=args.url,recorder=args.recorder,requested_at=datetime.now(timezone.utc))
    if acquisition.retrieved_content is None: print(f"Acquisition blocked: {acquisition.receipt.error_message}"); return 1
    extraction=TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(args.extraction_ledger_path)).extract(acquisition,extraction_id=args.extraction_id,recorder=args.recorder)
    if extraction.extracted_text is None: print(f"Extraction blocked: {extraction.receipt.error_message}"); return 1
    preview=TrustedPublicFoodgrainBufferExtractor().extract(acquisition,extraction.receipt); payload={"schema_version":1,"acquisition_id":preview.acquisition_id,"extraction_id":preview.extraction_id,"creates_observation":False,"requires_human_review":True,"records":[item.__dict__ for item in preview.records]}
    output=Path(args.output_path); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for item in preview.records: print(f"{item.grain}: {item.stock_lmt} LMT, {item.stock_to_norm_percent}% of norm")
    print("No Observation, Evidence, Meta conclusion, Signal, recommendation, or trade was created."); return 0


if __name__=="__main__": raise SystemExit(main())
