"""Print review-memory measurements without changing reviews or approvals."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.review_memory_report import build_review_memory_report


def main():
    report = build_review_memory_report(
        ROOT / 'data/company_intelligence/company_fact_human_reviews.jsonl',
        evaluated_at=datetime.now(timezone.utc))
    print(json.dumps(report, indent=2))
    return 1 if report['failed_review_ids'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
