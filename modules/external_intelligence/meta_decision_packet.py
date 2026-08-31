"""Final read-only assembly gate around mandatory Meta and its downstream bridges."""

from dataclasses import dataclass

from modules.external_intelligence.catalyst_event_readiness import CatalystEventReadiness
from modules.external_intelligence.company_impact_bridge import CompanyImpactBridgeAssessment
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaGateDecision,MandatoryMetaGateResult


@dataclass(frozen=True)
class MetaDecisionPacketInput:
    packet_id: str
    meta_gate_result: MandatoryMetaGateResult
    governed_fact_ids: tuple[str,...]
    independent_source_group_ids: tuple[str,...]
    contradiction_search_completed: bool
    contradiction_fact_ids: tuple[str,...]
    no_contradiction_rationale: str | None
    stale_input_ids: tuple[str,...]
    unresolved_research_gaps: tuple[str,...]
    company_scope_requested: bool
    company_assessment: CompanyImpactBridgeAssessment | None
    catalyst_scope_requested: bool
    catalyst_assessment: CatalystEventReadiness | None


@dataclass(frozen=True)
class MetaDecisionPacketReadiness:
    status: str
    sector_monitoring_ready: bool
    company_pre_inflection_ready: bool
    expectation_reset_ready: bool
    reason_codes: tuple[str,...]
    permitted_claim: str
    non_authority_statement: str="Read-only Meta packet; it cannot create a Signal, Catalyst, Opportunity, recommendation, position, or trade."


def assess_meta_decision_packet(packet):
    if not isinstance(packet,MetaDecisionPacketInput): raise ValueError("Meta decision packet is required")
    reasons=[]
    if not packet.packet_id.strip(): reasons.append("PACKET_ID_MISSING")
    if not isinstance(packet.meta_gate_result,MandatoryMetaGateResult) or packet.meta_gate_result.decision!=MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION:
        reasons.append("MANDATORY_META_NOT_READY")
    if not packet.governed_fact_ids: reasons.append("GOVERNED_FACTS_MISSING")
    if len(set(packet.independent_source_group_ids))<2: reasons.append("INDEPENDENT_SOURCE_GROUPS_INSUFFICIENT")
    if not packet.contradiction_search_completed: reasons.append("CONTRADICTION_SEARCH_INCOMPLETE")
    elif not packet.contradiction_fact_ids and (not packet.no_contradiction_rationale or len(packet.no_contradiction_rationale.split())<6):
        reasons.append("NO_CONTRADICTION_RESULT_UNEXPLAINED")
    if packet.stale_input_ids: reasons.append("STALE_INPUTS_PRESENT")
    sector_ready=not reasons
    company_ready=False; expectation=False
    if packet.company_scope_requested:
        if packet.company_assessment is None: reasons.append("COMPANY_BRIDGE_MISSING")
        elif not packet.company_assessment.company_hypothesis_ready: reasons.append("COMPANY_BRIDGE_NOT_READY")
    if packet.catalyst_scope_requested:
        if packet.catalyst_assessment is None: reasons.append("CATALYST_GATE_MISSING")
        elif not packet.catalyst_assessment.factual_event_ready: reasons.append("CATALYST_EVENT_NOT_READY")
        else: expectation=packet.catalyst_assessment.expectation_reset_ready
    company_ready=sector_ready and packet.company_scope_requested and packet.catalyst_scope_requested and "COMPANY_BRIDGE_MISSING" not in reasons and "COMPANY_BRIDGE_NOT_READY" not in reasons and "CATALYST_GATE_MISSING" not in reasons and "CATALYST_EVENT_NOT_READY" not in reasons
    if not sector_ready: status="RESEARCH_HOLD"; claim="The assembled Meta case is incomplete and cannot advance."
    elif company_ready and expectation: status="COMPANY_EXPECTATION_RESET_RESEARCH_READY"; claim="The sector case, company exposure, dated event, and public expectation comparator are assembled for human pre-inflection review."
    elif company_ready: status="COMPANY_PRE_INFLECTION_RESEARCH_READY"; claim="The sector case, company exposure, and dated event are assembled; expectation reset remains unproven."
    else: status="SECTOR_MONITORING_READY"; claim="The governed sector case is ready for monitoring; it is not a company-specific pre-inflection case."
    return MetaDecisionPacketReadiness(status,sector_ready,company_ready,expectation,tuple(dict.fromkeys(reasons)),claim)


__all__=["MetaDecisionPacketInput","MetaDecisionPacketReadiness","assess_meta_decision_packet"]
