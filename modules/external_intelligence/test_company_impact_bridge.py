from dataclasses import replace
from datetime import datetime,timezone

from modules.external_intelligence.company_impact_bridge import CompanyExposureDisclosure,GovernedSectorFact,assess_company_impact_bridge


def main():
    now=datetime(2026,8,31,tzinfo=timezone.utc)
    fact=GovernedSectorFact("FACT-1","MAIZE_AREA_LAG",("MAIZE",),("MH",),("MAIZE_INPUT",),"NEGATIVE",now,("AGRI_MINISTRY",))
    broad=CompanyExposureDisclosure("D-1","Example Limited","NSE","AR-2026","https://nse.example/ar.pdf","a"*64,"The company distributes agricultural inputs across Maharashtra and other important Indian markets.",datetime(2026,6,30,tzinfo=timezone.utc),(),("MH",),(),None,None)
    held=assess_company_impact_bridge(fact,broad,assessed_at=now)
    assert held.status=="EXPOSURE_MAPPED_RESEARCH_HOLD" and not held.company_hypothesis_ready and "matching product exposure" in held.missing_controls
    exact=replace(broad,product_ids=("MAIZE_INPUT",),crop_ids=("MAIZE",),disclosed_revenue_exposure_pct=18.4,transmission_mechanism="Lower planted maize area can reduce addressable seasonal product volumes")
    ready=assess_company_impact_bridge(fact,exact,assessed_at=now)
    assert ready.status=="COMPANY_HYPOTHESIS_READY" and ready.company_hypothesis_ready and ready.matched_dimensions==("CROP","STATE","PRODUCT")
    unverifiable=replace(exact,authority_id="COMPANY_WEBSITE",document_hash="not-a-hash")
    rejected=assess_company_impact_bridge(fact,unverifiable,assessed_at=now)
    assert not rejected.company_hypothesis_ready and "exchange or securities-regulator authority" in rejected.missing_controls
    no_materiality=assess_company_impact_bridge(fact,replace(exact,disclosed_revenue_exposure_pct=None),assessed_at=now)
    assert "quantified revenue or volume materiality" in no_materiality.missing_controls
    print("COMPANY IMPACT BRIDGE: ALL TESTS PASSED")


if __name__=="__main__": main()
