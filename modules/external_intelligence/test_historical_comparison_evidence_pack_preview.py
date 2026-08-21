"""No-network validation for entity-scoped materialized Evidence previews."""

import io
import json
from contextlib import redirect_stdout
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence import (
    test_historical_comparison_audit_reader_summary as audit_test,
)
from modules.external_intelligence.evidence_intelligence_adapter import (
    EvidenceIntelligenceAdapter,
)
from modules.external_intelligence.historical_comparison_accepted_observation_resolver import (
    HistoricalComparisonAcceptedObservationResolver,
)
from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_evidence_assessment_ledger import (
    HistoricalComparisonEvidenceAssessmentLedger,
)
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import (
    HistoricalComparisonEvidenceConversionReceiptLedger,
)
from modules.external_intelligence.historical_comparison_evidence_materializer import (
    HistoricalComparisonEvidenceMaterializer,
)
from modules.external_intelligence.historical_comparison_evidence_receipt_reconciler import (
    HistoricalComparisonEvidenceReceiptReconciler,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence.historical_comparison_review_candidate_builder import (
    HistoricalComparisonReviewCandidateBuilder,
)
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_service import (
    HistoricalComparisonReviewService,
)
from modules.external_intelligence.test_historical_comparison_accepted_observation_preview import (
    make_observation,
)
from modules.observation.observation_persistence import ObservationPersistence
from modules.opportunity.evidence_engine import OpportunityEvidenceEngine
from scripts.preview_historical_comparison_entity_evidence_packs import (
    main as preview_main,
)


def accept(candidate):
    return HistoricalComparisonReviewService().review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Accepted for entity pack validation.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=5),
    )


def assess(path, preview):
    return HistoricalComparisonEvidenceAssessmentLedger(path).record(
        preview,
        category="Company filing",
        direction="Supporting",
        strength=86.0,
        confidence=80.0,
        independent_confirmation=2,
        is_primary_source=True,
        is_time_sensitive=False,
        assessor="Human Assessor",
        rationale="Explicit assessment for receipt reconciliation.",
        assessed_at=preview.reviewed_at + timedelta(minutes=5),
    )


def materialize(path, preview, assessment):
    return HistoricalComparisonEvidenceConversionReceiptLedger(path).materialize(
        preview,
        assessment,
        converter="Human Converter",
        converted_at=assessment.assessed_at + timedelta(minutes=5),
    )[1]


def validate_reconciler(root, preview) -> None:
    assessment = assess(root / "direct-assessment.jsonl", preview)
    receipt = materialize(root / "direct-receipt.jsonl", preview, assessment)
    second = replace(
        preview,
        candidate_id="1" * 64,
        content_fingerprint="2" * 64,
        entity="Second Entity",
    )
    result = HistoricalComparisonEvidenceReceiptReconciler().reconcile(
        [preview, second], [assessment], [receipt]
    )
    assert result.accepted_count == 2
    assert result.assessment_count == 1
    assert result.receipt_count == 1
    assert len(result.entity_packs) == 2
    first = next(pack for pack in result.entity_packs if pack.entity == preview.entity)
    assert first.materialized_count == 1
    assert first.supporting_evidence_ids == (receipt.evidence_id,)
    assert first.contradictory_evidence_ids == ()
    second_pack = next(
        pack for pack in result.entity_packs if pack.entity == "Second Entity"
    )
    assert second_pack.missing_assessment_candidate_ids == (second.candidate_id,)

    invalid_cases = (
        ([replace(receipt, statement="Tampered")], "statement"),
        ([replace(receipt, candidate_id="0" * 64)], "unknown"),
        ([receipt, receipt], "multiple"),
    )
    for receipts, expected in invalid_cases:
        try:
            HistoricalComparisonEvidenceReceiptReconciler().reconcile(
                [preview], [assessment], receipts
            )
            raise AssertionError(f"Invalid receipt accepted: {expected}")
        except ValueError as exc:
            assert expected in str(exc).casefold()


def validate_command(root, audit_path, candidate, observation) -> None:
    review_path = root / "reviews.jsonl"
    observation_path = root / "observations.json"
    assessment_path = root / "assessments.jsonl"
    receipt_path = root / "receipts.jsonl"
    reviewed = accept(candidate)
    HistoricalComparisonReviewDecisionLedger(review_path).record(reviewed)
    ObservationPersistence(observation_path).save([observation])
    preview = HistoricalComparisonAcceptedObservationResolver().resolve(
        reviewed, [observation]
    )
    assessment = assess(assessment_path, preview)
    receipt = materialize(receipt_path, preview, assessment)
    paths = (audit_path, review_path, observation_path, assessment_path, receipt_path)
    before = {path: path.read_bytes() for path in paths}
    output = io.StringIO()
    with (
        patch.object(
            HistoricalComparisonEvidenceMaterializer,
            "materialize",
            side_effect=AssertionError("new Evidence creation attempted"),
        ) as materializer,
        patch.object(
            EvidenceIntelligenceAdapter,
            "publish",
            side_effect=AssertionError("Intelligence publication attempted"),
        ) as publish,
        patch.object(
            OpportunityEvidenceEngine,
            "analyze",
            side_effect=AssertionError("Opportunity scoring attempted"),
        ) as analyze,
        redirect_stdout(output),
    ):
        result = preview_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(assessment_path),
                "--receipt-path", str(receipt_path),
                "--json",
            ]
        )
    assert result == 0
    assert materializer.call_count == 0
    assert publish.call_count == 0
    assert analyze.call_count == 0
    payload = json.loads(output.getvalue())
    assert payload["accepted_count"] == 1
    assert payload["assessment_count"] == 1
    assert payload["receipt_count"] == 1
    assert payload["entity_pack_count"] == 1
    pack = payload["entity_packs"][0]
    assert pack["entity"] == observation.entity
    assert pack["supporting_evidence_ids"] == [receipt.evidence_id]
    assert pack["missing_assessment_candidate_ids"] == []
    assert pack["missing_receipt_candidate_ids"] == []
    assert payload["new_evidence_created"] is False
    assert payload["intelligence_published"] is False
    assert payload["opportunity_scoring_performed"] is False
    for path, content in before.items():
        assert path.read_bytes() == content


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        observation = make_observation(candidate)
        preview = HistoricalComparisonAcceptedObservationResolver().resolve(
            accept(candidate), [observation]
        )
        validate_reconciler(root, preview)
        validate_command(root, audit_path, candidate, observation)
    print("HISTORICAL ENTITY EVIDENCE PACK PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
