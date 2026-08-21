"""Read-only receipt reconciliation and entity pack preview assembly."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from modules.external_intelligence.historical_comparison_accepted_observation_preview import (
    HistoricalComparisonAcceptedObservationPreview,
)
from modules.external_intelligence.historical_comparison_entity_evidence_pack_preview import (
    HistoricalComparisonEntityEvidencePackPreview,
    HistoricalComparisonEvidencePackPreviewResult,
)
from modules.external_intelligence.historical_comparison_evidence_assessment import (
    HistoricalComparisonEvidenceAssessment,
)
from modules.external_intelligence.historical_comparison_evidence_conversion_preview_builder import (
    HistoricalComparisonEvidenceConversionPreviewBuilder,
)
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import (
    HistoricalComparisonEvidenceConversionReceipt,
)


class HistoricalComparisonEvidenceReceiptReconciler:
    """Verify receipts exactly without recreating EvidenceItems."""

    def reconcile(
        self,
        previews: Iterable[HistoricalComparisonAcceptedObservationPreview],
        assessments: Iterable[HistoricalComparisonEvidenceAssessment],
        receipts: Iterable[HistoricalComparisonEvidenceConversionReceipt],
    ) -> HistoricalComparisonEvidencePackPreviewResult:
        if previews is None or assessments is None or receipts is None:
            raise ValueError("previews, assessments, and receipts must not be None")
        preview_list = tuple(previews)
        assessment_list = tuple(assessments)
        receipt_list = tuple(receipts)
        eligibility = HistoricalComparisonEvidenceConversionPreviewBuilder().build(
            preview_list, assessment_list
        )
        preview_by_id = {item.candidate_id: item for item in preview_list}
        projection_by_id = {
            item.candidate_id: item for item in eligibility.eligible_previews
        }
        assessment_by_id = {
            item.candidate_id: item for item in assessment_list
        }

        receipt_by_id = {}
        evidence_ids = set()
        for receipt in receipt_list:
            if not isinstance(
                receipt, HistoricalComparisonEvidenceConversionReceipt
            ):
                raise ValueError("receipts contain an invalid item")
            if receipt.candidate_id not in preview_by_id:
                raise ValueError(
                    "receipt references unknown accepted candidate "
                    f"{receipt.candidate_id}"
                )
            if receipt.candidate_id not in projection_by_id:
                raise ValueError(
                    "receipt candidate lacks a reconciled human assessment"
                )
            if receipt.candidate_id in receipt_by_id:
                raise ValueError("accepted candidate has multiple receipts")
            if receipt.evidence_id in evidence_ids:
                raise ValueError("duplicate materialized Evidence identity")
            self._validate_receipt(
                receipt,
                projection_by_id[receipt.candidate_id],
                assessment_by_id[receipt.candidate_id],
            )
            receipt_by_id[receipt.candidate_id] = receipt
            evidence_ids.add(receipt.evidence_id)

        groups = defaultdict(
            lambda: {
                "receipts": [],
                "supporting": [],
                "contradictory": [],
                "missing_assessment": [],
                "missing_receipt": [],
            }
        )
        for preview in preview_list:
            group = groups[preview.entity]
            receipt = receipt_by_id.get(preview.candidate_id)
            if preview.candidate_id not in assessment_by_id:
                group["missing_assessment"].append(preview.candidate_id)
            elif receipt is None:
                group["missing_receipt"].append(preview.candidate_id)
            else:
                group["receipts"].append(receipt)
                if receipt.direction == "Supporting":
                    group["supporting"].append(receipt.evidence_id)
                else:
                    group["contradictory"].append(receipt.evidence_id)

        packs = []
        for entity in sorted(groups, key=str.casefold):
            group = groups[entity]
            packs.append(
                HistoricalComparisonEntityEvidencePackPreview(
                    entity=entity,
                    materialized_receipts=tuple(
                        sorted(
                            group["receipts"],
                            key=lambda item: item.candidate_id,
                        )
                    ),
                    supporting_evidence_ids=tuple(sorted(group["supporting"])),
                    contradictory_evidence_ids=tuple(
                        sorted(group["contradictory"])
                    ),
                    missing_assessment_candidate_ids=tuple(
                        sorted(group["missing_assessment"])
                    ),
                    missing_receipt_candidate_ids=tuple(
                        sorted(group["missing_receipt"])
                    ),
                )
            )
        return HistoricalComparisonEvidencePackPreviewResult(
            accepted_count=len(preview_list),
            assessment_count=len(assessment_list),
            receipt_count=len(receipt_list),
            entity_packs=tuple(packs),
        )

    @staticmethod
    def _validate_receipt(receipt, projection, assessment) -> None:
        expected = {
            "observation_fingerprint": projection.observation_fingerprint,
            "evidence_id": projection.proposed_evidence_id,
            "statement": projection.statement,
            "source": projection.source,
            "category": projection.category,
            "direction": projection.direction,
            "strength": projection.strength,
            "confidence": projection.confidence,
            "independent_confirmation": projection.independent_confirmation,
            "is_primary_source": projection.is_primary_source,
            "is_time_sensitive": projection.is_time_sensitive,
            "notes": projection.notes,
            "reviewer": projection.reviewer,
            "reviewed_at": projection.reviewed_at,
            "assessor": projection.assessor,
            "assessed_at": projection.assessed_at,
        }
        for name, value in expected.items():
            if getattr(receipt, name) != value:
                raise ValueError(
                    "materialized Evidence receipt mismatch: " + name
                )
        try:
            if receipt.converted_at < assessment.assessed_at:
                raise ValueError("receipt conversion precedes assessment")
        except TypeError as exc:
            raise ValueError(
                "receipt timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc


__all__ = ["HistoricalComparisonEvidenceReceiptReconciler"]
