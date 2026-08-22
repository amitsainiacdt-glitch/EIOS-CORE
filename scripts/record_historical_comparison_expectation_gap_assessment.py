"""Record a human decision on one exact governed Expectation Gap analysis."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_expectation_gap_assessment_ledger import HistoricalComparisonExpectationGapAssessmentLedger
from scripts.preview_historical_comparison_expectation_gap_analysis import build_preview_from_args, parser as analysis_parser


def parser():
    result = analysis_parser()
    result.description = "Record a human assessment of an exact governed Expectation Gap analysis."
    for name in ("decision-ledger-path", "disposition", "reviewer", "rationale", "reviewed-at"):
        result.add_argument("--" + name, required=True)
    result.add_argument("--condition", action="append", default=[])
    result.add_argument("--monitoring-requirement", action="append", default=[])
    return result


def source_paths(args):
    paths = [
        Path(args.stage_review_ledger_path), Path(args.assessment_ledger_path),
        Path(args.catalyst_creation_ledger_path),
    ]
    for raw in args.signal_chain_json:
        spec = json.loads(raw)
        paths.extend(Path(spec[key]) for key in ("creation_path", "interpretation_path", "conversion_path", "validation_decision_path"))
    return paths


def main(argv=None):
    args = parser().parse_args(argv)
    destination = Path(args.decision_ledger_path)
    try:
        sources = source_paths(args)
        if destination.resolve() in {path.resolve() for path in sources}:
            raise ValueError("decision ledger must be distinct from every source ledger")
        preview, before = build_preview_from_args(args)
        decision = HistoricalComparisonExpectationGapAssessmentLedger(destination).record(
            preview, disposition=args.disposition, conditions=args.condition,
            monitoring_requirements=args.monitoring_requirement, reviewer=args.reviewer,
            rationale=args.rationale, reviewed_at=datetime.fromisoformat(args.reviewed_at),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Expectation Gap assessment error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Expectation Gap assessment error: a source ledger changed.")
        return 1
    print(f"Expectation Gap: {decision.gap_id}")
    print(f"Decision: {decision.disposition.value}")
    print(f"Analysis fingerprint: {decision.analysis_fingerprint}")
    print("Decision appended. No downstream analysis or investment action was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
