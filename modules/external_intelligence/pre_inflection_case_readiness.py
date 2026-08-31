"""Cross-layer readiness for a live pre-inflection research case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PreInflectionCaseInputs:
    case_id: str
    current_weather_ready: bool
    current_crop_progress_ready: bool
    soil_or_crop_condition_ready: bool
    irrigation_buffer_resolved: bool
    input_market_ready: bool
    output_price_ready: bool
    physical_arrivals_ready: bool
    contradiction_review_complete: bool
    independent_source_group_count: int
    company_bridge_ready: bool
    factual_catalyst_ready: bool
    expectation_reset_ready: bool
    stale_critical_input_ids: tuple[str,...]
    unresolved_gaps: tuple[str,...]


@dataclass(frozen=True)
class PreInflectionCaseReadiness:
    stage: str
    weather_crop_hint_ready: bool
    sector_transmission_ready: bool
    company_case_ready: bool
    expectation_reset_ready: bool
    reason_codes: tuple[str,...]
    next_evidence_priorities: tuple[str,...]
    permitted_claim: str


def assess_pre_inflection_case(inputs):
    if not isinstance(inputs,PreInflectionCaseInputs): raise ValueError("pre-inflection case inputs are required")
    if not inputs.case_id.strip(): raise ValueError("case_id must not be empty")
    reasons=[]; priorities=[]
    hint=inputs.current_weather_ready and inputs.current_crop_progress_ready
    if not inputs.current_weather_ready: reasons.append("CURRENT_WEATHER_MISSING"); priorities.append("current official weather anomaly")
    if not inputs.current_crop_progress_ready: reasons.append("CURRENT_CROP_PROGRESS_MISSING"); priorities.append("current crop progress")
    if not inputs.soil_or_crop_condition_ready: reasons.append("CROP_CONDITION_UNRESOLVED"); priorities.append("official soil-moisture or crop-condition observation")
    if not inputs.irrigation_buffer_resolved: reasons.append("IRRIGATION_BUFFER_UNRESOLVED"); priorities.append("current reservoir storage mapped to crop geography")
    if not inputs.input_market_ready: reasons.append("INPUT_MARKET_TRANSMISSION_MISSING"); priorities.append("comparable product and geography input demand")
    if not inputs.output_price_ready: reasons.append("OUTPUT_PRICE_TRANSMISSION_MISSING"); priorities.append("hash-bound current official food or mandi prices")
    if not inputs.physical_arrivals_ready: reasons.append("PHYSICAL_ARRIVALS_MISSING"); priorities.append("verified mandi arrival quantity and unit")
    if not inputs.contradiction_review_complete: reasons.append("CONTRADICTION_REVIEW_INCOMPLETE"); priorities.append("explicit contradiction review")
    if inputs.independent_source_group_count<2: reasons.append("INDEPENDENT_SUPPORT_INSUFFICIENT"); priorities.append("second independent primary source group")
    if inputs.stale_critical_input_ids: reasons.append("STALE_CRITICAL_INPUTS")
    causal=hint and inputs.soil_or_crop_condition_ready and inputs.irrigation_buffer_resolved and inputs.contradiction_review_complete and inputs.independent_source_group_count>=2 and not inputs.stale_critical_input_ids and (inputs.input_market_ready or inputs.output_price_ready or inputs.physical_arrivals_ready)
    company=causal and inputs.company_bridge_ready and inputs.factual_catalyst_ready
    expectation=company and inputs.expectation_reset_ready
    if expectation: stage="COMPANY_EXPECTATION_RESET_RESEARCH_READY"; claim="A governed sector transmission, company exposure, dated catalyst, and expectation comparator are assembled for human review."
    elif company: stage="COMPANY_PRE_INFLECTION_RESEARCH_READY"; claim="A governed sector transmission, company exposure, and dated catalyst are assembled; expectation reset is unproven."
    elif causal: stage="SECTOR_TRANSMISSION_RESEARCH_READY"; claim="The sector transmission is research-ready, but no company-specific case is authorized."
    elif hint: stage="WEATHER_CROP_HINT_ONLY"; claim="Current public data supports a weather-and-crop research hint only; causal sector and company impact remain unproven."
    else: stage="RESEARCH_HOLD"; claim="The case lacks the current weather-and-crop foundation required for pre-inflection research."
    if causal and not inputs.company_bridge_ready: reasons.append("COMPANY_BRIDGE_NOT_READY"); priorities.append("issuer disclosure with matched exposure and materiality")
    if causal and not inputs.factual_catalyst_ready: reasons.append("FACTUAL_CATALYST_NOT_READY"); priorities.append("dated quantified catalyst event")
    return PreInflectionCaseReadiness(stage,hint,causal,company,expectation,tuple(dict.fromkeys(reasons)),tuple(dict.fromkeys(priorities)),claim)


__all__=["PreInflectionCaseInputs","PreInflectionCaseReadiness","assess_pre_inflection_case"]
