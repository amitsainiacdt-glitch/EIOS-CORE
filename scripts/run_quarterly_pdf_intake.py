"""One-command local quarterly PDF layout and bounded Windows OCR intake."""
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.quarterly_pdf_intake import run_quarterly_intake

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--ticker', required=True)
    parser.add_argument('--company')
    parser.add_argument('--source-url')
    parser.add_argument('--source-verification-from', help='Existing same-document quarterly queue whose source receipt should be reused')
    args = parser.parse_args()
    root = ROOT
    verification = None
    if args.source_verification_from:
        source_path = (root / args.source_verification_from).resolve()
        if root not in source_path.parents:
            raise ValueError('Source verification path must remain inside workspace')
        saved = json.loads(source_path.read_text(encoding='utf-8'))
        verification = saved.get('source_verification')
        if not isinstance(verification, dict):
            raise ValueError('Saved packet has no source verification receipt')
    print(json.dumps(run_quarterly_intake(root / args.file, workspace=root, ticker=args.ticker,
                                        company=args.company, source_url=args.source_url,
                                        source_verification_override=verification), indent=2))
