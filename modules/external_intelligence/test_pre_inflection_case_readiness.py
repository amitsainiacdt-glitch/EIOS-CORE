from dataclasses import replace

from modules.external_intelligence.pre_inflection_case_readiness import PreInflectionCaseInputs,assess_pre_inflection_case


def main():
    live=PreInflectionCaseInputs("INDIA-KHARIF-2026",True,True,False,False,True,False,False,True,3,False,False,False,(),("soil moisture unavailable","current reservoirs unresolved","mandi arrivals unavailable"))
    held=assess_pre_inflection_case(live)
    assert held.stage=="WEATHER_CROP_HINT_ONLY" and held.weather_crop_hint_ready and not held.sector_transmission_ready
    assert "CROP_CONDITION_UNRESOLVED" in held.reason_codes and "IRRIGATION_BUFFER_UNRESOLVED" in held.reason_codes
    sector=assess_pre_inflection_case(replace(live,soil_or_crop_condition_ready=True,irrigation_buffer_resolved=True,output_price_ready=True))
    assert sector.stage=="SECTOR_TRANSMISSION_RESEARCH_READY" and sector.sector_transmission_ready
    company_inputs=replace(live,soil_or_crop_condition_ready=True,irrigation_buffer_resolved=True,output_price_ready=True,company_bridge_ready=True,factual_catalyst_ready=True)
    company=assess_pre_inflection_case(company_inputs)
    assert company.stage=="COMPANY_PRE_INFLECTION_RESEARCH_READY"
    stale=assess_pre_inflection_case(replace(company_inputs,stale_critical_input_ids=("RESERVOIR-OLD",)))
    assert stale.stage=="WEATHER_CROP_HINT_ONLY" and "STALE_CRITICAL_INPUTS" in stale.reason_codes
    print("PRE-INFLECTION CASE READINESS: ALL TESTS PASSED")


if __name__=="__main__": main()
