"""Explicitly materialize one approved governed Expectation Gap."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_expectation_gap_assessment_ledger import HistoricalComparisonExpectationGapAssessmentLedger
from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from scripts.preview_historical_comparison_expectation_gap_analysis import build_preview_from_args, parser as analysis_parser


def parser():
    result = analysis_parser()
    result.description = "Explicitly materialize one approved governed Expectation Gap."
    for name in ("gap-assessment-ledger-path", "creation-ledger-path", "creator", "rationale", "created-at"):
        result.add_argument("--" + name, required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    destination, assessment_path = Path(args.creation_ledger_path), Path(args.gap_assessment_ledger_path)
    try:
        preview, before, context = build_preview_from_args(args, include_context=True)
        source_paths = set(before) | {assessment_path}
        if destination.resolve() in {path.resolve() for path in source_paths}:
            raise ValueError("creation ledger must be distinct from every source ledger")
        if assessment_path.is_file():
            before[assessment_path] = assessment_path.read_bytes()
        matches = [item for item in HistoricalComparisonExpectationGapAssessmentLedger(assessment_path).read_all() if item.analysis_fingerprint == preview.analysis_fingerprint]
        if len(matches) != 1:
            raise ValueError("approved Expectation Gap assessment was not found uniquely")
        gap, receipt = HistoricalComparisonExpectationGapCreationLedger(destination).materialize(
            context["inputs"], context["reviews"], context["catalyst_assessment"],
            context["catalyst_creation"], matches[0], **context["analysis_kwargs"],
            creator=args.creator, rationale=args.rationale, created_at=datetime.fromisoformat(args.created_at),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Expectation Gap materialization error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Expectation Gap materialization error: a source ledger changed.")
        return 1
    print(f"Expectation Gap: {gap.gap_id}")
    print(f"Score: {gap.gap_score:.2f}")
    print(f"Expectation Gap fingerprint: {receipt.expectation_gap_fingerprint}")
    print("Creation receipt appended. No downstream engine or investment action was invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
