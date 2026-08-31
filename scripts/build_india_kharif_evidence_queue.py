"""Generate the bounded evidence queue for the live Kharif case."""

import argparse,json
from dataclasses import asdict
from datetime import datetime,timezone
from pathlib import Path

from modules.external_intelligence.evidence_acquisition_queue import AcquisitionRouteState,EvidenceAcquisitionNeed,build_evidence_acquisition_queue


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True); args=parser.parse_args()
    now=datetime(2026,8,31,12,tzinfo=timezone.utc)
    needs=(
        EvidenceAcquisitionNeed("CURRENT-RESERVOIR-CROP-MAP","HYDROLOGY","CWC_OR_NWIC",AcquisitionRouteState.STALE_ONLY,True,False,25,30,3,datetime(2026,8,30,12,tzinfo=timezone.utc),24,True,False),
        EvidenceAcquisitionNeed("OBSERVED-SOIL-OR-CROP-CONDITION","CROP_CONDITION","NRSC",AcquisitionRouteState.ACCESS_REQUIRED,True,False,25,30,1,datetime(2026,8,30,12,tzinfo=timezone.utc),48,True,True),
        EvidenceAcquisitionNeed("CURRENT-OFFICIAL-FOOD-PRICES","OUTPUT_PRICE","CONSUMER_AFFAIRS_PRICES",AcquisitionRouteState.TRANSIENT_FAILURE,True,False,18,24,3,datetime(2026,8,31,6,tzinfo=timezone.utc),6,True,False),
        EvidenceAcquisitionNeed("MAIZE-MANDI-PRICE-ARRIVALS","PRICE_ARRIVAL","INDIA_OGD",AcquisitionRouteState.ACCESS_REQUIRED,True,False,22,28,0,None,24,True,True),
        EvidenceAcquisitionNeed("ISSUER-EXPOSURE-DISCLOSURE","COMPANY_EXPOSURE","NSE_OR_BSE",AcquisitionRouteState.READY,False,True,8,12,0,None,24,True,False),
        EvidenceAcquisitionNeed("DATED-COMPANY-CATALYST","CATALYST","NSE_OR_BSE",AcquisitionRouteState.READY,False,True,8,12,0,None,24,True,False),
    )
    queue=build_evidence_acquisition_queue(needs,now=now,sector_transmission_ready=False)
    payload={"schema_version":1,"case_id":"INDIA-KHARIF-2026","generated_at":now.isoformat(),"items":[asdict(item) for item in queue],"automatic_external_actions":False,"requires_human_review":True,"non_authority_statement":"Research queue only; it cannot bypass access controls or create an investment conclusion."}
    path=Path(args.output); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,indent=2,default=str)+"\n",encoding="utf-8"); print(f"Wrote {path}")


if __name__=="__main__": main()
