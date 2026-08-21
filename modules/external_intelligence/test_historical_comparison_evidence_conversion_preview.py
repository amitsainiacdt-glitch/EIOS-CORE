"""No-network validation for read-only Evidence conversion previews."""

import io
import json
from contextlib import redirect_stdout
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence import (
    test_historical_comparison_audit_reader_summary as audit_test,
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
from modules.external_intelligence.historical_comparison_evidence_conversion_preview_builder import (
    HistoricalComparisonEvidenceConversionPreviewBuilder,
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
from scripts.preview_historical_comparison_evidence_conversion import (
    main as preview_main,
)


def accept(candidate):
    return HistoricalComparisonReviewService().review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Accepted for assessment.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=5),
    )


def assess(path, preview):
    return HistoricalComparisonEvidenceAssessmentLedger(path).record(
        preview,
        category="Company filing",
        direction="Supporting",
        strength=84.0,
        confidence=79.0,
        independent_confirmation=2,
        is_primary_source=True,
        is_time_sensitive=False,
        assessor="Human Assessor",
        rationale="Explicit assessment for conversion preview only.",
        assessed_at=preview.reviewed_at + timedelta(minutes=5),
    )


def validate_builder(root, preview) -> None:
    assessment = assess(root / "builder-assessment.jsonl", preview)
    builder = HistoricalComparisonEvidenceConversionPreviewBuilder()
    eligibility = builder.build([preview], [assessment])
    assert eligibility.accepted_count == 1
    assert eligibility.eligible_count == 1
    assert eligibility.missing_assessment_candidate_ids == ()
    projected = eligibility.eligible_previews[0]
    assert projected.proposed_evidence_id == f"HC-{preview.candidate_id}"
    assert projected.statement == preview.description
    assert projected.source == preview.source
    assert projected.direction == "Supporting"
    assert projected.strength == 84.0
    assert projected.notes == assessment.rationale

    missing = builder.build([preview], [])
    assert missing.eligible_count == 0
    assert missing.missing_assessment_candidate_ids == (preview.candidate_id,)

    invalid_cases = (
        ([preview, preview], [assessment], "unique"),
        ([preview], [replace(assessment, candidate_id="0" * 64)], "unknown"),
        (
            [preview],
            [replace(assessment, observation_fingerprint="0" * 64)],
            "fingerprint",
        ),
        ([preview], [assessment, assessment], "multiple"),
    )
    for previews, assessments, expected in invalid_cases:
        try:
            builder.build(previews, assessments)
            raise AssertionError(f"Invalid conversion preview: {expected}")
        except ValueError as exc:
            assert expected in str(exc).casefold()


def validate_command(root, audit_path, candidate, observation) -> None:
    review_path = root / "reviews.jsonl"
    observation_path = root / "observations.json"
    assessment_path = root / "assessments.jsonl"
    accepted = accept(candidate)
    HistoricalComparisonReviewDecisionLedger(review_path).record(accepted)
    ObservationPersistence(observation_path).save([observation])
    resolved = HistoricalComparisonAcceptedObservationResolver().resolve(
        accepted, [observation]
    )
    assess(assessment_path, resolved)
    paths = (audit_path, review_path, observation_path, assessment_path)
    before = {path: path.read_bytes() for path in paths}

    output = io.StringIO()
    with redirect_stdout(output):
        result = preview_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(assessment_path),
                "--json",
            ]
        )
    assert result == 0
    payload = json.loads(output.getvalue())
    assert payload["review_candidate_count"] == 1
    assert payload["accepted_count"] == 1
    assert payload["eligible_count"] == 1
    assert payload["missing_assessment_candidate_ids"] == []
    projected = payload["conversion_previews"][0]
    assert projected["proposed_evidence_id"] == f"HC-{candidate.candidate_id}"
    assert projected["would_be_evidence_fields"]["direction"] == "Supporting"
    assert projected["lineage"]["assessor"] == "Human Assessor"
    assert payload["source_files_modified"] is False
    assert payload["evidence_created"] is False
    assert payload["financial_interpretation_performed"] is False
    for path, content in before.items():
        assert path.read_bytes() == content

    error_output = io.StringIO()
    with redirect_stdout(error_output):
        error = preview_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(audit_path),
            ]
        )
    assert error == 1
    assert "must differ" in error_output.getvalue()


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        observation = make_observation(candidate)
        accepted = accept(candidate)
        preview = HistoricalComparisonAcceptedObservationResolver().resolve(
            accepted, [observation]
        )
        validate_builder(root, preview)
        validate_command(root, audit_path, candidate, observation)
    print("HISTORICAL EVIDENCE CONVERSION PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
