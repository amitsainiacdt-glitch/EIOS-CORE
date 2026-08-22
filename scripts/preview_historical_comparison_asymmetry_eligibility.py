"""Preview governed Asymmetry eligibility without invoking its engine."""

import json

from modules.external_intelligence.historical_comparison_asymmetry_eligibility_preview_builder import HistoricalComparisonAsymmetryEligibilityPreviewBuilder
from scripts.preview_historical_comparison_opportunity_eligibility import build_opportunity_eligibility_from_args, parser as opportunity_parser


def parser():
    result = opportunity_parser()
    result.description = "Preview governed eligibility for later Asymmetry analysis."
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        _, before, context = build_opportunity_eligibility_from_args(args)
        preview = HistoricalComparisonAsymmetryEligibilityPreviewBuilder().build(
            context["inputs"], context["reviews"], context["catalyst_assessment"],
            context["catalyst_creation"], context["gap_assessment"], context["gap_creation"],
            context["valuation"], context["valuation_receipt"],
            context["mispricing_assessment"], context["mispricing_creation"],
            cmp=args.cmp, mispricing_assumptions=args.mispricing_assumption,
            mispricing_invalidation_conditions=args.mispricing_invalidation_condition,
            **context["analysis_kwargs"],
        )
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Asymmetry eligibility error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Asymmetry eligibility error: a source file changed.")
        return 1
    payload = {key: list(value) if isinstance(value, tuple) else value for key, value in preview.__dict__.items()}
    print(json.dumps(payload, sort_keys=True, indent=2))
    print("Read-only eligibility preview: Asymmetry analysis was not invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
