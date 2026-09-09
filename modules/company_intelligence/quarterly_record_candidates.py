"""Join recognised headers to agreeing source cells and reconcile totals."""
import re
from decimal import Decimal
from datetime import datetime
from itertools import product
from modules.company_intelligence.quarterly_column_reconciliation import reconcile_column
from modules.company_intelligence.quarterly_ocr_comparison import numeric_reading


def metric_for_label(label):
    label = re.sub(r'^\s*(?:\([a-z]\)|\d+)\s*', '', label).strip().lower()
    exact = {'revenue from operations': 'revenue', 'other income': 'other_income',
             'total income': 'total_income', 'net profit after tax (7-8)': 'pat',
             'net profit after tax': 'pat', 'profit for the period/year': 'pat',
             'profit for the period': 'pat', 'profit for the quarter': 'pat',
             'total expenses':'total_expenses'}
    if label in exact: return exact[label]
    patterns = (
        ('raw_materials', r'^cost of (?:raw )?materials(?: consumed)?'), ('traded_goods_purchases', r'^purchases of traded goods'),
        ('inventory_change', r'^changes in inventories'), ('employee_benefits', r'^employee benefits'),
        ('finance_costs', r'^finance costs'), ('depreciation_amortisation', r'^depreciation and amortisation'),
        ('freight_distribution', r'distribution expense$'), ('other_expenses', r'^other expenses$'),
        ('pbt_before_exceptional', r'^profit before exceptional items and tax'), ('profit_before_tax', r'^profit before tax'),
        ('pat', r'^profit for the (?:period|quarter)(?:/year)?'),
    )
    return next((metric for metric, pattern in patterns if re.search(pattern, label)), None)


def _reading_options(cell, native, ocr):
    options = {(kind, value) for kind, value in (('NATIVE', native), ('OCR', ocr))
               if value is not None and value.is_finite()}
    # Repair only a missing decimal separator before exactly two terminal digits.
    # The repaired value still needs the complete expense sum to be uniquely valid.
    raw = cell.get('native_text', '').strip()
    if re.fullmatch(r'\(?\d{1,3}(?:,\d{3})*\s\d{2}\)?', raw):
        negative = raw.startswith('('); token = raw.strip('()')
        value = Decimal(token.replace(',', '').replace(' ', '.')) * (-1 if negative else 1)
        options.add(('NATIVE_DECIMAL_REPAIR', value))
    return sorted(options)


def _triangulate_expenses(cells, unresolved, document_hash, page, index):
    names = ('raw_materials','traded_goods_purchases','inventory_change','employee_benefits',
             'finance_costs','depreciation_amortisation','freight_distribution','other_expenses')
    if 'total_expenses' not in cells or not all(name in cells or name in unresolved for name in names):
        return
    choices = []
    for name in names:
        if name in cells:
            choices.append([(name, 'AGREED', Decimal(cells[name]['value']))])
        else:
            cell,native,ocr=unresolved[name]
            choices.append([(name,kind,value) for kind,value in _reading_options(cell,native,ocr)])
    if any(not options for options in choices): return
    target=Decimal(cells['total_expenses']['value'])
    matches=[]
    for combination in product(*choices):
        if abs(sum((item[2] for item in combination),Decimal('0'))-target)<=Decimal('0.02'):
            signature=tuple(item[2] for item in combination)
            if signature not in [tuple(item[2] for item in match) for match in matches]: matches.append(combination)
    if len(matches)!=1: return
    for name,kind,value in matches[0]:
        if name not in unresolved: continue
        original=unresolved.pop(name)[0]
        reading={**original,'status':'EXPENSE_SUM_TRIANGULATED_PENDING_REVIEW','selected_reading':kind,
                 'selected_value':str(value),'triangulation':{'method':'EIGHT_EXPENSE_LINES_EQUAL_TOTAL_EXPENSES',
                 'total_expenses':str(target),'tolerance':'0.02'}}
        cells[name]={'document_hash':document_hash,'pdf_page':page,'column_index':index,
                     'value':str(value),'source_reading':reading}


def _column_geometry_agrees(first, second):
    left, right = first
    other_left, other_right = second
    overlap = max(0, min(right, other_right) - max(left, other_left))
    smaller = min(right - left, other_right - other_left)
    return smaller > 0 and Decimal(str(overlap)) / Decimal(str(smaller)) >= Decimal('0.90')


def _exchange_matched_reading(raw, target):
    """Allow only conventional grouped spaces when an exchange value agrees exactly."""
    if not isinstance(raw, str):
        return None
    text = raw.strip()
    negative = text.startswith('(') and text.endswith(')')
    token = text[1:-1].strip() if negative else text
    if not re.fullmatch(r'\d{1,3}(?:[ ,]\d{3})+(?:\.\d+)?', token):
        return None
    value = Decimal(token.replace(',', '').replace(' ', '')) * (-1 if negative else 1)
    return value if value == target else None


def build_record_candidates(page, receipt, ticker, document_hash, exchange_corroboration=None):
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
            if len(ruled) != 1 or len(mapped) != 1 or not _column_geometry_agrees(
                    ruled[0]['x_bounds'], mapped[0]['x_bounds']):
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
            _triangulate_expenses(cells, unresolved, document_hash, page['pdf_page'], index)
            exchange = exchange_corroboration or {}
            metadata = exchange.get('metadata', {})
            expected = exchange.get('values_inr_lakh', {})
            if (exchange.get('status') == 'EXCHANGE_CORROBORATION_CANDIDATE'
                    and metadata.get('ticker', '').upper() == ticker.upper()
                    and metadata.get('basis', '').upper() == header.get('basis')
                    and metadata.get('period_end') == datetime.strptime(
                        header['period_end'], '%Y-%m-%d').strftime('%d-%m-%Y')):
                for metric in list(unresolved):
                    source_values = expected.get(metric, [])
                    if not source_values:
                        continue
                    target = Decimal(source_values[0])
                    cell, native, ocr = unresolved[metric]
                    readings = [('NATIVE', native), ('OCR', ocr),
                                ('NATIVE_GROUPING_NORMALIZED', _exchange_matched_reading(cell.get('native_text'), target)),
                                ('OCR_GROUPING_NORMALIZED', _exchange_matched_reading(cell.get('ocr_text'), target))]
                    matches = [(kind, value) for kind, value in readings
                               if value is not None and value.is_finite() and value == target]
                    if not matches:
                        continue
                    selected = matches[0]
                    unresolved.pop(metric)
                    reading = {**cell, 'status': 'EXCHANGE_TRIANGULATED_PENDING_REVIEW',
                               'selected_reading': selected[0], 'selected_value': str(selected[1]),
                               'exchange_document_hash': exchange['document_hash'],
                               'exchange_source_url': exchange['source_url']}
                    cells[metric] = {'document_hash':document_hash, 'pdf_page':page['pdf_page'],
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
