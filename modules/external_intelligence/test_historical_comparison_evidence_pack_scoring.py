"""No-network validation for explicit entity Evidence pack scoring."""

import io
from contextlib import redirect_stdout
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence import test_historical_comparison_audit_reader_summary as audit_test
from modules.external_intelligence.evidence_intelligence_adapter import EvidenceIntelligenceAdapter
from modules.external_intelligence.historical_comparison_accepted_observation_resolver import HistoricalComparisonAcceptedObservationResolver
from modules.external_intelligence.historical_comparison_audit_reader import HistoricalComparisonAuditReader
from modules.external_intelligence.historical_comparison_evidence_assessment_ledger import HistoricalComparisonEvidenceAssessmentLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.historical_comparison_evidence_receipt_reconciler import HistoricalComparisonEvidenceReceiptReconciler
from modules.external_intelligence.historical_comparison_review_candidate import HistoricalComparisonReviewStatus
from modules.external_intelligence.historical_comparison_review_candidate_builder import HistoricalComparisonReviewCandidateBuilder
from modules.external_intelligence.historical_comparison_review_decision_ledger import HistoricalComparisonReviewDecisionLedger
from modules.external_intelligence.historical_comparison_review_service import HistoricalComparisonReviewService
from modules.external_intelligence.test_historical_comparison_accepted_observation_preview import make_observation
from modules.observation.observation_persistence import ObservationPersistence
from modules.opportunity.catalyst.catalyst_classifier import CatalystClassifier
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine
from scripts.analyze_historical_comparison_entity_evidence_pack import main as analyze_main


def build_chain(root, audit_path):
    candidate = HistoricalComparisonReviewCandidateBuilder().build(
        HistoricalComparisonAuditReader(audit_path).read_all()
    )[0]
    observation = make_observation(candidate)
    reviewed = HistoricalComparisonReviewService().review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Accepted for controlled scoring.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=5),
    )
    review_path = root / "reviews.jsonl"
    observation_path = root / "observations.json"
    assessment_path = root / "assessments.jsonl"
    conversion_path = root / "conversions.jsonl"
    HistoricalComparisonReviewDecisionLedger(review_path).record(reviewed)
    ObservationPersistence(observation_path).save([observation])
    preview = HistoricalComparisonAcceptedObservationResolver().resolve(reviewed, [observation])
    assessment = HistoricalComparisonEvidenceAssessmentLedger(assessment_path).record(
        preview,
        category="Company filing",
        direction="Supporting",
        strength=90.0,
        confidence=84.0,
        independent_confirmation=2,
        is_primary_source=True,
        is_time_sensitive=False,
        assessor="Human Assessor",
        rationale="Explicit input to Evidence pack scoring.",
        assessed_at=preview.reviewed_at + timedelta(minutes=5),
    )
    receipt = HistoricalComparisonEvidenceConversionReceiptLedger(conversion_path).materialize(
        preview,
        assessment,
        converter="Human Converter",
        converted_at=assessment.assessed_at + timedelta(minutes=5),
    )[1]
    pack = HistoricalComparisonEvidenceReceiptReconciler().reconcile(
        [preview], [assessment], [receipt]
    ).entity_packs[0]
    return candidate, observation, assessment, receipt, pack, (
        review_path, observation_path, assessment_path, conversion_path
    )


class FailingAnalyzer:
    def analyze(self, pack):
        raise AssertionError("duplicate reached scoring engine")


def validate_ledger(root, pack, receipt):
    path = root / "direct-scores.jsonl"
    ledger = HistoricalComparisonEvidencePackScoringLedger(path)
    analyzed_at = receipt.converted_at + timedelta(minutes=5)
    result, scoring = ledger.analyze(
        pack, analyst="Human Analyst", analyzed_at=analyzed_at
    )
    assert result.company == pack.entity
    assert len(result.supporting_evidence) == 1
    assert result.supporting_evidence[0].evidence_id == receipt.evidence_id
    assert result.contradictory_evidence == []
    assert "No contradictory evidence documented." in result.evidence_gaps
    assert "No explicit assumptions documented." in result.evidence_gaps
    assert scoring.evidence_score == result.evidence_score
    assert ledger.read_all() == (scoring,)
    before = path.read_bytes()
    try:
        ledger.analyze(
            pack,
            analyst="Second Analyst",
            analyzed_at=analyzed_at,
            analyzer=FailingAnalyzer(),
        )
        raise AssertionError("duplicate pack score was accepted")
    except ValueError as exc:
        assert "already scored" in str(exc).casefold()
    assert path.read_bytes() == before


def validate_command(root, audit_path, chain):
    candidate, observation, assessment, receipt, pack, source_paths = chain
    review_path, observation_path, assessment_path, conversion_path = source_paths
    scoring_path = root / "scores.jsonl"
    all_sources = (audit_path,) + source_paths
    before = {path: path.read_bytes() for path in all_sources}
    output = io.StringIO()
    with (
        patch.object(EvidenceIntelligenceAdapter, "publish", side_effect=AssertionError("publish")) as publish,
        patch.object(SignalInterpretationEngine, "create", side_effect=AssertionError("signal")) as signal,
        patch.object(CatalystClassifier, "classify", side_effect=AssertionError("catalyst")) as catalyst,
        redirect_stdout(output),
    ):
        result = analyze_main([
            "--audit-path", str(audit_path),
            "--review-ledger-path", str(review_path),
            "--observation-path", str(observation_path),
            "--assessment-ledger-path", str(assessment_path),
            "--conversion-receipt-path", str(conversion_path),
            "--scoring-receipt-path", str(scoring_path),
            "--entity", observation.entity,
            "--analyst", "Human Analyst",
            "--analyzed-at", (receipt.converted_at + timedelta(minutes=5)).isoformat(),
        ])
    assert result == 0
    assert publish.call_count == signal.call_count == catalyst.call_count == 0
    assert "Scoring receipt appended." in output.getvalue()
    assert "No Signal or Catalyst was created." in output.getvalue()
    scores = HistoricalComparisonEvidencePackScoringLedger(scoring_path).read_all()
    assert len(scores) == 1
    assert scores[0].entity == observation.entity
    for path, content in before.items():
        assert path.read_bytes() == content


def main():
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        chain = build_chain(root, audit_path)
        validate_ledger(root, chain[4], chain[3])
        validate_command(root, audit_path, chain)
    print("HISTORICAL ENTITY EVIDENCE PACK SCORING: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
