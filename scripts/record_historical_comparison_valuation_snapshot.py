"""Record a governed snapshot of an authoritative ValuationSection."""

import argparse
import json
from dataclasses import fields
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.master_dossier.valuation_section import ValuationSection


def parser():
    result = argparse.ArgumentParser(description="Record an authoritative EIOS valuation snapshot receipt.")
    for name in ("valuation-json-path", "receipt-ledger-path", "entity", "recorder", "rationale", "recorded-at"):
        result.add_argument("--" + name, required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    source, destination = Path(args.valuation_json_path), Path(args.receipt_ledger_path)
    try:
        if source.resolve() == destination.resolve():
            raise ValueError("receipt ledger must be distinct from the valuation JSON")
        before = source.read_bytes()
        payload = json.loads(before)
        if not isinstance(payload, dict):
            raise ValueError("valuation JSON must contain one object")
        allowed = {field.name for field in fields(ValuationSection)}
        unknown = set(payload) - allowed
        if unknown:
            raise ValueError("valuation JSON contains unknown fields: " + ", ".join(sorted(unknown)))
        valuation = ValuationSection(**payload)
        receipt = HistoricalComparisonValuationSnapshotLedger(destination).record(
            valuation, entity=args.entity, recorder=args.recorder, rationale=args.rationale,
            recorded_at=datetime.fromisoformat(args.recorded_at),
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Valuation snapshot error: {exc}")
        return 1
    if source.read_bytes() != before:
        print("Valuation snapshot error: source valuation JSON changed.")
        return 1
    print(f"Entity: {receipt.entity}")
    print(f"Valuation fingerprint: {receipt.valuation_fingerprint}")
    print("Snapshot receipt appended. Valuation and Mispricing engines were not invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
