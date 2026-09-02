"""Preserve eight years of operating-earnings calculation inputs for review."""
import hashlib
import json
import sys
from pathlib import Path
from pypdf import PdfReader
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.extract_coromandel_cash_flow_history import SOURCES
from scripts.extract_coromandel_balance_sheet_history import PAGES
from modules.company_intelligence.operating_earnings_review import extract_operating_earnings

def main():
    directory = ROOT / 'data/company_intelligence/coromandel'
    reports = {r['financial_year']: r for r in json.loads((directory/'coromandel_annual_report_library.json').read_text(encoding='utf-8'))['reports']}
    periods = []
    for suffix, _, columns in SOURCES:
        paths = list((ROOT/'tmp/pdfs').glob(f'*{suffix}.pdf'))
        if len(paths) != 1:
            raise ValueError('Ambiguous earnings document')
        path = paths[0]
        page = 117 if suffix == '2017_18' else PAGES[suffix]
        year = suffix.replace('_', '-')
        source = {'pdf_page': page, 'report_year': year,
                  'source_url': reports[year]['official_url'], 'url_kind': reports[year]['access'],
                  'document_hash': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'column_periods': [f'FY{year}', f'FY{int(suffix[:4])-1}-{suffix[2:4]}']}
        text = PdfReader(path).pages[page-1].extract_text()
        periods.extend(extract_operating_earnings(text, p, c, source) for p,c in columns)
    output = directory/'coromandel_operating_earnings_review.json'
    output.write_text(json.dumps({'schema_version': 1, 'ticker': 'COROMANDEL', 'periods': periods,
        'extracted_fact_count': 40, 'calculated_fact_count': 8, 'creates_evidence': False,
        'review_status': 'PENDING_META_REVIEW'}, indent=2)+'\n', encoding='utf-8')
    print('Extracted 40 input figures; calculated eight operating EBITDA values. No governed history was overwritten.')

if __name__ == '__main__':
    main()
