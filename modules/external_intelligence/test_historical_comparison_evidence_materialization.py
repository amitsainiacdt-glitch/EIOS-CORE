"""No-network validation for explicit historical EvidenceItem creation."""

import io
from contextlib import redirect_stdout
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
from modules.opportunity.evidence_engine import EvidenceItem, OpportunityEvidenceEngine
from scripts.materialize_historical_comparison_evidence import main as materialize_main


def accepted(candidate):
    return HistoricalComparisonReviewService().review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Accepted for controlled Evidence materialization.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=5),
    )


def assessed(path, preview):
    return HistoricalComparisonEvidenceAssessmentLedger(path).record(
        preview,
        category="Company filing",
        direction="Supporting",
        strength=88.0,
        confidence=81.0,
        independent_confirmation=2,
        is_primary_source=True,
        is_time_sensitive=False,
        assessor="Human Assessor",
        rationale="Explicit human assessment for one EvidenceItem.",
        assessed_at=preview.reviewed_at + timedelta(minutes=5),
    )


class FailingMaterializer:
    def materialize(self, preview, assessment):
        raise AssertionError("duplicate reached materializer")


def validate_ledger(root, preview, assessment) -> None:
    path = root / "direct-receipts.jsonl"
    ledger = HistoricalComparisonEvidenceConversionReceiptLedger(path)
    converted_at = assessment.assessed_at + timedelta(minutes=5)
    evidence, receipt = ledger.materialize(
        preview,
        assessment,
        converter="Human Converter",
        converted_at=converted_at,
    )
    assert isinstance(evidence, EvidenceItem)
    assert evidence.evidence_id == f"HC-{preview.candidate_id}"
    assert evidence.statement == preview.description
    assert evidence.direction == assessment.direction
    assert evidence.strength == assessment.strength
    assert receipt.evidence_id == evidence.evidence_id
    assert ledger.read_all() == (receipt,)
    before = path.read_bytes()

    try:
        ledger.materialize(
            preview,
            assessment,
            converter="Second Converter",
            converted_at=converted_at,
            materializer=FailingMaterializer(),
        )
        raise AssertionError("duplicate conversion was accepted")
    except ValueError as exc:
        assert "already exists" in str(exc).casefold()
    assert path.read_bytes() == before

    early = HistoricalComparisonEvidenceConversionReceiptLedger(
        root / "early-receipt.jsonl"
    )
    try:
        early.materialize(
            preview,
            assessment,
            converter="Human Converter",
            converted_at=assessment.assessed_at - timedelta(seconds=1),
        )
        raise AssertionError("early conversion was accepted")
    except ValueError as exc:
        assert "precedes" in str(exc).casefold()
    assert not early.path.exists()


def validate_command(root, audit_path, candidate, observation) -> None:
    review_path = root / "reviews.jsonl"
    observation_path = root / "observations.json"
    assessment_path = root / "assessments.jsonl"
    receipt_path = root / "receipts.jsonl"
    reviewed = accepted(candidate)
    HistoricalComparisonReviewDecisionLedger(review_path).record(reviewed)
    ObservationPersistence(observation_path).save([observation])
    preview = HistoricalComparisonAcceptedObservationResolver().resolve(
        reviewed, [observation]
    )
    assessment = assessed(assessment_path, preview)
    source_paths = (audit_path, review_path, observation_path, assessment_path)
    source_before = {path: path.read_bytes() for path in source_paths}

    output = io.StringIO()
    with (
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
        result = materialize_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(assessment_path),
                "--receipt-path", str(receipt_path),
                "--candidate-id", candidate.candidate_id,
                "--converter", "Human Converter",
                "--converted-at", (
                    assessment.assessed_at + timedelta(minutes=5)
                ).isoformat(),
            ]
        )
    assert result == 0
    assert publish.call_count == 0
    assert analyze.call_count == 0
    text = output.getvalue()
    assert f"Created EvidenceItem: HC-{candidate.candidate_id}" in text
    assert "No Intelligence was published." in text
    assert "No Opportunity was scored." in text
    receipts = HistoricalComparisonEvidenceConversionReceiptLedger(
        receipt_path
    ).read_all()
    assert len(receipts) == 1
    for path, content in source_before.items():
        assert path.read_bytes() == content

    receipt_before = receipt_path.read_bytes()
    duplicate_output = io.StringIO()
    with redirect_stdout(duplicate_output):
        duplicate = materialize_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(assessment_path),
                "--receipt-path", str(receipt_path),
                "--candidate-id", candidate.candidate_id,
                "--converter", "Human Converter",
                "--converted-at", (
                    assessment.assessed_at + timedelta(minutes=6)
                ).isoformat(),
            ]
        )
    assert duplicate == 1
    assert receipt_path.read_bytes() == receipt_before


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        observation = make_observation(candidate)
        reviewed = accepted(candidate)
        preview = HistoricalComparisonAcceptedObservationResolver().resolve(
            reviewed, [observation]
        )
        assessment = assessed(root / "direct-assessments.jsonl", preview)
        validate_ledger(root, preview, assessment)
        validate_command(root, audit_path, candidate, observation)
    print("HISTORICAL EVIDENCE MATERIALIZATION: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
