"""Deterministic persistence/independence preview; no causal conclusion."""

from __future__ import annotations

import json
from hashlib import sha256

from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry
from modules.external_intelligence.temporal_leading_indicator_preview import IndicatorEvidenceRelationship, TemporalIndicatorEvidenceLink, TemporalIndicatorStructuralState, TemporalLeadingIndicatorPreview


class TemporalLeadingIndicatorService:
    def __init__(self, registry):
        if not isinstance(registry, SectorCausalIndicatorRegistry): raise ValueError("registry must be SectorCausalIndicatorRegistry")
        self.registry = registry

    def preview(self, *, entity, sector_id, indicator_id, temporal_evidence, links):
        entity, sector_id = self._text(entity, "entity"), self._text(sector_id, "sector_id")
        definition = self.registry.get(indicator_id)
        if sector_id.casefold() not in {item.casefold() for item in definition.sector_ids}: raise ValueError("indicator does not apply to sector")
        records = tuple(temporal_evidence); links = tuple(links)
        if not records or not all(isinstance(item, PublicTemporalEvidenceRecord) for item in records): raise ValueError("temporal_evidence must not be empty")
        if not links or not all(isinstance(item, TemporalIndicatorEvidenceLink) for item in links): raise ValueError("links must not be empty")
        record_map = {item.temporal_evidence_id: item for item in records}
        if len(record_map) != len(records): raise ValueError("duplicate Temporal Evidence IDs")
        link_map = {item.temporal_evidence_id: item for item in links}
        if len(link_map) != len(links) or set(link_map) != set(record_map): raise ValueError("every Temporal Evidence record requires exactly one link")
        if any(item.indicator_id != definition.indicator_id for item in links): raise ValueError("evidence link indicator mismatch")
        if any(not isinstance(item.relationship, IndicatorEvidenceRelationship) for item in links): raise ValueError("evidence relationship is invalid")
        if any(item.entity.casefold() != entity.casefold() for item in records): raise ValueError("Temporal Evidence entity mismatch")
        if any(item.event_type not in definition.applicable_event_types for item in records): raise ValueError("Temporal Evidence event type is not applicable to indicator")
        for link in links:
            self._text(link.independence_group_id, "independence_group_id"); self._text(link.rationale, "rationale")

        ordered = tuple(sorted(records, key=lambda item: (item.event_at, item.known_at, item.temporal_evidence_id)))
        supporting = tuple(item for item in links if item.relationship == IndicatorEvidenceRelationship.SUPPORTS)
        contradicting = tuple(item for item in links if item.relationship == IndicatorEvidenceRelationship.CONTRADICTS)
        context = tuple(item for item in links if item.relationship == IndicatorEvidenceRelationship.CONTEXT_ONLY)
        support_groups = tuple(sorted({item.independence_group_id for item in supporting}))
        support_records = tuple(record_map[item.temporal_evidence_id] for item in supporting)
        span = (max((item.event_at for item in support_records), default=ordered[0].event_at) - min((item.event_at for item in support_records), default=ordered[0].event_at)).days
        span = max(0, span)
        reasons, warnings = [], []
        if len(supporting) < definition.minimum_persistent_observations: reasons.append("PERSISTENT_OBSERVATION_COUNT_INSUFFICIENT")
        if len(support_groups) < definition.minimum_independence_groups: reasons.append("INDEPENDENCE_BREADTH_INSUFFICIENT")
        if span < definition.expected_persistence_days: reasons.append("PERSISTENCE_DURATION_INSUFFICIENT")
        if contradicting: reasons.append("CONTRADICTING_EVIDENCE_PRESENT")
        if any(item.time_basis == "KNOWN_AT_FALLBACK" for item in ordered): warnings.append("Some evidence uses known-at fallback time.")
        if context: warnings.append("Context-only evidence is excluded from support and contradiction counts.")
        state = TemporalIndicatorStructuralState.STRUCTURALLY_READY_FOR_META
        if contradicting:
            state = TemporalIndicatorStructuralState.CONTRADICTED
        elif not supporting:
            state = TemporalIndicatorStructuralState.INSUFFICIENT
        elif reasons:
            state = TemporalIndicatorStructuralState.FORMING
        fingerprint_payload = {
            "indicator_id": definition.indicator_id, "indicator_version": definition.version,
            "entity": entity, "sector_id": sector_id,
            "records": [(item.temporal_evidence_id, item.observation_fingerprint) for item in ordered],
            "links": sorted((item.temporal_evidence_id, item.independence_group_id, item.relationship.value, item.rationale) for item in links),
            "requirements": (definition.minimum_independence_groups, definition.minimum_persistent_observations, definition.expected_persistence_days),
        }
        preview_fingerprint = sha256(json.dumps(fingerprint_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        return TemporalLeadingIndicatorPreview(
            preview_fingerprint, definition.indicator_id, definition.version, entity, sector_id,
            tuple(sorted({item.event_type for item in ordered})), tuple(item.temporal_evidence_id for item in ordered),
            tuple(item.observation_fingerprint for item in ordered), len(supporting), len(contradicting), len(context),
            support_groups, len(support_groups), definition.minimum_independence_groups, len(supporting),
            definition.minimum_persistent_observations, span, definition.expected_persistence_days,
            ordered[0].event_at, ordered[-1].event_at,
            (definition.lead_time_quarters_min, definition.lead_time_quarters_max), state,
            tuple(reasons), tuple(warnings),
        )

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["TemporalLeadingIndicatorService"]
