"""Run one governed Expectation Gap analysis without persistence."""

import argparse
import json
from pathlib import Path

from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview_builder import HistoricalComparisonExpectationGapAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput, HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger


def parser():
    result = argparse.ArgumentParser(description="Run governed read-only Expectation Gap analysis.")
    result.add_argument("--signal-chain-json", action="append", required=True)
    for name in (
        "stage-review-ledger-path", "assessment-ledger-path", "catalyst-creation-ledger-path",
        "theme", "cluster-id", "catalyst-id", "trigger", "description", "economic-impact",
        "earnings-impact", "valuation-impact", "gap-id", "company", "sector",
    ):
        result.add_argument("--" + name, required=True)
    for name in ("market-expectation", "eios-expectation", "market-earnings-expectation", "eios-earnings-expectation"):
        result.add_argument("--" + name, required=True, type=float)
    result.add_argument("--assumption", action="append", default=[])
    result.add_argument("--invalidation-condition", action="append", default=[])
    return result


def one(items, predicate, name):
    matches = [item for item in items if predicate(item)]
    if len(matches) != 1:
        raise ValueError(f"{name} was not found uniquely")
    return matches[0]


def main(argv=None):
    args = parser().parse_args(argv)
    paths, chains = [], []
    review_path = Path(args.stage_review_ledger_path)
    assessment_path = Path(args.assessment_ledger_path)
    creation_path = Path(args.catalyst_creation_ledger_path)
    try:
        for raw in args.signal_chain_json:
            spec = json.loads(raw)
            signal_id = spec["signal_id"]
            current = [Path(spec[key]) for key in ("creation_path", "interpretation_path", "conversion_path", "validation_decision_path")]
            paths.extend(current)
            signal_creation = one(HistoricalComparisonSignalCreationLedger(current[0]).read_all(), lambda item: item.signal_id == signal_id, "Signal creation")
            interpretation = one(HistoricalComparisonSignalInterpretationLedger(current[1]).read_all(), lambda item: (item.governed_input_fingerprint, item.evidence_id) == (signal_creation.governed_input_fingerprint, signal_creation.evidence_id), "Signal interpretation")
            conversion = one(HistoricalComparisonEvidenceConversionReceiptLedger(current[2]).read_all(), lambda item: item.evidence_id == signal_creation.evidence_id, "Evidence conversion")
            decision = one(HistoricalComparisonSignalValidationDecisionLedger(current[3]).read_all(), lambda item: item.signal_id == signal_id, "Signal validation decision")
            chains.append(HistoricalComparisonApprovedSignalInput(signal_creation, interpretation, conversion, decision))
        sources = paths + [review_path, assessment_path, creation_path]
        before = {path: path.read_bytes() for path in sources if path.is_file()}
        catalyst_kwargs = dict(theme=args.theme, cluster_id=args.cluster_id, catalyst_id=args.catalyst_id, trigger=args.trigger, description=args.description, economic_impact=args.economic_impact, earnings_impact=args.earnings_impact, valuation_impact=args.valuation_impact)
        baseline = HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(chains, **catalyst_kwargs)
        reviews = [item for item in HistoricalComparisonSignalStageReviewLedger(review_path).read_all() if item.support_fingerprint == baseline.support_fingerprint]
        promoted = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(chains, reviews, **catalyst_kwargs)
        preview_fingerprint = HistoricalComparisonPromotedCatalystAssessmentLedger.preview_fingerprint(promoted)
        assessment = one(HistoricalComparisonPromotedCatalystAssessmentLedger(assessment_path).read_all(), lambda item: item.preview_fingerprint == preview_fingerprint, "promoted Catalyst assessment")
        assessment_fingerprint = HistoricalComparisonCatalystCreationLedger._assessment_fingerprint(assessment)
        creation = one(HistoricalComparisonCatalystCreationLedger(creation_path).read_all(), lambda item: item.assessment_fingerprint == assessment_fingerprint, "Catalyst creation receipt")
        preview = HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(
            chains, reviews, assessment, creation, **catalyst_kwargs,
            gap_id=args.gap_id, company=args.company, sector=args.sector,
            market_expectation=args.market_expectation, eios_expectation=args.eios_expectation,
            market_earnings_expectation=args.market_earnings_expectation,
            eios_earnings_expectation=args.eios_earnings_expectation,
            assumptions=args.assumption, invalidation_conditions=args.invalidation_condition,
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Expectation Gap analysis error: {exc}")
        return 1
    if any(path.read_bytes() != value for path, value in before.items()):
        print("Expectation Gap analysis error: a source ledger changed.")
        return 1
    payload = {key: list(value) if isinstance(value, tuple) else value for key, value in preview.__dict__.items()}
    print(json.dumps(payload, sort_keys=True, indent=2))
    print("Read-only analysis preview: no receipt was appended and no downstream engine was invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
