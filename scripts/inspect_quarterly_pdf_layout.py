"""Save source-bound PDF geometry for quarterly reconciliation."""
import argparse
import hashlib
import json
from pathlib import Path
from modules.company_intelligence.quarterly_pdf_layout import extract_pdf_layout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    path = (root / args.file).resolve()
    if root not in path.parents:
        raise ValueError('Input must be inside workspace')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    report = extract_pdf_layout(path)
    report['document_hash'] = digest
    folder = root / 'data/runtime/quarterly_candidates' / digest
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'layout.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'pages': len(report['pages']),
                      'columns': sum(len(page['columns']) for page in report['pages']),
                      'creates_approved_facts': False}))


if __name__ == '__main__':
    main()
