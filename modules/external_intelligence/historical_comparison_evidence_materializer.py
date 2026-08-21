"""Explicit materialization of one assessed historical comparison EvidenceItem."""

from __future__ import annotations

from modules.external_intelligence.evidence_assessment import EvidenceAssessment
from modules.external_intelligence.evidence_intake import ExternalEvidenceIntake
from modules.external_intelligence.historical_comparison_accepted_observation_preview import (
    HistoricalComparisonAcceptedObservationPreview,
)
from modules.external_intelligence.historical_comparison_evidence_assessment import (
    HistoricalComparisonEvidenceAssessment,
)
from modules.observation.observation import Observation, ObservationProvenance
from modules.opportunity.evidence_engine import EvidenceItem


class HistoricalComparisonEvidenceMaterializer:
    """Use the canonical intake without publication or opportunity analysis."""

    def __init__(self, intake: ExternalEvidenceIntake | None = None) -> None:
        self.intake = intake if intake is not None else ExternalEvidenceIntake()

    def materialize(
        self,
        preview: HistoricalComparisonAcceptedObservationPreview,
        assessment: HistoricalComparisonEvidenceAssessment,
    ) -> EvidenceItem:
        if not isinstance(preview, HistoricalComparisonAcceptedObservationPreview):
            raise ValueError("preview must be an accepted observation preview")
        if not isinstance(assessment, HistoricalComparisonEvidenceAssessment):
            raise ValueError("assessment must be a historical Evidence assessment")
        if assessment.candidate_id != preview.candidate_id:
            raise ValueError("assessment candidate identity mismatch")
        if assessment.observation_fingerprint != preview.content_fingerprint:
            raise ValueError("assessment observation fingerprint mismatch")

        observation = Observation(
            title=preview.title,
            description=preview.description,
            source=preview.source,
            category=preview.category,
            entity=preview.entity,
            confidence=preview.confidence,
            timestamp=preview.timestamp,
            provenance=ObservationProvenance(
                cycle_id=preview.cycle_id,
                job_id=preview.job_id,
                research_intent=preview.research_intent,
                retrieved_at=preview.retrieved_at,
                source_url=preview.source_url,
                source_domain=preview.source_domain,
                source_type=preview.source_type,
                content_fingerprint=preview.content_fingerprint,
            ),
        )
        explicit_assessment = EvidenceAssessment(
            category=assessment.category,
            direction=assessment.direction,
            strength=assessment.strength,
            confidence=assessment.confidence,
            independent_confirmation=assessment.independent_confirmation,
            is_primary_source=assessment.is_primary_source,
            is_time_sensitive=assessment.is_time_sensitive,
            notes=assessment.rationale,
        )
        return self.intake.assess(
            observation=observation,
            assessment=explicit_assessment,
            evidence_id=f"HC-{preview.candidate_id}",
        )


__all__ = ["HistoricalComparisonEvidenceMaterializer"]
