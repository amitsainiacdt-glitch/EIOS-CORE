"""No-network validation for accepted-review observation resolution."""

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
from modules.observation.observation import Observation, ObservationProvenance
from modules.observation.observation_persistence import ObservationPersistence
from scripts.preview_historical_comparison_accepted_observations import (
    main as preview_main,
)


def make_observation(candidate) -> Observation:
    reference = candidate.current_observation
    return Observation(
        title=reference.title,
        description=reference.title,
        source=reference.source,
        category=reference.category,
        entity=reference.entity,
        confidence=82.0,
        timestamp=reference.timestamp,
        provenance=ObservationProvenance(
            cycle_id="cycle-preview-test",
            job_id=reference.job_id,
            research_intent=reference.research_intent,
            retrieved_at=reference.timestamp,
            source_url=reference.source,
            source_domain="research.example.com",
            source_type="text/html",
            content_fingerprint=reference.content_fingerprint,
        ),
    )


def accept(candidate):
    return HistoricalComparisonReviewService().review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Approved for assessment preview only.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=5),
    )


def validate_resolver(candidate, observation) -> None:
    resolver = HistoricalComparisonAcceptedObservationResolver()
    accepted = accept(candidate)
    preview = resolver.resolve(accepted, [observation])
    assert preview.candidate_id == candidate.candidate_id
    assert preview.title == observation.title
    assert preview.description == observation.description
    assert preview.content_fingerprint == (
        observation.provenance.content_fingerprint
    )
    assert preview.reviewer == "Human Reviewer"

    cases = (
        (candidate, [observation], "ACCEPTED"),
        (accepted, [], "missing"),
        (accepted, [observation, observation], "ambiguous"),
        (
            accepted,
            [replace(observation, title="Mismatched title")],
            "mismatch",
        ),
    )
    for test_candidate, observations, expected in cases:
        try:
            resolver.resolve(test_candidate, observations)
            raise AssertionError(f"Invalid resolution accepted: {expected}")
        except ValueError as exc:
            assert expected.casefold() in str(exc).casefold()


def validate_command(root, audit_path, candidate, observation) -> None:
    ledger_path = root / "decisions.jsonl"
    observation_path = root / "observations.json"
    HistoricalComparisonReviewDecisionLedger(ledger_path).record(
        accept(candidate)
    )
    ObservationPersistence(observation_path).save([observation])
    before = {
        path: path.read_bytes()
        for path in (audit_path, ledger_path, observation_path)
    }

    output = io.StringIO()
    with redirect_stdout(output):
        result = preview_main(
            [
                "--audit-path",
                str(audit_path),
                "--ledger-path",
                str(ledger_path),
                "--observation-path",
                str(observation_path),
                "--json",
            ]
        )
    assert result == 0
    payload = json.loads(output.getvalue())
    assert payload["candidate_count"] == 1
    assert payload["accepted_count"] == 1
    assert payload["resolved_count"] == 1
    assert payload["assessment_required"] is True
    assert payload["previews"][0]["evidence_assessment_supplied"] is False
    assert payload["previews"][0]["observation"]["title"] == observation.title
    assert payload["source_files_modified"] is False
    assert payload["evidence_created"] is False
    assert payload["financial_interpretation_performed"] is False
    for path, content in before.items():
        assert path.read_bytes() == content

    error_output = io.StringIO()
    with redirect_stdout(error_output):
        error = preview_main(
            [
                "--audit-path",
                str(audit_path),
                "--ledger-path",
                str(audit_path),
                "--observation-path",
                str(observation_path),
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
        validate_resolver(candidate, observation)
        validate_command(root, audit_path, candidate, observation)
    print("ACCEPTED-REVIEW OBSERVATION PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
