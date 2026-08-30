"""Offline tests proving Meta-Analysis cannot be skipped."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone

from modules.external_intelligence.mandatory_meta_analysis import MandatoryMetaAnalysisAssessment, MetaAnalysisConclusion, MetaContradictionBurden, MetaKillTestResult, MetaKillTestStatus
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaAnalysisGate
from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry
from modules.external_intelligence.temporal_leading_indicator_preview import IndicatorEvidenceRelationship, TemporalIndicatorEvidenceLink
from modules.external_intelligence.temporal_leading_indicator_service import TemporalLeadingIndicatorService


def main():
    now = datetime(2026, 8, 29, 19, tzinfo=timezone.utc)
    records = tuple(
        PublicTemporalEvidenceRecord(1, f"TE-{i}", f"{i:064x}", "Alpha Limited", "ORDER_CONTRACT", "ASSERTED", now + timedelta(days=(i-1)*180), now + timedelta(days=(i-1)*180), "PUBLISHED_AT", "https://www.nseindia.com/a", f"{i+10:064x}", f"C-{i}", f"P-{i}", f"R-{i}", f"Order {i}", f"Exact passage {i}")
        for i in (1, 2)
    )
    registry = SectorCausalIndicatorRegistry.initial_library()
    gate = MandatoryMetaAnalysisGate(registry)
    preview = TemporalLeadingIndicatorService(registry).preview(
        entity="Alpha Limited", sector_id="INDUSTRIALS", indicator_id="INDUSTRIAL_ORDER_CONVERSION", temporal_evidence=records,
        links=(
            TemporalIndicatorEvidenceLink("TE-1", "INDUSTRIAL_ORDER_CONVERSION", "NSE", IndicatorEvidenceRelationship.SUPPORTS, "First primary source."),
            TemporalIndicatorEvidenceLink("TE-2", "INDUSTRIAL_ORDER_CONVERSION", "TENDER_AUTHORITY", IndicatorEvidenceRelationship.SUPPORTS, "Independent authority."),
        ),
    )
    missing = gate.evaluate(temporal_evidence=records, assessment=None)
    assert missing.decision.value == "BLOCKED" and missing.meta_required
    assessment = MandatoryMetaAnalysisAssessment(
        1, "META-1", ("Alpha Limited",), ("Industrials",), ("TE-1", "TE-2"),
        (f"{1:064x}", f"{2:064x}"), (preview.preview_fingerprint,), ("INDUSTRIAL_ORDER_CONVERSION",), ("Tender awards may be converting into company orders.",),
        ("NSE_COMPANY_FILING", "GOVERNMENT_TENDER"), (), ("Execution confirmation not yet published.",),
        (), (), ("Tender authority to company order transmission observed.",), ("Execution confirmation remains a research gap.",),
        tuple(MetaKillTestResult("INDUSTRIAL_ORDER_CONVERSION", test, MetaKillTestStatus.NOT_TRIGGERED, ("TE-1", "TE-2"), "No public evidence currently triggers this kill test.") for test in registry.get("INDUSTRIAL_ORDER_CONVERSION").kill_tests),
        MetaAnalysisConclusion.EMERGING, MetaContradictionBurden.LOW,
        True, True, True, True, True, True,
        "Evidence is early and order execution remains uncertain.",
        "Read-only research assessment; not an investment decision.", now, "Meta Analysis Engine",
    )
    ready = gate.evaluate(temporal_evidence=records, assessment=assessment, indicator_previews=(preview,))
    assert ready.decision.value == "READY_FOR_PRE_INFLECTION" and ready.reason_codes == ()
    incomplete = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, contradictions_checked=False), indicator_previews=(preview,))
    assert incomplete.decision.value == "BLOCKED" and "CONTRADICTION_CHECK_MISSING" in incomplete.reason_codes
    one_source = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, independence_group_ids=("NSE_COMPANY_FILING",)), indicator_previews=(preview,))
    assert one_source.decision.value == "HOLD_FOR_RESEARCH" and "INDEPENDENT_SUPPORT_INSUFFICIENT" in one_source.reason_codes
    contradicted = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, conclusion=MetaAnalysisConclusion.CONTRADICTED, contradiction_burden=MetaContradictionBurden.HIGH), indicator_previews=(preview,))
    assert contradicted.decision.value == "HOLD_FOR_RESEARCH" and "HIGH_CONTRADICTION_BURDEN" in contradicted.reason_codes
    wrong_inputs = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, input_temporal_evidence_ids=("TE-1",)), indicator_previews=(preview,))
    assert wrong_inputs.decision.value == "BLOCKED" and "TEMPORAL_EVIDENCE_BINDING_MISMATCH" in wrong_inputs.reason_codes
    non_public = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, public_information_only=False), indicator_previews=(preview,))
    assert non_public.decision.value == "BLOCKED" and "NON_PUBLIC_INFORMATION_PROHIBITED" in non_public.reason_codes
    unknown_indicator = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, causal_indicator_ids=("UNKNOWN",)), indicator_previews=(preview,))
    assert unknown_indicator.decision.value == "BLOCKED" and "CAUSAL_INDICATOR_UNKNOWN" in unknown_indicator.reason_codes
    wrong_sector = gate.evaluate(temporal_evidence=records, assessment=replace(assessment, sector_scope=("BANKING",)), indicator_previews=(preview,))
    assert wrong_sector.decision.value == "BLOCKED" and "CAUSAL_INDICATOR_SCOPE_MISMATCH" in wrong_sector.reason_codes
    rainfall_only_fertilizer = gate.evaluate(
        temporal_evidence=records,
        assessment=replace(assessment, sector_scope=("FERTILIZERS",), causal_indicator_ids=("RAINFALL_FERTILIZER_RESPONSE_CURVE",)),
        indicator_previews=(preview,),
    )
    assert rainfall_only_fertilizer.decision.value == "BLOCKED"
    assert "CAUSAL_INDICATOR_DEPENDENCY_MISSING" in rainfall_only_fertilizer.reason_codes
    print("MANDATORY META-ANALYSIS GATE: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
