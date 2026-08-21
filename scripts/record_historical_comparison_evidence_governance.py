"""Record explicit human governance for one exact scored Evidence pack."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_evidence_governance_ledger import (
    HistoricalComparisonEvidenceGovernanceLedger,
)
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import (
    HistoricalComparisonEvidencePackScoringLedger,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Record explicit assumptions, kill switches, and monitoring "
            "signals for one exact scored Evidence pack."
        )
    )
    parser.add_argument("--scoring-receipt-path")
    parser.add_argument("--governance-ledger-path")
    parser.add_argument("--pack-fingerprint", required=True)
    parser.add_argument("--assumption", action="append", required=True)
    parser.add_argument("--kill-switch-json", action="append", required=True)
    parser.add_argument("--monitoring-signal", action="append", required=True)
    parser.add_argument("--analyst", required=True)
    parser.add_argument("--rationale", required=True)
    parser.add_argument("--governed-at", required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    scoring_value = args.scoring_receipt_path or os.environ.get(
        "EIOS_HISTORICAL_COMPARISON_EVIDENCE_SCORING_RECEIPT_PATH", ""
    ).strip()
    governance_value = args.governance_ledger_path or os.environ.get(
        "EIOS_HISTORICAL_COMPARISON_EVIDENCE_GOVERNANCE_LEDGER_PATH", ""
    ).strip()
    if not scoring_value or not governance_value:
        print("Configuration error: scoring and governance paths are required.")
        return 1
    scoring_path = Path(scoring_value)
    governance_path = Path(governance_value)
    if scoring_path.resolve() == governance_path.resolve():
        print("Evidence governance error: source and governance paths must differ.")
        return 1
    scoring_before = scoring_path.read_bytes() if scoring_path.is_file() else None
    try:
        governed_at = datetime.fromisoformat(args.governed_at)
        kill_switches = [json.loads(value) for value in args.kill_switch_json]
        fingerprint = args.pack_fingerprint.casefold()
        matches = [
            item
            for item in HistoricalComparisonEvidencePackScoringLedger(
                scoring_path
            ).read_all()
            if item.pack_fingerprint == fingerprint
        ]
        if len(matches) != 1:
            raise ValueError("pack fingerprint was not found uniquely")
        governance = HistoricalComparisonEvidenceGovernanceLedger(
            governance_path
        ).record(
            matches[0],
            assumptions=args.assumption,
            kill_switches=kill_switches,
            monitoring_signals=args.monitoring_signal,
            analyst=args.analyst,
            rationale=args.rationale,
            governed_at=governed_at,
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Evidence governance error: {exc}")
        return 1
    if scoring_before is not None and scoring_path.read_bytes() != scoring_before:
        print("Evidence governance error: scoring receipt file changed.")
        return 1
    print(f"Governed pack: {governance.pack_fingerprint}")
    print(f"Entity: {governance.entity}")
    print(f"Assumptions: {len(governance.assumptions)}")
    print(f"Kill switches: {len(governance.kill_switches)}")
    print(f"Monitoring signals: {len(governance.monitoring_signals)}")
    print("Governance record appended.")
    print("No Evidence pack was rescored.")
    print("No Intelligence, Signal, or Catalyst was created.")
    print("No valuation or investment decision was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
