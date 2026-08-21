"""Explicitly score one verified entity EvidenceItem pack."""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_accepted_observation_resolver import HistoricalComparisonAcceptedObservationResolver
from modules.external_intelligence.historical_comparison_audit_reader import HistoricalComparisonAuditReader
from modules.external_intelligence.historical_comparison_evidence_assessment_ledger import HistoricalComparisonEvidenceAssessmentLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.historical_comparison_evidence_receipt_reconciler import HistoricalComparisonEvidenceReceiptReconciler
from modules.external_intelligence.historical_comparison_review_candidate import HistoricalComparisonReviewStatus
from modules.external_intelligence.historical_comparison_review_candidate_builder import HistoricalComparisonReviewCandidateBuilder
from modules.external_intelligence.historical_comparison_review_decision_ledger import HistoricalComparisonReviewDecisionLedger
from modules.external_intelligence.historical_comparison_review_reconciler import HistoricalComparisonReviewReconciler
from modules.observation.observation_persistence import ObservationPersistence


def build_parser():
    parser = argparse.ArgumentParser(
        description="Explicitly score one verified entity EvidenceItem pack."
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--review-ledger-path")
    parser.add_argument("--observation-path")
    parser.add_argument("--assessment-ledger-path")
    parser.add_argument("--conversion-receipt-path")
    parser.add_argument("--scoring-receipt-path")
    parser.add_argument("--entity", required=True)
    parser.add_argument("--analyst", required=True)
    parser.add_argument("--analyzed-at", required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    values = {
        "audit": args.audit_path or os.environ.get("EIOS_HISTORICAL_COMPARISON_AUDIT_PATH", "").strip(),
        "review": args.review_ledger_path or os.environ.get("EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH", "").strip(),
        "observation": args.observation_path or os.environ.get("EIOS_OBSERVATION_PATH", "").strip(),
        "assessment": args.assessment_ledger_path or os.environ.get("EIOS_HISTORICAL_COMPARISON_EVIDENCE_ASSESSMENT_LEDGER_PATH", "").strip(),
        "conversion": args.conversion_receipt_path or os.environ.get("EIOS_HISTORICAL_COMPARISON_EVIDENCE_CONVERSION_RECEIPT_PATH", "").strip(),
        "scoring": args.scoring_receipt_path or os.environ.get("EIOS_HISTORICAL_COMPARISON_EVIDENCE_SCORING_RECEIPT_PATH", "").strip(),
    }
    if any(not value for value in values.values()):
        print("Configuration error: all six paths are required.")
        return 1
    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 6:
        print("Evidence pack scoring error: all configured paths must differ.")
        return 1
    source_names = ("audit", "review", "observation", "assessment", "conversion")
    before = {
        name: paths[name].read_bytes() if paths[name].is_file() else None
        for name in source_names
    }
    try:
        analyzed_at = datetime.fromisoformat(args.analyzed_at)
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(paths["audit"]).read_all()
        )
        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            candidates,
            HistoricalComparisonReviewDecisionLedger(paths["review"]).read_all(),
        )
        accepted = tuple(
            item for item in reconciled
            if item.status == HistoricalComparisonReviewStatus.ACCEPTED
        )
        observations = ObservationPersistence(paths["observation"]).load()
        resolver = HistoricalComparisonAcceptedObservationResolver()
        previews = tuple(
            resolver.resolve(candidate, observations) for candidate in accepted
        )
        packs = HistoricalComparisonEvidenceReceiptReconciler().reconcile(
            previews,
            HistoricalComparisonEvidenceAssessmentLedger(paths["assessment"]).read_all(),
            HistoricalComparisonEvidenceConversionReceiptLedger(paths["conversion"]).read_all(),
        ).entity_packs
        matches = [pack for pack in packs if pack.entity == args.entity]
        if len(matches) != 1:
            raise ValueError("entity was not found uniquely")
        result, receipt = HistoricalComparisonEvidencePackScoringLedger(
            paths["scoring"]
        ).analyze(
            matches[0], analyst=args.analyst, analyzed_at=analyzed_at
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Evidence pack scoring error: {exc}")
        return 1
    for name in source_names:
        path = paths[name]
        if before[name] is not None and path.read_bytes() != before[name]:
            print(f"Evidence pack scoring error: {name} source file changed.")
            return 1
    print(f"Entity: {receipt.entity}")
    print(f"Pack fingerprint: {receipt.pack_fingerprint}")
    print(f"Evidence score: {result.evidence_score}")
    print(f"Confidence: {result.confidence}")
    print(f"Sufficiently supported: {result.sufficiently_supported}")
    print("Scoring receipt appended.")
    print("No Intelligence was published.")
    print("No Signal or Catalyst was created.")
    print("No valuation or investment decision was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
