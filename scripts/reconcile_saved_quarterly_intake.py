"""Reconcile saved extraction evidence without rerunning OCR or modifying it."""
import argparse
import hashlib
import json
from pathlib import Path
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    run = (root / args.run).resolve()
    if root not in run.parents:
        raise ValueError('Run must be inside workspace')
    intake = json.loads((run / 'intake.json').read_text(encoding='utf-8'))
    layout = json.loads((run / 'layout.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256((run / 'source.pdf').read_bytes()).hexdigest()
    if digest != intake['document_hash']:
        raise ValueError('Source PDF hash mismatch')
    outputs = [build_record_candidates(page, receipt, intake['ticker'], digest)
               for page in layout['pages'] for receipt in intake['ocr_pages']
               if page['pdf_page'] == receipt['pdf_page']]
    print(json.dumps(outputs, indent=2))


if __name__ == '__main__':
    main()
