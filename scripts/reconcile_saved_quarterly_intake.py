"""Reconcile saved extraction evidence without rerunning OCR or modifying it."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_review_bridge import write_quarterly_review_queue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    parser.add_argument('--write-review-queue', action='store_true')
    args = parser.parse_args()
    root = ROOT
    run = (root / args.run).resolve()
    if root not in run.parents:
        raise ValueError('Run must be inside workspace')
    intake = json.loads((run / 'intake.json').read_text(encoding='utf-8'))
    layout = json.loads((run / 'layout.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256((run / 'source.pdf').read_bytes()).hexdigest()
    if digest != intake['document_hash']:
        raise ValueError('Source PDF hash mismatch')
    pairs = [(receipt, build_record_candidates(page, receipt, intake['ticker'], digest))
             for page in layout['pages'] for receipt in intake['ocr_pages']
             if page['pdf_page'] == receipt['pdf_page']]
    outputs = [result for _, result in pairs]
    response = {'reconciliations': outputs, 'creates_approved_facts': False, 'changes_verdict': False}
    if args.write_review_queue:
        output = run / 'reconciled-triangulation-v1'
        if output.exists():
            raise ValueError('Reconciled output already exists')
        report = {**intake, 'ocr_pages': [{**receipt, 'record_candidates': result} for receipt, result in pairs]}
        response['review_queue'] = write_quarterly_review_queue(report, output_directory=output,
            company=next((item.get('company') for item in [intake] if item.get('company')), None)
                    or json.loads(next(run.glob('quarterly-candidates.json')).read_text(encoding='utf-8'))['company'],
            source_url=json.loads(next(run.glob('quarterly-candidates.json')).read_text(encoding='utf-8'))['candidates'][0]['source_url'])
    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main()
