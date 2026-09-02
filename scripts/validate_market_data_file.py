"""Validate a local market-data JSON export without importing it into valuation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {"current_price", "consensus_eps", "approved"}


def validate(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    if not isinstance(payload, dict):
        return ["Root value must be an object keyed by ticker."]
    for ticker, record in payload.items():
        if not isinstance(record, dict):
            errors.append(f"{ticker}: record must be an object")
            continue
        missing = REQUIRED - record.keys()
        if missing:
            errors.append(f"{ticker}: missing {', '.join(sorted(missing))}")
        if record.get("approved") is True and (record.get("current_price") is None or record.get("consensus_eps") is None):
            errors.append(f"{ticker}: approved records require price and consensus_eps")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/validate_market_data_file.py <file.json>")
    problems = validate(Path(sys.argv[1]))
    if problems:
        print("INVALID")
        print("\n".join(f"- {item}" for item in problems))
        raise SystemExit(1)
    print("VALID: market-data file meets the EIOS intake contract")
