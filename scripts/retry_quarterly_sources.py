"""Preview due quarterly source checks; use --execute for one bounded attempt."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.quarterly_source_retry import run_source_retries

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run_source_retries(ROOT, execute=args.execute), indent=2))
