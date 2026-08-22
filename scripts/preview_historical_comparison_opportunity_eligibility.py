"""Preview governed Opportunity-synthesis eligibility without invoking it."""

import json
from pathlib import Path

from modules.external_intelligence.historical_comparison_mispricing_assessment_ledger import HistoricalComparisonMispricingAssessmentLedger
from modules.external_intelligence.historical_comparison_mispricing_creation_ledger import HistoricalComparisonMispricingCreationLedger
from modules.external_intelligence.historical_comparison_opportunity_eligibility_preview_builder import HistoricalComparisonOpportunityEligibilityPreviewBuilder
from scripts.preview_historical_comparison_mispricing_analysis import build_mispricing_preview_from_args, parser as analysis_parser


def parser():
    result = analysis_parser()
    result.description = "Preview governed eligibility for later Opportunity synthesis."
    result.add_argument("--mispricing-assessment-ledger-path", required=True)
    result.add_argument("--mispricing-creation-ledger-path", required=True)
    return result


def one(items, predicate, name):
    matches = [item for item in items if predicate(item)]
    if len(matches) != 1:
        raise ValueError(f"{name} was not found uniquely")
    return matches[0]


def main(argv=None):
    args = parser().parse_args(argv)
    assessment_path = Path(args.mispricing_assessment_ledger_path)
    creation_path = Path(args.mispricing_creation_ledger_path)
    try:
        analysis, before, context = build_mispricing_preview_from_args(args, include_context=True)
        for path in (assessment_path, creation_path):
            if path.is_file():
                before[path] = path.read_bytes()
        assessment = one(
            HistoricalComparisonMispricingAssessmentLedger(assessment_path).read_all(),
            lambda item: item.analysis_fingerprint == analysis.analysis_fingerprint,
            "Mispricing assessment",
        )
        assessment_fingerprint = HistoricalComparisonMispricingCreationLedger.assessment_fingerprint(assessment)
        creation = one(
            HistoricalComparisonMispricingCreationLedger(creation_path).read_all(),
            lambda item: item.assessment_fingerprint == assessment_fingerprint,
            "Mispricing creation receipt",
        )
        preview = HistoricalComparisonOpportunityEligibilityPreviewBuilder().build(
            context["inputs"], context["reviews"], context["catalyst_assessment"],
            context["catalyst_creation"], context["gap_assessment"], context["gap_creation"],
            context["valuation"], context["valuation_receipt"], assessment, creation,
            cmp=args.cmp, mispricing_assumptions=args.mispricing_assumption,
            mispricing_invalidation_conditions=args.mispricing_invalidation_condition,
            **context["analysis_kwargs"],
        )
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Opportunity eligibility error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Opportunity eligibility error: a source file changed.")
        return 1
    payload = {key: list(value) if isinstance(value, tuple) else value for key, value in preview.__dict__.items()}
    print(json.dumps(payload, sort_keys=True, indent=2))
    print("Read-only eligibility preview: Opportunity synthesis was not invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
