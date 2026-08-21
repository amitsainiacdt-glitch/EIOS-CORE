"""Explicit analysis of a verified Evidence pack with human governance."""

from __future__ import annotations

from modules.external_intelligence.historical_comparison_entity_evidence_pack_preview import HistoricalComparisonEntityEvidencePackPreview
from modules.external_intelligence.historical_comparison_evidence_governance import HistoricalComparisonEvidenceGovernance
from modules.opportunity.evidence_engine import EvidenceItem, KillSwitch, OpportunityEvidenceEngine


class HistoricalComparisonGovernedEvidencePackAnalyzer:
    def __init__(self, engine=None):
        self.engine = engine if engine is not None else OpportunityEvidenceEngine()

    def analyze(self, pack, governance):
        if not isinstance(pack, HistoricalComparisonEntityEvidencePackPreview):
            raise ValueError("pack must be an entity Evidence pack preview")
        if not isinstance(governance, HistoricalComparisonEvidenceGovernance):
            raise ValueError("governance must be a human governance record")
        if pack.entity != governance.entity:
            raise ValueError("governance entity does not match Evidence pack")
        if pack.missing_assessment_candidate_ids or pack.missing_receipt_candidate_ids:
            raise ValueError("entity pack has unresolved workflow gaps")
        if not pack.materialized_receipts:
            raise ValueError("entity pack has no materialized EvidenceItems")
        supporting, contradictory = [], []
        for receipt in pack.materialized_receipts:
            item = EvidenceItem(
                evidence_id=receipt.evidence_id,
                statement=receipt.statement,
                source=receipt.source,
                category=receipt.category,
                direction=receipt.direction,
                strength=receipt.strength,
                confidence=receipt.confidence,
                independent_confirmation=receipt.independent_confirmation,
                is_primary_source=receipt.is_primary_source,
                is_time_sensitive=receipt.is_time_sensitive,
                notes=receipt.notes,
            )
            if item.direction == "Supporting":
                supporting.append(item)
            elif item.direction == "Contradictory":
                contradictory.append(item)
            else:
                raise ValueError("receipt has unsupported Evidence direction")
        kill_switches = [
            KillSwitch(
                name=item.name,
                condition=item.condition,
                severity=item.severity,
                measurable=item.measurable,
                threshold=item.threshold,
                monitoring_frequency=item.monitoring_frequency,
                rationale=item.rationale,
                triggered=item.triggered,
            )
            for item in governance.kill_switches
        ]
        return self.engine.analyze(
            company=pack.entity,
            supporting_evidence=supporting,
            contradictory_evidence=contradictory,
            assumptions=list(governance.assumptions),
            kill_switches=kill_switches,
            monitoring_signals=list(governance.monitoring_signals),
        )


__all__ = ["HistoricalComparisonGovernedEvidencePackAnalyzer"]
