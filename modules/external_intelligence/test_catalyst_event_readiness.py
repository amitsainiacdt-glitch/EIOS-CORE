from dataclasses import replace
from datetime import datetime,timezone

from modules.external_intelligence.catalyst_event_readiness import CatalystEventStatus,PublicCatalystEventCandidate,assess_catalyst_event
from modules.opportunity.catalyst.catalyst_taxonomy import CatalystFamily


def main():
    now=datetime(2026,8,31,tzinfo=timezone.utc)
    candidate=PublicCatalystEventCandidate("CAT-1","Example Limited",CatalystFamily.ORDER_CONTRACT,CatalystEventStatus.ANNOUNCED,datetime(2026,8,30,tzinfo=timezone.utc),"NSE","FILING-1","https://nse.example/filing.pdf","b"*64,"The company received a firm domestic order with scheduled delivery over twelve months.",("FACT-1",),125.0,"INR_CRORE","Order execution can add to reported revenue as milestones are completed",None,None,"Customer cancellation or delayed milestone certification would invalidate expected timing")
    factual=assess_catalyst_event(candidate,assessed_at=now)
    assert factual.status=="FACTUAL_EVENT_READY" and factual.factual_event_ready and not factual.expectation_reset_ready
    expected=replace(candidate,expectation_baseline_source_id="PUBLIC-CONSENSUS-1",expectation_gap_statement="The disclosed order exceeds the documented public order-inflow expectation")
    ready=assess_catalyst_event(expected,assessed_at=now)
    assert ready.status=="EXPECTATION_RESET_READY" and ready.expectation_reset_ready
    trend=replace(expected,event_status=CatalystEventStatus.CONTINUING_TREND)
    held=assess_catalyst_event(trend,assessed_at=now)
    assert held.status=="RESEARCH_HOLD" and "discrete announced, scheduled, or completed event" in held.missing_controls
    unquantified=assess_catalyst_event(replace(candidate,quantified_event_value=None),assessed_at=now)
    assert not unquantified.factual_event_ready and "quantified event magnitude and unit" in unquantified.missing_controls
    print("CATALYST EVENT READINESS: ALL TESTS PASSED")


if __name__=="__main__": main()
