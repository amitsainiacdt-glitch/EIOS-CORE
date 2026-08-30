"""Governed builder and evaluator for mandatory read-only Meta-Analysis."""

from dataclasses import dataclass
from datetime import datetime, timezone

from modules.external_intelligence.mandatory_meta_analysis import MandatoryMetaAnalysisAssessment, MetaAnalysisConclusion, MetaContradictionBurden, MetaKillTestResult
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaAnalysisGate, MandatoryMetaGateResult
from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord
from modules.external_intelligence.temporal_leading_indicator_preview import TemporalLeadingIndicatorPreview


@dataclass(frozen=True)
class MandatoryMetaAnalysisRunResult:
    assessment: MandatoryMetaAnalysisAssessment
    gate_result: MandatoryMetaGateResult


class MandatoryMetaAnalysisService:
    """Creates a source-bound assessment; it does not generate investment actions."""

    NON_AUTHORITY = "Read-only research assessment; not a Signal, Catalyst, Opportunity, recommendation, or trade decision."

    def __init__(self, gate, *, clock=None):
        if not isinstance(gate, MandatoryMetaAnalysisGate): raise ValueError("gate must be MandatoryMetaAnalysisGate")
        self.gate = gate
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def assess(
        self, *, assessment_id, temporal_evidence, indicator_previews, entity_scope, sector_scope,
        causal_hypotheses, contradictions, missing_expected_evidence, coverage_gaps,
        syndication_findings, cross_scope_transmissions, research_gaps, kill_test_results,
        conclusion, contradiction_burden, uncertainty_statement, assessor,
    ):
        records, previews = tuple(temporal_evidence), tuple(indicator_previews)
        if not records or not all(isinstance(item, PublicTemporalEvidenceRecord) for item in records): raise ValueError("temporal_evidence must not be empty")
        if not previews or not all(isinstance(item, TemporalLeadingIndicatorPreview) for item in previews): raise ValueError("indicator_previews must not be empty")
        if not all(isinstance(item, MetaKillTestResult) for item in kill_test_results): raise ValueError("kill_test_results are invalid")
        assessment = MandatoryMetaAnalysisAssessment(
            1, self._text(assessment_id, "assessment_id"), self._texts(entity_scope, "entity_scope"),
            self._texts(sector_scope, "sector_scope"), tuple(sorted(item.temporal_evidence_id for item in records)),
            tuple(sorted(item.observation_fingerprint for item in records)),
            tuple(sorted(item.preview_fingerprint for item in previews)), tuple(sorted({item.indicator_id for item in previews})),
            self._texts(causal_hypotheses, "causal_hypotheses"),
            tuple(sorted({group for item in previews for group in item.independence_group_ids})),
            self._texts(contradictions, "contradictions"), self._texts(missing_expected_evidence, "missing_expected_evidence"),
            self._texts(coverage_gaps, "coverage_gaps"), self._texts(syndication_findings, "syndication_findings"),
            self._texts(cross_scope_transmissions, "cross_scope_transmissions"), self._texts(research_gaps, "research_gaps"),
            tuple(kill_test_results), conclusion if isinstance(conclusion, MetaAnalysisConclusion) else MetaAnalysisConclusion(conclusion),
            contradiction_burden if isinstance(contradiction_burden, MetaContradictionBurden) else MetaContradictionBurden(contradiction_burden),
            True, True, True, True, True, True, self._text(uncertainty_statement, "uncertainty_statement"),
            self.NON_AUTHORITY, self.clock(), self._text(assessor, "assessor"),
        )
        result = self.gate.evaluate(temporal_evidence=records, assessment=assessment, indicator_previews=previews)
        return MandatoryMetaAnalysisRunResult(assessment, result)

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(item, name) for item in values)
        if len(set(result)) != len(result): raise ValueError(f"{name} must be unique")
        return result


__all__ = ["MandatoryMetaAnalysisRunResult", "MandatoryMetaAnalysisService"]
