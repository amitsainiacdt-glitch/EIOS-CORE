"""One-command local quarterly PDF layout and bounded Windows OCR intake."""
import argparse
import json
from pathlib import Path
from modules.company_intelligence.quarterly_pdf_intake import run_quarterly_intake

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--ticker', required=True)
    parser.add_argument('--company')
    parser.add_argument('--source-url')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(run_quarterly_intake(root / args.file, workspace=root, ticker=args.ticker,
                                        company=args.company, source_url=args.source_url), indent=2))
