"""Prepare exact-quarter searches and optionally assess saved results; no API calls."""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.quarterly_search_target import quarterly_search_plan, assess_quarterly_search_results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--company', required=True)
    parser.add_argument('--domain', required=True)
    parser.add_argument('--period-end', required=True)
    parser.add_argument('--saved-results', type=Path)
    args = parser.parse_args()
    plan = quarterly_search_plan(args.company,args.domain,args.period_end)
    output = {'plan':plan,'network_requests':0}
    if args.saved_results:
        saved = json.loads(args.saved_results.read_text(encoding='utf-8'))
        output['assessment'] = assess_quarterly_search_results([SimpleNamespace(**r) for r in saved['results']],plan)
    print(json.dumps(output,indent=2))
