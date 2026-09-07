"""Issuer-independent, non-authoritative candidate extraction from PDF layout text.

This stage retains rows, not mapped financial records. Column dates, accounting
basis, units and OCR errors must be reconciled before a candidate can be used.
"""
import re
import math


ROW_LABELS = (
    ('revenue', re.compile(r'revenue\s+from\s+operations', re.I)),
    ('total_income', re.compile(r'total\s+income', re.I)),
    ('pat', re.compile(r'(?:profit|loss).*?(?:after\s+tax|for\s+the\s+(?:period|quarter))', re.I)),
    ('ebitda', re.compile(r'\bebitda\b', re.I)),
)
NUMBER = re.compile(r'-?(?:\d+|\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})*,\d{3})(?:\.\d+)?')


def extract_table_candidates(pages, *, document_hash, source_url, ticker):
    if not re.fullmatch(r'[a-f0-9]{64}', document_hash):
        raise ValueError('A SHA-256 document hash is required')
    if not isinstance(ticker, str) or not ticker.strip():
        raise ValueError('Ticker is required')
    candidates = []
    for page_number, text in enumerate(pages, 1):
        for line_number, line in enumerate(text.splitlines(), 1):
            for metric, pattern in ROW_LABELS:
                match = pattern.search(line)
                if not match:
                    continue
                # A broad profit label must not turn a pre-tax subtotal into PAT.
                if metric == 'pat' and re.search(r'before\s+(?:exceptional.*?and\s+)?tax', line[:match.end()], re.I):
                    continue
                # Layout spacing defines candidate cells, never semantic columns.
                cells = re.split(r'\s{2,}', line[match.end():].strip())
                tokens = []
                for cell in cells:
                    cell = cell.strip()
                    negative = cell.startswith('(') and cell.endswith(')')
                    numeric = cell[1:-1].strip() if negative else cell
                    valid = bool(NUMBER.fullmatch(numeric)) and not (negative and numeric.startswith('-'))
                    value = (-1 if negative else 1) * float(numeric.replace(',', '')) if valid else None
                    if value is not None and not math.isfinite(value):
                        valid, value = False, None
                    tokens.append({'raw': cell, 'numeric_token_valid': valid,
                                   'value': value})
                candidates.append({
                    'candidate_id': f'{document_hash}:{page_number}:{line_number}:{metric}',
                    'metric_candidate': metric, 'pdf_page': page_number,
                    'source_row': re.sub(r'\s+', ' ', line).strip(), 'cells': tokens,
                    'source_layout_row': line,
                    'column_mapping': None, 'unit': None, 'accounting_basis': None,
                    'status': 'HOLD_FOR_COLUMN_RECONCILIATION',
                    'requires_ocr_review': any(not token['numeric_token_valid'] for token in tokens),
                })
                break
    return {'schema_version': 1, 'ticker': ticker, 'document_hash': document_hash,
            'source_url': source_url, 'source_origin': 'LOCAL_FILE_UNVERIFIED_ORIGIN',
            'candidates': candidates, 'candidate_count': len(candidates),
            'status': 'CANDIDATES_HELD' if candidates else 'NO_TABLE_ROWS_IDENTIFIED',
            'creates_approved_facts': False, 'changes_verdict': False,
            'requires_meta_review': True, 'requires_human_review': True}
