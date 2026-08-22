"""Explicitly materialize one approved governed Mispricing result."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_mispricing_assessment_ledger import HistoricalComparisonMispricingAssessmentLedger
from modules.external_intelligence.historical_comparison_mispricing_creation_ledger import HistoricalComparisonMispricingCreationLedger
from scripts.preview_historical_comparison_mispricing_analysis import build_mispricing_preview_from_args, parser as analysis_parser


def parser():
    result = analysis_parser()
    result.description = "Explicitly materialize one approved governed Mispricing result."
    for name in ("mispricing-assessment-ledger-path", "creation-ledger-path", "creator", "rationale", "created-at"):
        result.add_argument("--" + name, required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    destination = Path(args.creation_ledger_path)
    assessment_path = Path(args.mispricing_assessment_ledger_path)
    try:
        preview, before, context = build_mispricing_preview_from_args(args, include_context=True)
        source_paths = set(before) | {assessment_path}
        if destination.resolve() in {path.resolve() for path in source_paths}:
            raise ValueError("creation ledger must be distinct from every source file")
        if assessment_path.is_file():
            before[assessment_path] = assessment_path.read_bytes()
        matches = [
            item for item in HistoricalComparisonMispricingAssessmentLedger(assessment_path).read_all()
            if item.analysis_fingerprint == preview.analysis_fingerprint
        ]
        if len(matches) != 1:
            raise ValueError("approved Mispricing assessment was not found uniquely")
        result, receipt = HistoricalComparisonMispricingCreationLedger(destination).materialize(
            context["inputs"], context["reviews"], context["catalyst_assessment"],
            context["catalyst_creation"], context["gap_assessment"], context["gap_creation"],
            context["valuation"], context["valuation_receipt"], matches[0], cmp=args.cmp,
            mispricing_assumptions=args.mispricing_assumption,
            mispricing_invalidation_conditions=args.mispricing_invalidation_condition,
            creator=args.creator, rationale=args.rationale,
            created_at=datetime.fromisoformat(args.created_at), **context["analysis_kwargs"],
        )
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Mispricing materialization error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Mispricing materialization error: a source file changed.")
        return 1
    print(f"Company: {result.company}")
    print(f"Score: {result.mispricing_score:.2f}")
    print(f"Mispricing fingerprint: {receipt.mispricing_fingerprint}")
    print("Creation receipt appended. No Opportunity, valuation, portfolio, or investment action was invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
