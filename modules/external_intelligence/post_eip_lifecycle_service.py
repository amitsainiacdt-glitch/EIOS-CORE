"""Classifies later evidence without backdating it into the original EIP."""

from modules.external_intelligence.post_eip_lifecycle import (
    PostEIPConfirmationType, PostEIPEvidence, PostEIPLifecycleAction,
    PostEIPLifecycleAssessment, PostEIPLifecycleResult, PostEIPRelationship,
)
from modules.external_intelligence.reader_eip_classification import ReaderEIPClassification, ReaderEIPClassificationResult


class PostEIPLifecycleService:
    NON_AUTHORITY = "Post-EIP thesis monitoring only; not a portfolio instruction, order, or trade authorization."
    MINIMUM_SCALE_CONFIRMATION_GROUPS = 2

    def evaluate(self, *, reader_classification, assessment):
        if not isinstance(reader_classification, ReaderEIPClassificationResult):
            raise ValueError("reader_classification must be ReaderEIPClassificationResult")
        if reader_classification.classification not in (
                ReaderEIPClassification.EARLIEST_INVESTABLE_POINT,
                ReaderEIPClassification.BUY_ZONE_CANDIDATE):
            raise ValueError("post-EIP lifecycle requires a governed EIP or Buy-Zone Candidate")
        if not isinstance(assessment, PostEIPLifecycleAssessment):
            raise ValueError("assessment must be PostEIPLifecycleAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported post-EIP lifecycle schema")
        self._text(assessment.assessment_id, "assessment_id")
        if assessment.reader_packet_fingerprint != reader_classification.packet_fingerprint:
            raise ValueError("post-EIP lifecycle does not bind to reader packet")
        if assessment.eip_identified_at.tzinfo is None:
            raise ValueError("eip_identified_at must be timezone-aware")
        if not assessment.public_information_only:
            raise ValueError("post-EIP lifecycle accepts public information only")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("post-EIP lifecycle requires the canonical non-authority statement")
        self._texts(assessment.unresolved_uncertainties, "unresolved_uncertainties", allow_empty=True)
        self._texts(assessment.monitoring_requirements, "monitoring_requirements")
        if not isinstance(assessment.evidence, tuple):
            raise ValueError("evidence must be a tuple")

        ids = set()
        confirms, contradicts, groups, kills = [], [], set(), []
        for item in assessment.evidence:
            if not isinstance(item, PostEIPEvidence):
                raise ValueError("evidence must contain PostEIPEvidence values")
            evidence_id = self._text(item.evidence_id, "evidence_id")
            if evidence_id in ids:
                raise ValueError("post-EIP evidence IDs must be unique")
            ids.add(evidence_id)
            if not isinstance(item.confirmation_type, PostEIPConfirmationType):
                raise ValueError("post-EIP confirmation type is invalid")
            if not isinstance(item.relationship, PostEIPRelationship):
                raise ValueError("post-EIP relationship is invalid")
            if item.observed_at.tzinfo is None:
                raise ValueError("post-EIP evidence time must be timezone-aware")
            if item.observed_at <= assessment.eip_identified_at:
                raise ValueError("post-EIP evidence must be known after the original EIP")
            self._texts(item.source_ids, "post-EIP source_ids")
            group = self._text(item.independence_group_id, "independence_group_id")
            self._text(item.explanation, "evidence explanation")
            if item.triggered_kill_test is not None:
                kills.append(self._text(item.triggered_kill_test, "triggered_kill_test"))
            if item.relationship == PostEIPRelationship.CONFIRMS:
                confirms.append(evidence_id); groups.add(group)
            elif item.relationship == PostEIPRelationship.CONTRADICTS:
                contradicts.append(evidence_id)

        reasons = []
        if kills:
            action = PostEIPLifecycleAction.KILL_THESIS_REVIEW
            reasons.append("FORWARD_KILL_TEST_TRIGGERED")
        elif contradicts:
            action = PostEIPLifecycleAction.HOLD
            reasons.append("POST_EIP_CONTRADICTION_REQUIRES_REVIEW")
        elif len(groups) >= self.MINIMUM_SCALE_CONFIRMATION_GROUPS:
            action = PostEIPLifecycleAction.SCALE_REVIEW
            reasons.append("INDEPENDENT_POST_EIP_CONFIRMATION_PRESENT")
        else:
            action = PostEIPLifecycleAction.WAIT_FOR_CONFIRMATION
            reasons.append("INDEPENDENT_POST_EIP_CONFIRMATION_INSUFFICIENT")
        if assessment.unresolved_uncertainties and action == PostEIPLifecycleAction.SCALE_REVIEW:
            action = PostEIPLifecycleAction.HOLD
            reasons.append("UNRESOLVED_UNCERTAINTY_BLOCKS_SCALE_REVIEW")
        return PostEIPLifecycleResult(
            assessment.assessment_id, action, tuple(confirms), tuple(contradicts), tuple(sorted(groups)),
            tuple(kills), tuple(reasons), False, False, self.NON_AUTHORITY,
        )

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name, *, allow_empty=False):
        if not isinstance(values, tuple):
            raise ValueError(f"{name} must be a tuple")
        result = tuple(cls._text(value, name) for value in values)
        if not allow_empty and not result:
            raise ValueError(f"{name} must not be empty")
        if len(set(result)) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result


__all__ = ["PostEIPLifecycleService"]
