"""No-network validation for the human Evidence assessment ledger."""

import io
import json
from contextlib import redirect_stdout
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
from scripts.record_historical_comparison_evidence_assessment import (
    main as record_main,
)


def accept(candidate):
    return HistoricalComparisonReviewService().review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Accepted for explicit human assessment.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=5),
    )


def record(ledger, preview, **overrides):
    values = {
        "category": "Company filing",
        "direction": "Supporting",
        "strength": 82.0,
        "confidence": 78.0,
        "independent_confirmation": 2,
        "is_primary_source": True,
        "is_time_sensitive": False,
        "assessor": "Human Assessor",
        "rationale": "Explicit assessment; no Evidence conversion.",
        "assessed_at": preview.reviewed_at + timedelta(minutes=5),
    }
    values.update(overrides)
    return ledger.record(preview, **values)


def validate_ledger(root, candidate, observation) -> None:
    preview = HistoricalComparisonAcceptedObservationResolver().resolve(
        accept(candidate), [observation]
    )
    path = root / "direct-assessments.jsonl"
    ledger = HistoricalComparisonEvidenceAssessmentLedger(path)
    assessment = record(ledger, preview)
    assert assessment.candidate_id == candidate.candidate_id
    assert assessment.observation_fingerprint == (
        candidate.current_observation.content_fingerprint
    )
    assert assessment.direction == "Supporting"
    assert ledger.read_all() == (assessment,)
    before = path.read_bytes()

    try:
        record(ledger, preview, direction="Contradictory")
        raise AssertionError("Duplicate assessment was persisted")
    except ValueError as exc:
        assert "already exists" in str(exc).casefold()
    assert path.read_bytes() == before

    invalid_cases = (
        ({"strength": 101.0}, "strength"),
        ({"confidence": float("nan")}, "confidence"),
        ({"independent_confirmation": -1}, "independent"),
        ({"is_primary_source": 1}, "boolean"),
        ({"direction": "Unknown"}, "direction"),
        (
            {"assessed_at": preview.reviewed_at - timedelta(seconds=1)},
            "precedes",
        ),
    )
    for index, (overrides, expected) in enumerate(invalid_cases):
        invalid_ledger = HistoricalComparisonEvidenceAssessmentLedger(
            root / f"invalid-{index}.jsonl"
        )
        try:
            record(invalid_ledger, preview, **overrides)
            raise AssertionError(f"Invalid assessment accepted: {expected}")
        except ValueError as exc:
            assert expected in str(exc).casefold()
        assert not invalid_ledger.path.exists()

    malformed = root / "malformed.jsonl"
    malformed.write_text(json.dumps({"schema_version": 2}) + "\n", encoding="utf-8")
    try:
        HistoricalComparisonEvidenceAssessmentLedger(malformed).read_all()
        raise AssertionError("Unsupported assessment schema was read")
    except ValueError as exc:
        assert "line 1" in str(exc).casefold()


def validate_command(root, audit_path, candidate, observation) -> None:
    review_path = root / "review-decisions.jsonl"
    observation_path = root / "observations.json"
    assessment_path = root / "assessment-decisions.jsonl"
    accepted = accept(candidate)
    HistoricalComparisonReviewDecisionLedger(review_path).record(accepted)
    ObservationPersistence(observation_path).save([observation])
    source_before = {
        path: path.read_bytes()
        for path in (audit_path, review_path, observation_path)
    }
    assessed_at = accepted.reviewed_at + timedelta(minutes=5)

    output = io.StringIO()
    with redirect_stdout(output):
        result = record_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(assessment_path),
                "--candidate-id", candidate.candidate_id,
                "--category", "Company filing",
                "--direction", "Supporting",
                "--strength", "82",
                "--confidence", "78",
                "--independent-confirmation", "2",
                "--primary-source",
                "--no-time-sensitive",
                "--assessor", "Human Assessor",
                "--rationale", "Explicit human assessment only.",
                "--assessed-at", assessed_at.isoformat(),
            ]
        )
    assert result == 0
    assert "No Evidence was created." in output.getvalue()
    stored = HistoricalComparisonEvidenceAssessmentLedger(
        assessment_path
    ).read_all()
    assert len(stored) == 1
    assert stored[0].is_primary_source is True
    assert stored[0].is_time_sensitive is False
    assert stored[0].assessor == "Human Assessor"
    for path, content in source_before.items():
        assert path.read_bytes() == content

    assessment_before = assessment_path.read_bytes()
    duplicate_output = io.StringIO()
    with redirect_stdout(duplicate_output):
        duplicate = record_main(
            [
                "--audit-path", str(audit_path),
                "--review-ledger-path", str(review_path),
                "--observation-path", str(observation_path),
                "--assessment-ledger-path", str(assessment_path),
                "--candidate-id", candidate.candidate_id,
                "--category", "Company filing",
                "--direction", "Contradictory",
                "--strength", "20",
                "--confidence", "30",
                "--independent-confirmation", "0",
                "--no-primary-source",
                "--time-sensitive",
                "--assessor", "Second Assessor",
                "--rationale", "Conflicting second assessment.",
                "--assessed-at", assessed_at.isoformat(),
            ]
        )
    assert duplicate == 1
    assert assessment_path.read_bytes() == assessment_before


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        observation = make_observation(candidate)
        validate_ledger(root, candidate, observation)
        validate_command(root, audit_path, candidate, observation)
    print("HISTORICAL EVIDENCE ASSESSMENT LEDGER: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
