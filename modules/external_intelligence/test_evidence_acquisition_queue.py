from datetime import datetime,timezone

from modules.external_intelligence.evidence_acquisition_queue import AcquisitionRouteState,EvidenceAcquisitionNeed,build_evidence_acquisition_queue


def main():
    now=datetime(2026,8,31,12,tzinfo=timezone.utc)
    needs=(
        EvidenceAcquisitionNeed("RESERVOIR","HYDROLOGY","CWC",AcquisitionRouteState.STALE_ONLY,True,False,20,25,0,None,24,True,False),
        EvidenceAcquisitionNeed("FOOD-PRICE","OUTPUT_PRICE","CONSUMER_AFFAIRS_PRICES",AcquisitionRouteState.TRANSIENT_FAILURE,True,False,15,20,2,datetime(2026,8,31,11,tzinfo=timezone.utc),6,True,False),
        EvidenceAcquisitionNeed("MANDI","PRICE_ARRIVAL","INDIA_OGD",AcquisitionRouteState.ACCESS_REQUIRED,True,False,18,25,0,None,24,True,True),
        EvidenceAcquisitionNeed("COMPANY","COMPANY_EXPOSURE","NSE",AcquisitionRouteState.READY,False,True,5,10,0,None,24,True,False),
    )
    queue=build_evidence_acquisition_queue(needs,now=now)
    assert queue[0].need_id=="RESERVOIR" and queue[0].action=="FIND_SANCTIONED_ALTERNATIVE"
    food=next(item for item in queue if item.need_id=="FOOD-PRICE"); assert not food.eligible_now and "RETRY_BACKOFF_ACTIVE" in food.reason_codes
    mandi=next(item for item in queue if item.need_id=="MANDI"); assert "USER_ACCESS_REQUIRED" in mandi.reason_codes
    company=next(item for item in queue if item.need_id=="COMPANY"); assert "DEFER_UNTIL_SECTOR_TRANSMISSION_READY" in company.reason_codes
    later=build_evidence_acquisition_queue(needs,now=now,sector_transmission_ready=True)
    assert next(item for item in later if item.need_id=="COMPANY").eligible_now
    print("EVIDENCE ACQUISITION QUEUE: ALL TESTS PASSED")


if __name__=="__main__": main()
