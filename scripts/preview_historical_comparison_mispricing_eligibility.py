"""Preview governed Mispricing eligibility without invoking its engine."""

import json
from pathlib import Path

from modules.external_intelligence.historical_comparison_expectation_gap_assessment_ledger import HistoricalComparisonExpectationGapAssessmentLedger
from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_eligibility_preview_builder import HistoricalComparisonMispricingEligibilityPreviewBuilder
from scripts.preview_historical_comparison_expectation_gap_analysis import build_preview_from_args, parser as analysis_parser


def parser():
    result = analysis_parser()
    result.description = "Preview governed eligibility for later Mispricing analysis."
    result.add_argument("--gap-assessment-ledger-path", required=True)
    result.add_argument("--gap-creation-ledger-path", required=True)
    return result


def one(items, predicate, name):
    matches = [item for item in items if predicate(item)]
    if len(matches) != 1:
        raise ValueError(f"{name} was not found uniquely")
    return matches[0]


def main(argv=None):
    args = parser().parse_args(argv)
    assessment_path, creation_path = Path(args.gap_assessment_ledger_path), Path(args.gap_creation_ledger_path)
    try:
        analysis, before, context = build_preview_from_args(args, include_context=True)
        for path in (assessment_path, creation_path):
            if path.is_file(): before[path] = path.read_bytes()
        assessment = one(HistoricalComparisonExpectationGapAssessmentLedger(assessment_path).read_all(), lambda item: item.analysis_fingerprint == analysis.analysis_fingerprint, "Expectation Gap assessment")
        assessment_fingerprint = HistoricalComparisonExpectationGapCreationLedger.assessment_fingerprint(assessment)
        creation = one(HistoricalComparisonExpectationGapCreationLedger(creation_path).read_all(), lambda item: item.assessment_fingerprint == assessment_fingerprint, "Expectation Gap creation receipt")
        preview = HistoricalComparisonMispricingEligibilityPreviewBuilder().build(
            context["inputs"], context["reviews"], context["catalyst_assessment"],
            context["catalyst_creation"], assessment, creation, **context["analysis_kwargs"],
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Mispricing eligibility error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Mispricing eligibility error: a source ledger changed.")
        return 1
    payload = {key: list(value) if isinstance(value, tuple) else value for key, value in preview.__dict__.items()}
    print(json.dumps(payload, sort_keys=True, indent=2))
    print("Read-only eligibility preview: Mispricing analysis was not invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
