"""Extract held financial row candidates from any locally supplied issuer PDF."""
import argparse
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader
from modules.company_intelligence.quarterly_table_candidates import extract_table_candidates

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--ticker', required=True)
    parser.add_argument('--source-url', required=True)
    args = parser.parse_args()
    path = (ROOT / args.file).resolve()
    if ROOT not in path.parents:
        raise ValueError('Input must be inside workspace')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    reader = PdfReader(path)
    report = extract_table_candidates(
        (page.extract_text(extraction_mode='layout') or '' for page in reader.pages),
        document_hash=digest, source_url=args.source_url, ticker=args.ticker)
    target = ROOT / 'data/runtime/quarterly_candidates' / digest
    target.mkdir(parents=True, exist_ok=True)
    (target / 'candidates.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'candidate_count': report['candidate_count'],
                      'creates_approved_facts': False, 'output': str(target / 'candidates.json')}))


if __name__ == '__main__':
    main()
