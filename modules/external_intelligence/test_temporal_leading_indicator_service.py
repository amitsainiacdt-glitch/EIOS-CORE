"""Offline tests for Meta-facing temporal leading-indicator previews."""

from datetime import datetime, timedelta, timezone

from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry
from modules.external_intelligence.temporal_leading_indicator_preview import IndicatorEvidenceRelationship, TemporalIndicatorEvidenceLink
from modules.external_intelligence.temporal_leading_indicator_service import TemporalLeadingIndicatorService


def main():
    now = datetime(2026, 8, 29, 20, tzinfo=timezone.utc)

    def record(index, days, event_type="ORDER_CONTRACT", posture="ASSERTED"):
        event_at = now + timedelta(days=days)
        return PublicTemporalEvidenceRecord(
            1, f"TE-{index}", f"{index:064x}", "Alpha Limited", event_type, posture,
            event_at, event_at + timedelta(hours=1), "PUBLISHED_AT", "https://public.example/a",
            f"{index+10:064x}", f"C-{index}", f"P-{index}", f"R-{index}", f"Fact {index}", f"Exact passage {index}",
        )

    first, second = record(1, 0, "TENDER"), record(2, 180, "ORDER_CONTRACT")
    links = (
        TemporalIndicatorEvidenceLink("TE-1", "INDUSTRIAL_ORDER_CONVERSION", "GOVERNMENT_TENDER", IndicatorEvidenceRelationship.SUPPORTS, "Official tender authority."),
        TemporalIndicatorEvidenceLink("TE-2", "INDUSTRIAL_ORDER_CONVERSION", "NSE_COMPANY_FILING", IndicatorEvidenceRelationship.SUPPORTS, "Company exchange filing."),
    )
    service = TemporalLeadingIndicatorService(SectorCausalIndicatorRegistry.initial_library())
    ready = service.preview(entity="Alpha Limited", sector_id="INDUSTRIALS", indicator_id="INDUSTRIAL_ORDER_CONVERSION", temporal_evidence=(second, first), links=links)
    assert ready.structural_state.value == "STRUCTURALLY_READY_FOR_META"
    assert ready.independence_group_count == 2 and ready.observed_span_days == 180
    assert ready.meta_analysis_required and ready.reason_codes == ()

    short = service.preview(entity="Alpha Limited", sector_id="INDUSTRIALS", indicator_id="INDUSTRIAL_ORDER_CONVERSION", temporal_evidence=(first,), links=(links[0],))
    assert short.structural_state.value == "FORMING"
    assert "INDEPENDENCE_BREADTH_INSUFFICIENT" in short.reason_codes
    assert "PERSISTENCE_DURATION_INSUFFICIENT" in short.reason_codes

    contradiction = record(3, 200, "EXECUTION_UPDATE", "NEGATED")
    contradicted = service.preview(
        entity="Alpha Limited", sector_id="INDUSTRIALS", indicator_id="INDUSTRIAL_ORDER_CONVERSION",
        temporal_evidence=(first, second, contradiction),
        links=links + (TemporalIndicatorEvidenceLink("TE-3", "INDUSTRIAL_ORDER_CONVERSION", "CUSTOMER_DISCLOSURE", IndicatorEvidenceRelationship.CONTRADICTS, "Customer reports cancellation."),),
    )
    assert contradicted.structural_state.value == "CONTRADICTED"
    assert contradicted.contradicting_count == 1

    try:
        service.preview(entity="Alpha Limited", sector_id="BANKING", indicator_id="INDUSTRIAL_ORDER_CONVERSION", temporal_evidence=(first,), links=(links[0],))
    except ValueError as exc:
        assert "sector" in str(exc)
    else:
        raise AssertionError("wrong-sector interpretation accepted")

    try:
        service.preview(entity="Alpha Limited", sector_id="INDUSTRIALS", indicator_id="INDUSTRIAL_ORDER_CONVERSION", temporal_evidence=(first, second), links=(links[0],))
    except ValueError as exc:
        assert "exactly one link" in str(exc)
    else:
        raise AssertionError("unlinked evidence accepted")

    print("TEMPORAL LEADING INDICATOR SERVICE: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
