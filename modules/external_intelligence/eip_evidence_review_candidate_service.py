"""Build an EIP review manifest without creating or scoring Evidence."""

import json
from dataclasses import asdict
from hashlib import sha256

from modules.external_intelligence.eip_evidence_review_candidate import EIPEvidenceReviewCandidate, EIPEvidenceReviewReference
from modules.external_intelligence.eip_repository import EIPRepository, StoredEIPClassification
from modules.external_intelligence.eip_review import EIPReviewDecision, EIPReviewReceipt
from modules.external_intelligence.mandatory_meta_analysis_repository import MandatoryMetaAnalysisRepository, StoredMandatoryMetaAnalysis
from modules.external_intelligence.pre_inflection_repository import PreInflectionRepository, StoredPreInflectionAssessment
from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord


class EIPEvidenceReviewCandidateService:
    NON_AUTHORITY = "Review manifest only; it is not Evidence, a Signal, an Opportunity, a recommendation, or trade authority."

    def build(self, *, candidate_id, stored_eip, eip_review, stored_pre_inflection, stored_meta, temporal_evidence):
        candidate_id = self._text(candidate_id, "candidate_id")
        if not isinstance(stored_eip, StoredEIPClassification): raise ValueError("stored_eip must be StoredEIPClassification")
        if not isinstance(eip_review, EIPReviewReceipt): raise ValueError("eip_review must be EIPReviewReceipt")
        if not isinstance(stored_pre_inflection, StoredPreInflectionAssessment): raise ValueError("stored_pre_inflection must be StoredPreInflectionAssessment")
        if not isinstance(stored_meta, StoredMandatoryMetaAnalysis): raise ValueError("stored_meta must be StoredMandatoryMetaAnalysis")
        eip_fingerprint = EIPRepository.fingerprint_payload(EIPRepository.classification_payload(stored_eip.classification))
        if stored_eip.classification_fingerprint != eip_fingerprint: raise ValueError("stored EIP fingerprint mismatch")
        if eip_review.decision != EIPReviewDecision.AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW: raise ValueError("EIP is not authorized for downstream Evidence review")
        if (eip_review.classification_id, eip_review.classification_fingerprint, eip_review.stage) != (stored_eip.classification.classification_id, eip_fingerprint, stored_eip.classification.stage.value): raise ValueError("EIP review binding mismatch")
        pre_fingerprint = PreInflectionRepository.fingerprint_payload(PreInflectionRepository.preview_payload(stored_pre_inflection.preview))
        if stored_pre_inflection.preview_fingerprint != pre_fingerprint: raise ValueError("stored Pre-Inflection fingerprint mismatch")
        if (stored_eip.classification.pre_inflection_preview_id, stored_eip.classification.pre_inflection_fingerprint) != (stored_pre_inflection.preview.preview_id, pre_fingerprint): raise ValueError("EIP Pre-Inflection binding mismatch")
        meta_fingerprint = MandatoryMetaAnalysisRepository.fingerprint_payload(MandatoryMetaAnalysisRepository.assessment_payload(stored_meta.assessment))
        if stored_meta.assessment_fingerprint != meta_fingerprint: raise ValueError("stored Meta fingerprint mismatch")
        if (stored_pre_inflection.preview.meta_assessment_id, stored_pre_inflection.preview.meta_assessment_fingerprint) != (stored_meta.assessment.assessment_id, meta_fingerprint): raise ValueError("Pre-Inflection Meta binding mismatch")
        records = tuple(temporal_evidence)
        if not records or any(not isinstance(item, PublicTemporalEvidenceRecord) for item in records): raise ValueError("temporal_evidence must contain governed records")
        ids = tuple(sorted(item.temporal_evidence_id for item in records)); fingerprints = tuple(sorted(item.observation_fingerprint for item in records))
        if len(set(ids)) != len(ids) or len(set(fingerprints)) != len(fingerprints): raise ValueError("temporal evidence identities must be unique")
        if ids != tuple(sorted(stored_meta.assessment.input_temporal_evidence_ids)) or fingerprints != tuple(sorted(stored_meta.assessment.input_observation_fingerprints)): raise ValueError("Temporal Evidence does not match authorized Meta inputs")
        references = tuple(
            EIPEvidenceReviewReference(item.temporal_evidence_id, item.observation_fingerprint, item.entity, item.event_type, item.statement_posture, item.event_at, item.known_at, item.source_url, item.observation_title, item.observation_description)
            for item in sorted(records, key=lambda value: (value.known_at, value.temporal_evidence_id))
        )
        base = dict(
            schema_version=1, candidate_id=candidate_id, classification_id=stored_eip.classification.classification_id,
            classification_fingerprint=eip_fingerprint, eip_review_id=eip_review.review_id, eip_stage=eip_review.stage,
            pre_inflection_preview_id=stored_pre_inflection.preview.preview_id, pre_inflection_fingerprint=pre_fingerprint,
            meta_assessment_id=stored_meta.assessment.assessment_id, meta_assessment_fingerprint=meta_fingerprint,
            entity_scope=stored_meta.assessment.entity_scope, sector_scope=stored_meta.assessment.sector_scope,
            causal_indicator_ids=stored_meta.assessment.causal_indicator_ids, evidence_references=references,
            confirmation_requirements=stored_eip.classification.confirmation_requirements,
            invalidation_conditions=stored_eip.classification.invalidation_conditions,
            requires_human_evidence_assessment=True, non_authority_statement=self.NON_AUTHORITY,
        )
        payload = self._jsonable(base)
        fingerprint = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        return EIPEvidenceReviewCandidate(candidate_fingerprint=fingerprint, **base)

    @classmethod
    def _jsonable(cls, value):
        if isinstance(value, dict): return {key: cls._jsonable(item) for key, item in value.items()}
        if isinstance(value, (tuple, list)): return [cls._jsonable(item) for item in value]
        if hasattr(value, "isoformat"): return value.isoformat()
        if hasattr(value, "__dataclass_fields__"): return cls._jsonable(asdict(value))
        return value

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["EIPEvidenceReviewCandidateService"]
