from dataclasses import replace
from datetime import datetime,timezone

from modules.external_intelligence.catalyst_event_readiness import CatalystEventReadiness
from modules.external_intelligence.company_impact_bridge import CompanyImpactBridgeAssessment
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaGateDecision,MandatoryMetaGateResult
from modules.external_intelligence.meta_decision_packet import MetaDecisionPacketInput,assess_meta_decision_packet


def main():
    meta=MandatoryMetaGateResult(MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION,(),"META-1",("TE-1","TE-2"))
    company=CompanyImpactBridgeAssessment("COMPANY_HYPOTHESIS_READY",True,("CROP","STATE","PRODUCT"),(),"Company exposure hypothesis ready.",())
    catalyst=CatalystEventReadiness("FACTUAL_EVENT_READY",True,False,("public expectation baseline",),"Factual event ready.",())
    packet=MetaDecisionPacketInput("PACKET-1",meta,("FACT-1","FACT-2"),("IMD","AGRI_MINISTRY"),True,("FACT-C1",),None,(),("current reservoir storage",),True,company,True,catalyst)
    ready=assess_meta_decision_packet(packet)
    assert ready.status=="COMPANY_PRE_INFLECTION_RESEARCH_READY" and ready.company_pre_inflection_ready and not ready.expectation_reset_ready
    expectation=assess_meta_decision_packet(replace(packet,catalyst_assessment=replace(catalyst,status="EXPECTATION_RESET_READY",expectation_reset_ready=True,missing_controls=())))
    assert expectation.status=="COMPANY_EXPECTATION_RESET_RESEARCH_READY"
    stale=assess_meta_decision_packet(replace(packet,stale_input_ids=("FOOD-STOCK-MAY",)))
    assert stale.status=="RESEARCH_HOLD" and "STALE_INPUTS_PRESENT" in stale.reason_codes
    sector=assess_meta_decision_packet(replace(packet,company_scope_requested=False,company_assessment=None,catalyst_scope_requested=False,catalyst_assessment=None))
    assert sector.status=="SECTOR_MONITORING_READY" and sector.sector_monitoring_ready and not sector.company_pre_inflection_ready
    unexplained=assess_meta_decision_packet(replace(packet,contradiction_fact_ids=(),no_contradiction_rationale="none"))
    assert "NO_CONTRADICTION_RESULT_UNEXPLAINED" in unexplained.reason_codes
    print("META DECISION PACKET: ALL TESTS PASSED")


if __name__=="__main__": main()
