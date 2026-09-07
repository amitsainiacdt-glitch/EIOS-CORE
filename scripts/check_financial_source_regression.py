"""Run the local source-consistency check without collection or approvals."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.source_review_regression import check_source_review_regression


def run_check():
    return check_source_review_regression(ROOT,
        ROOT / 'data/runtime/financial_source_assistant_review.json',
        ROOT / 'data/company_intelligence/coromandel/coromandel_cash_flow_review.json')


if __name__ == '__main__':
    report = run_check()
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if report['issues'] else 0)
