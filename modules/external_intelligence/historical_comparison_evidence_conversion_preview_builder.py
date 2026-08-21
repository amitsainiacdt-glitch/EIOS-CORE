"""Build read-only Evidence conversion eligibility projections."""

from __future__ import annotations

from typing import Iterable

from modules.external_intelligence.historical_comparison_accepted_observation_preview import (
    HistoricalComparisonAcceptedObservationPreview,
)
from modules.external_intelligence.historical_comparison_evidence_assessment import (
    HistoricalComparisonEvidenceAssessment,
)
from modules.external_intelligence.historical_comparison_evidence_conversion_preview import (
    HistoricalComparisonEvidenceConversionEligibility,
    HistoricalComparisonEvidenceConversionPreview,
)


class HistoricalComparisonEvidenceConversionPreviewBuilder:
    """Reconcile accepted observations and assessments without Evidence."""

    def build(
        self,
        previews: Iterable[HistoricalComparisonAcceptedObservationPreview],
        assessments: Iterable[HistoricalComparisonEvidenceAssessment],
    ) -> HistoricalComparisonEvidenceConversionEligibility:
        if previews is None or assessments is None:
            raise ValueError("previews and assessments must not be None")
        preview_list = tuple(previews)
        assessment_list = tuple(assessments)

        preview_by_id = {}
        fingerprints = set()
        for preview in preview_list:
            if not isinstance(
                preview, HistoricalComparisonAcceptedObservationPreview
            ):
                raise ValueError("previews contain an invalid item")
            if preview.candidate_id in preview_by_id:
                raise ValueError("accepted candidate identities must be unique")
            if preview.content_fingerprint in fingerprints:
                raise ValueError(
                    "accepted candidates resolve to a duplicate observation "
                    "fingerprint"
                )
            preview_by_id[preview.candidate_id] = preview
            fingerprints.add(preview.content_fingerprint)

        assessment_by_id = {}
        for assessment in assessment_list:
            if not isinstance(assessment, HistoricalComparisonEvidenceAssessment):
                raise ValueError("assessments contain an invalid item")
            if assessment.candidate_id not in preview_by_id:
                raise ValueError(
                    "assessment references unknown accepted candidate "
                    f"{assessment.candidate_id}"
                )
            if assessment.candidate_id in assessment_by_id:
                raise ValueError("accepted candidate has multiple assessments")
            assessment_by_id[assessment.candidate_id] = assessment

        eligible = []
        missing = []
        for candidate_id in sorted(preview_by_id):
            preview = preview_by_id[candidate_id]
            assessment = assessment_by_id.get(candidate_id)
            if assessment is None:
                missing.append(candidate_id)
                continue
            if assessment.observation_fingerprint != preview.content_fingerprint:
                raise ValueError(
                    "assessment observation fingerprint does not match "
                    f"accepted candidate {candidate_id}"
                )
            try:
                if assessment.assessed_at < preview.reviewed_at:
                    raise ValueError("assessment timestamp precedes accepted review")
            except TypeError as exc:
                raise ValueError(
                    "assessment and review timestamps must use a consistent "
                    "timezone-awareness policy"
                ) from exc
            eligible.append(self._project(preview, assessment))

        return HistoricalComparisonEvidenceConversionEligibility(
            accepted_count=len(preview_list),
            eligible_previews=tuple(eligible),
            missing_assessment_candidate_ids=tuple(missing),
        )

    @staticmethod
    def _project(preview, assessment):
        return HistoricalComparisonEvidenceConversionPreview(
            candidate_id=preview.candidate_id,
            observation_fingerprint=preview.content_fingerprint,
            proposed_evidence_id=f"HC-{preview.candidate_id}",
            statement=preview.description,
            source=preview.source,
            category=assessment.category,
            direction=assessment.direction,
            strength=assessment.strength,
            confidence=assessment.confidence,
            independent_confirmation=assessment.independent_confirmation,
            is_primary_source=assessment.is_primary_source,
            is_time_sensitive=assessment.is_time_sensitive,
            notes=assessment.rationale,
            entity=preview.entity,
            observation_title=preview.title,
            observation_timestamp=preview.timestamp,
            reviewer=preview.reviewer,
            reviewed_at=preview.reviewed_at,
            assessor=assessment.assessor,
            assessed_at=assessment.assessed_at,
        )


__all__ = ["HistoricalComparisonEvidenceConversionPreviewBuilder"]
