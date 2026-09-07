"""Join recognised headers to agreeing source cells and reconcile totals."""
import re
from decimal import Decimal
from itertools import product
from modules.company_intelligence.quarterly_column_reconciliation import reconcile_column
from modules.company_intelligence.quarterly_ocr_comparison import numeric_reading


def metric_for_label(label):
    label = re.sub(r'^\s*(?:\([a-z]\)|\d+)\s*', '', label).strip().lower()
    exact = {'revenue from operations': 'revenue', 'other income': 'other_income',
             'total income': 'total_income', 'net profit after tax (7-8)': 'pat',
             'net profit after tax': 'pat', 'total expenses':'total_expenses'}
    if label in exact: return exact[label]
    patterns = (
        ('raw_materials', r'^cost of raw materials'), ('traded_goods_purchases', r'^purchases of traded goods'),
        ('inventory_change', r'^changes in inventories'), ('employee_benefits', r'^employee benefits'),
        ('finance_costs', r'^finance costs'), ('depreciation_amortisation', r'^depreciation and amortisation'),
        ('freight_distribution', r'distribution expense$'), ('other_expenses', r'^other expenses$'),
        ('pbt_before_exceptional', r'^profit before exceptional items and tax'), ('profit_before_tax', r'^profit before tax'),
    )
    return next((metric for metric, pattern in patterns if re.search(pattern, label)), None)


def build_record_candidates(page, receipt, ticker, document_hash):
    comparison = receipt.get('comparison', {})
    if (receipt.get('document_hash') != document_hash or receipt.get('pdf_page') != page['pdf_page']
            or comparison.get('document_hash') != document_hash
            or comparison.get('image_sha256') != receipt.get('image_sha256')
            or not comparison.get('alignment_applied')):
        return {'status': 'HOLD_SOURCE_BINDING', 'records': [], 'creates_approved_facts': False}
    results = []
    for table in receipt.get('header_binding', {}).get('tables', []):
        source_tables = [t for t in page.get('ruled_tables', []) if t['table_id'] == table['table_id']]
        if len(source_tables) != 1:
            continue
        for header_column in table['columns']:
            header = header_column['resolution']
            if header['status'] != 'HEADER_RECOGNIZED_PENDING_REVIEW':
                continue
            index = header_column['column_index']
            ruled = [c for c in source_tables[0]['columns'] if c['column_index'] == index]
            mapped = [c for c in page['company_mapping_columns'] if c['column_index'] == index]
            issues, supplemental_issues = [], []
            if len(ruled) != 1 or len(mapped) != 1 or any(
                    abs(a-b) > 1 for a,b in zip(ruled[0]['x_bounds'], mapped[0]['x_bounds'])):
                issues.append('HEADER_VALUE_COLUMN_GEOMETRY_MISMATCH')
            cells, raw_readings, unresolved = {}, [], {}
            core_metrics = {'revenue', 'other_income', 'total_income', 'pat'}
            for metric in ('revenue', 'other_income', 'total_income', 'raw_materials', 'traded_goods_purchases',
                           'inventory_change', 'employee_benefits', 'finance_costs', 'depreciation_amortisation',
                           'freight_distribution', 'other_expenses', 'total_expenses',
                           'pbt_before_exceptional', 'profit_before_tax', 'pat'):
                matches = [c for c in comparison.get('cells', []) if c['column_index'] == index
                           and metric_for_label(c['row_label']) == metric]
                if len(matches) != 1:
                    if metric in core_metrics or len(matches) > 1:
                        (issues if metric in core_metrics else supplemental_issues).append('MISSING_OR_DUPLICATE_METRIC:' + metric)
                    continue
                cell = matches[0]
                raw_readings.append(cell)
                native, ocr = numeric_reading(cell['native_text']), numeric_reading(cell['ocr_text'])
                if (cell['pdf_page'] != page['pdf_page'] or cell['status'] != 'READINGS_AGREE_PENDING_REVIEW'
                        or native is None or ocr is None or native != ocr or not native.is_finite()):
                    unresolved[metric] = (cell, native, ocr)
                    continue
                cells[metric] = {'document_hash': document_hash, 'pdf_page': page['pdf_page'],
                                 'column_index': index, 'value': str(native), 'source_reading': cell}
            # Some old filings have complementary text/OCR defects. Resolve revenue
            # and other income only when one unique pair exactly explains a separately
            # agreeing total; preserve both failed readings and the arithmetic proof.
            if all(name in unresolved for name in ('revenue', 'other_income')) and 'total_income' in cells:
                choices = []
                for name in ('revenue', 'other_income'):
                    cell, native, ocr = unresolved[name]
                    choices.append([(kind, value) for kind, value in (('NATIVE', native), ('OCR', ocr))
                                    if value is not None and value.is_finite()])
                target = Decimal(cells['total_income']['value'])
                matches = [(left, right) for left, right in product(*choices)
                           if abs(left[1] + right[1] - target) <= Decimal('0.02')]
                if len(matches) == 1:
                    for name, selected in zip(('revenue', 'other_income'), matches[0]):
                        original = unresolved.pop(name)[0]
                        reading = {**original, 'status': 'ARITHMETICALLY_TRIANGULATED_PENDING_REVIEW',
                                   'selected_reading': selected[0], 'selected_value': str(selected[1]),
                                   'triangulation': {'method':'REVENUE_PLUS_OTHER_INCOME_EQUALS_TOTAL_INCOME',
                                                     'total_income':str(target), 'tolerance':'0.02'}}
                        cells[name] = {'document_hash':document_hash, 'pdf_page':page['pdf_page'],
                                       'column_index':index, 'value':str(selected[1]), 'source_reading':reading}
            for metric in unresolved:
                (issues if metric in core_metrics else supplemental_issues).append('UNRESOLVED_CELL:' + metric)
            source = {'ticker': ticker, 'document_hash': document_hash, 'pdf_page': page['pdf_page'],
                      'table_id': table['table_id'], 'column_index': index, 'cells': cells,
                      'header_text': header['header_text'], 'header_evidence': header,
                      'raw_readings': raw_readings, 'supplemental_issues': supplemental_issues,
                      **{k: header[k] for k in ('period_start','period_end','quarter','basis','unit')}}
            record = reconcile_column(source)
            if issues:
                record = {**record, 'status': 'HOLD', 'values_inr_crore': {},
                          'issues': [*record['issues'], *issues]}
            results.append(record)
    return {'status': 'REVIEW_CANDIDATES_ONLY', 'records': results,
            'checked_count': sum(r['status'] == 'CHECKED_PENDING_REVIEW' for r in results),
            'held_count': sum(r['status'] == 'HOLD' for r in results),
            'creates_approved_facts': False, 'changes_verdict': False}
