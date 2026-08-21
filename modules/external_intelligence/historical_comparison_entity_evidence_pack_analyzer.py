"""Explicit scoring of one fully reconciled entity EvidenceItem pack."""

from __future__ import annotations

from modules.external_intelligence.historical_comparison_entity_evidence_pack_preview import (
    HistoricalComparisonEntityEvidencePackPreview,
)
from modules.opportunity.evidence_engine import (
    EvidenceItem,
    OpportunityEvidenceEngine,
    OpportunityEvidencePack,
)


class HistoricalComparisonEntityEvidencePackAnalyzer:
    """Invoke only the existing Opportunity Evidence analysis boundary."""

    def __init__(self, engine: OpportunityEvidenceEngine | None = None) -> None:
        self.engine = engine if engine is not None else OpportunityEvidenceEngine()

    def analyze(
        self, pack: HistoricalComparisonEntityEvidencePackPreview
    ) -> OpportunityEvidencePack:
        if not isinstance(pack, HistoricalComparisonEntityEvidencePackPreview):
            raise ValueError("pack must be an entity Evidence pack preview")
        if pack.missing_assessment_candidate_ids:
            raise ValueError("entity pack has missing human assessments")
        if pack.missing_receipt_candidate_ids:
            raise ValueError("entity pack has missing materialization receipts")
        if not pack.materialized_receipts:
            raise ValueError("entity pack has no materialized EvidenceItems")

        supporting = []
        contradictory = []
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

        return self.engine.analyze(
            company=pack.entity,
            supporting_evidence=supporting,
            contradictory_evidence=contradictory,
            assumptions=[],
            kill_switches=[],
            monitoring_signals=[],
        )


__all__ = ["HistoricalComparisonEntityEvidencePackAnalyzer"]
