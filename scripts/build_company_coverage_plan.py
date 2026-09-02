"""Materialize a governed company monitoring plan for inspection and registration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.company_intelligence.company_coverage_orchestrator import CompanyCoverageProfile, build_company_coverage_plan


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--exchange", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--issuer-investor-url", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    plan = build_company_coverage_plan(CompanyCoverageProfile(args.company_id, args.name, args.ticker, args.exchange, args.sector, args.issuer_investor_url))
    output = (ROOT / args.output).resolve()
    if ROOT.resolve() not in output.parents:
        raise ValueError("output must remain inside the EIOS workspace")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"Coverage plan written: {plan.profile.ticker} | {len(plan.jobs)} recurring jobs")


if __name__ == "__main__":
    main()
