"""Mandatory fail-closed gate between Temporal Evidence and Pre-Inflection."""

from dataclasses import dataclass
from enum import Enum

from modules.external_intelligence.mandatory_meta_analysis import MandatoryMetaAnalysisAssessment, MetaAnalysisConclusion, MetaContradictionBurden, MetaKillTestResult, MetaKillTestStatus
from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry
from modules.external_intelligence.temporal_leading_indicator_preview import TemporalLeadingIndicatorPreview
from modules.external_intelligence.temporal_leading_indicator_preview import TemporalIndicatorStructuralState


class MandatoryMetaGateDecision(str, Enum):
    READY_FOR_PRE_INFLECTION = "READY_FOR_PRE_INFLECTION"
    HOLD_FOR_RESEARCH = "HOLD_FOR_RESEARCH"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class MandatoryMetaGateResult:
    decision: MandatoryMetaGateDecision
    reason_codes: tuple[str, ...]
    assessment_id: str | None
    expected_temporal_evidence_ids: tuple[str, ...]
    meta_required: bool = True


class MandatoryMetaAnalysisGate:
    """No downstream promotion may treat an absent Meta assessment as optional."""

    def __init__(self, causal_indicator_registry):
        if not isinstance(causal_indicator_registry, SectorCausalIndicatorRegistry):
            raise ValueError("causal_indicator_registry must be SectorCausalIndicatorRegistry")
        self.causal_indicator_registry = causal_indicator_registry

    def evaluate(self, *, temporal_evidence, assessment, indicator_previews=()):
        records = tuple(temporal_evidence)
        if not records or not all(isinstance(item, PublicTemporalEvidenceRecord) for item in records):
            raise ValueError("temporal_evidence must contain reviewed Temporal Evidence")
        expected_ids = tuple(sorted(item.temporal_evidence_id for item in records))
        reasons = []
        if assessment is None:
            return MandatoryMetaGateResult(MandatoryMetaGateDecision.BLOCKED, ("META_ASSESSMENT_MISSING",), None, expected_ids)
        if not isinstance(assessment, MandatoryMetaAnalysisAssessment):
            raise ValueError("assessment must be MandatoryMetaAnalysisAssessment or None")
        indicator_previews = tuple(indicator_previews)
        if not indicator_previews or not all(isinstance(item, TemporalLeadingIndicatorPreview) for item in indicator_previews):
            reasons.append("INDICATOR_PREVIEW_MISSING")
        else:
            expected_previews = tuple(sorted(item.preview_fingerprint for item in indicator_previews))
            if tuple(sorted(assessment.input_indicator_preview_fingerprints)) != expected_previews:
                reasons.append("INDICATOR_PREVIEW_BINDING_MISMATCH")
            preview_evidence_ids = {value for item in indicator_previews for value in item.temporal_evidence_ids}
            if not preview_evidence_ids.issubset(set(expected_ids)):
                reasons.append("INDICATOR_PREVIEW_EVIDENCE_MISMATCH")
            if {item.indicator_id for item in indicator_previews} != set(assessment.causal_indicator_ids):
                reasons.append("CAUSAL_INDICATOR_PREVIEW_MISMATCH")
        if assessment.schema_version != 1:
            reasons.append("META_SCHEMA_UNSUPPORTED")
        if tuple(sorted(assessment.input_temporal_evidence_ids)) != expected_ids:
            reasons.append("TEMPORAL_EVIDENCE_BINDING_MISMATCH")
        expected_observations = tuple(sorted(item.observation_fingerprint for item in records))
        if tuple(sorted(assessment.input_observation_fingerprints)) != expected_observations:
            reasons.append("OBSERVATION_BINDING_MISMATCH")
        if len(set(assessment.input_temporal_evidence_ids)) != len(assessment.input_temporal_evidence_ids):
            reasons.append("DUPLICATE_META_INPUT")
        if not assessment.public_information_only:
            reasons.append("NON_PUBLIC_INFORMATION_PROHIBITED")
        checks = (
            (assessment.independence_checked, "INDEPENDENCE_CHECK_MISSING"),
            (assessment.contradictions_checked, "CONTRADICTION_CHECK_MISSING"),
            (assessment.missing_evidence_checked, "MISSING_EVIDENCE_CHECK_MISSING"),
            (assessment.coverage_checked, "COVERAGE_CHECK_MISSING"),
            (assessment.kill_tests_checked, "KILL_TEST_CHECK_MISSING"),
        )
        reasons.extend(code for completed, code in checks if not completed)
        if not assessment.uncertainty_statement.strip(): reasons.append("UNCERTAINTY_NOT_STATED")
        if not assessment.non_authority_statement.strip(): reasons.append("NON_AUTHORITY_NOT_STATED")
        if not assessment.entity_scope and not assessment.sector_scope: reasons.append("META_SCOPE_MISSING")
        if not assessment.causal_indicator_ids:
            reasons.append("CAUSAL_INDICATOR_MISSING")
        else:
            for indicator_id in assessment.causal_indicator_ids:
                try:
                    definition = self.causal_indicator_registry.get(indicator_id)
                except ValueError:
                    reasons.append("CAUSAL_INDICATOR_UNKNOWN")
                    continue
                assessment_sectors = {value.casefold() for value in assessment.sector_scope}
                definition_sectors = {value.casefold() for value in definition.sector_ids}
                if assessment.sector_scope and not assessment_sectors.intersection(definition_sectors):
                    reasons.append("CAUSAL_INDICATOR_SCOPE_MISMATCH")
            if not any(code in reasons for code in ("CAUSAL_INDICATOR_UNKNOWN", "CAUSAL_INDICATOR_MISSING")):
                if self.causal_indicator_registry.missing_dependencies(assessment.causal_indicator_ids):
                    reasons.append("CAUSAL_INDICATOR_DEPENDENCY_MISSING")
        blocking = {
            "META_SCHEMA_UNSUPPORTED", "TEMPORAL_EVIDENCE_BINDING_MISMATCH", "OBSERVATION_BINDING_MISMATCH",
            "DUPLICATE_META_INPUT", "NON_PUBLIC_INFORMATION_PROHIBITED", "INDEPENDENCE_CHECK_MISSING",
            "CONTRADICTION_CHECK_MISSING", "MISSING_EVIDENCE_CHECK_MISSING", "COVERAGE_CHECK_MISSING",
            "UNCERTAINTY_NOT_STATED", "NON_AUTHORITY_NOT_STATED", "META_SCOPE_MISSING",
            "CAUSAL_INDICATOR_MISSING", "CAUSAL_INDICATOR_UNKNOWN", "CAUSAL_INDICATOR_SCOPE_MISMATCH",
            "CAUSAL_INDICATOR_DEPENDENCY_MISSING",
            "INDICATOR_PREVIEW_MISSING", "INDICATOR_PREVIEW_BINDING_MISMATCH", "INDICATOR_PREVIEW_EVIDENCE_MISMATCH",
            "CAUSAL_INDICATOR_PREVIEW_MISMATCH",
            "KILL_TEST_CHECK_MISSING", "KILL_TEST_COVERAGE_MISMATCH", "KILL_TEST_EVIDENCE_MISMATCH",
        }
        expected_kill_tests = {
            (indicator_id, kill_test)
            for indicator_id in assessment.causal_indicator_ids
            for kill_test in self.causal_indicator_registry.get(indicator_id).kill_tests
        } if not any(code in reasons for code in ("CAUSAL_INDICATOR_UNKNOWN", "CAUSAL_INDICATOR_MISSING")) else set()
        supplied_kill_tests = {
            (item.indicator_id, item.kill_test)
            for item in assessment.kill_test_results
            if isinstance(item, MetaKillTestResult)
        }
        if expected_kill_tests != supplied_kill_tests:
            reasons.append("KILL_TEST_COVERAGE_MISMATCH")
        if any(not set(item.evidence_ids).issubset(set(expected_ids)) for item in assessment.kill_test_results if isinstance(item, MetaKillTestResult)):
            reasons.append("KILL_TEST_EVIDENCE_MISMATCH")
        if blocking.intersection(reasons):
            return MandatoryMetaGateResult(MandatoryMetaGateDecision.BLOCKED, tuple(reasons), assessment.assessment_id, expected_ids)
        if assessment.conclusion in (MetaAnalysisConclusion.INSUFFICIENT, MetaAnalysisConclusion.CONTRADICTED):
            reasons.append("META_CONCLUSION_NOT_READY")
        if assessment.contradiction_burden == MetaContradictionBurden.HIGH:
            reasons.append("HIGH_CONTRADICTION_BURDEN")
        if len(set(assessment.independence_group_ids)) < 2:
            reasons.append("INDEPENDENT_SUPPORT_INSUFFICIENT")
        if not assessment.causal_hypotheses:
            reasons.append("CAUSAL_HYPOTHESIS_MISSING")
        if indicator_previews and any(item.structural_state != TemporalIndicatorStructuralState.STRUCTURALLY_READY_FOR_META for item in indicator_previews):
            reasons.append("INDICATOR_PREVIEW_NOT_STRUCTURALLY_READY")
        if any(item.status == MetaKillTestStatus.TRIGGERED for item in assessment.kill_test_results):
            reasons.append("KILL_TEST_TRIGGERED")
        if any(item.status == MetaKillTestStatus.UNKNOWN for item in assessment.kill_test_results):
            reasons.append("KILL_TEST_UNRESOLVED")
        if reasons:
            return MandatoryMetaGateResult(MandatoryMetaGateDecision.HOLD_FOR_RESEARCH, tuple(reasons), assessment.assessment_id, expected_ids)
        return MandatoryMetaGateResult(MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION, (), assessment.assessment_id, expected_ids)


__all__ = ["MandatoryMetaAnalysisGate", "MandatoryMetaGateDecision", "MandatoryMetaGateResult"]
