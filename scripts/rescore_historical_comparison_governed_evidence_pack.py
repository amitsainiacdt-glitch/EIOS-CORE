"""Explicitly rescore one exact governed entity Evidence pack."""

import argparse
import os
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_accepted_observation_resolver import HistoricalComparisonAcceptedObservationResolver
from modules.external_intelligence.historical_comparison_audit_reader import HistoricalComparisonAuditReader
from modules.external_intelligence.historical_comparison_evidence_assessment_ledger import HistoricalComparisonEvidenceAssessmentLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_evidence_governance_ledger import HistoricalComparisonEvidenceGovernanceLedger
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.historical_comparison_evidence_receipt_reconciler import HistoricalComparisonEvidenceReceiptReconciler
from modules.external_intelligence.historical_comparison_governed_scoring_ledger import HistoricalComparisonGovernedScoringLedger
from modules.external_intelligence.historical_comparison_review_candidate import HistoricalComparisonReviewStatus
from modules.external_intelligence.historical_comparison_review_candidate_builder import HistoricalComparisonReviewCandidateBuilder
from modules.external_intelligence.historical_comparison_review_decision_ledger import HistoricalComparisonReviewDecisionLedger
from modules.external_intelligence.historical_comparison_review_reconciler import HistoricalComparisonReviewReconciler
from modules.observation.observation_persistence import ObservationPersistence


ENV = {
    "audit": "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH",
    "review": "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH",
    "observation": "EIOS_OBSERVATION_PATH",
    "assessment": "EIOS_HISTORICAL_COMPARISON_EVIDENCE_ASSESSMENT_LEDGER_PATH",
    "conversion": "EIOS_HISTORICAL_COMPARISON_EVIDENCE_CONVERSION_RECEIPT_PATH",
    "scoring": "EIOS_HISTORICAL_COMPARISON_EVIDENCE_SCORING_RECEIPT_PATH",
    "governance": "EIOS_HISTORICAL_COMPARISON_EVIDENCE_GOVERNANCE_LEDGER_PATH",
    "governed": "EIOS_HISTORICAL_COMPARISON_GOVERNED_SCORING_RECEIPT_PATH",
}


def build_parser():
    parser = argparse.ArgumentParser(description="Rescore one exact governed Evidence pack.")
    for name in ENV:
        parser.add_argument(f"--{name}-path")
    parser.add_argument("--pack-fingerprint", required=True)
    parser.add_argument("--analyst", required=True)
    parser.add_argument("--rescored-at", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    values = {
        name: getattr(args, f"{name}_path") or os.environ.get(env, "").strip()
        for name, env in ENV.items()
    }
    if any(not value for value in values.values()):
        print("Configuration error: all eight paths are required.")
        return 1
    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 8:
        print("Governed rescoring error: all configured paths must differ.")
        return 1
    source_names = tuple(name for name in paths if name != "governed")
    before = {name: paths[name].read_bytes() if paths[name].is_file() else None for name in source_names}
    try:
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(paths["audit"]).read_all()
        )
        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            candidates, HistoricalComparisonReviewDecisionLedger(paths["review"]).read_all()
        )
        accepted = tuple(item for item in reconciled if item.status == HistoricalComparisonReviewStatus.ACCEPTED)
        observations = ObservationPersistence(paths["observation"]).load()
        resolver = HistoricalComparisonAcceptedObservationResolver()
        previews = tuple(resolver.resolve(item, observations) for item in accepted)
        packs = HistoricalComparisonEvidenceReceiptReconciler().reconcile(
            previews,
            HistoricalComparisonEvidenceAssessmentLedger(paths["assessment"]).read_all(),
            HistoricalComparisonEvidenceConversionReceiptLedger(paths["conversion"]).read_all(),
        ).entity_packs
        fingerprint = args.pack_fingerprint.casefold()
        scores = [item for item in HistoricalComparisonEvidencePackScoringLedger(paths["scoring"]).read_all() if item.pack_fingerprint == fingerprint]
        governance = [item for item in HistoricalComparisonEvidenceGovernanceLedger(paths["governance"]).read_all() if item.pack_fingerprint == fingerprint]
        pack_matches = [item for item in packs if HistoricalComparisonEvidencePackScoringLedger.pack_fingerprint(item) == fingerprint]
        if len(scores) != 1 or len(governance) != 1 or len(pack_matches) != 1:
            raise ValueError("scored pack and governance were not found uniquely")
        result, receipt = HistoricalComparisonGovernedScoringLedger(paths["governed"]).analyze(
            pack_matches[0], governance[0], analyst=args.analyst,
            rescored_at=datetime.fromisoformat(args.rescored_at),
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Governed rescoring error: {exc}")
        return 1
    for name in source_names:
        if before[name] is not None and paths[name].read_bytes() != before[name]:
            print(f"Governed rescoring error: {name} source changed.")
            return 1
    print(f"Entity: {receipt.entity}")
    print(f"Evidence score: {result.evidence_score}")
    print(f"Confidence: {result.confidence}")
    print(f"Sufficiently supported: {result.sufficiently_supported}")
    print(f"Remaining evidence gaps: {len(result.evidence_gaps)}")
    print("Governed scoring receipt appended.")
    print("No Intelligence, Signal, or Catalyst was created.")
    print("No valuation or investment decision was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
