"""Reconcile explicitly mapped quarterly columns; never infer approval.

The mapping producer must supply source-bound headers. This is a deterministic
validation stage, not an OCR or header-recognition implementation.
"""
from calendar import monthrange
from datetime import date
from decimal import Decimal, InvalidOperation
import re
from modules.company_intelligence.quarterly_header_recognition import recognize_quarterly_header

FACTORS = {'INR_CRORE': Decimal('1'), 'INR_LAKH': Decimal('0.01'),
           'INR_MILLION': Decimal('0.1')}


def reconcile_extracted_column(column):
    """Recognize an isolated header, then run arithmetic and binding checks."""
    header = recognize_quarterly_header(column.get('header_text'))
    if header['issues']:
        return {'status': 'HOLD', 'issues': header['issues'],
                'values_inr_crore': {}, 'creates_approved_facts': False,
                'changes_verdict': False}
    fields = ('period_start', 'period_end', 'quarter', 'basis', 'unit')
    conflicts = [key for key in fields if key in column and column[key] != header[key]]
    if conflicts:
        return {'status': 'HOLD', 'issues': ['HEADER_MAPPING_CONFLICT:' + key for key in conflicts],
                'values_inr_crore': {}, 'creates_approved_facts': False,
                'changes_verdict': False}
    return reconcile_column({**column, **{key: header[key] for key in fields}})


def reconcile_column(column):
    """Return held/checked research data from one same-basis source column."""
    errors = []
    quarter = None
    digest = column.get('document_hash', '')
    if not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest):
        errors.append('DOCUMENT_HASH_MISSING')
    if not isinstance(column.get('ticker'), str) or not column['ticker'].strip():
        errors.append('TICKER_MISSING')
    page = column.get('pdf_page')
    index = column.get('column_index')
    if type(page) is not int or page < 1 or type(index) is not int or index < 0:
        errors.append('SOURCE_LOCATION_MISSING')
    if not isinstance(column.get('header_text'), str) or not column['header_text'].strip():
        errors.append('HEADER_TEXT_MISSING')
    if column.get('basis') not in ('STANDALONE', 'CONSOLIDATED'):
        errors.append('ACCOUNTING_BASIS_UNKNOWN')
    factor = FACTORS.get(column.get('unit'))
    if factor is None:
        errors.append('UNIT_UNKNOWN')
    try:
        start = date.fromisoformat(column['period_start'])
        end = date.fromisoformat(column['period_end'])
        if (start.month not in (1, 4, 7, 10) or start.day != 1
                or end.year != start.year or end.month != start.month + 2
                or end.day != monthrange(end.year, end.month)[1]):
            raise ValueError('Not a discrete quarter')
        quarter = f'Q{ {4: 1, 7: 2, 10: 3, 1: 4}[start.month]}-FY{end.year + (end.month > 3)}'
        if column.get('quarter') != quarter:
            errors.append('QUARTER_LABEL_MISMATCH')
    except (ValueError, TypeError, KeyError):
        errors.append('NOT_A_DISCRETE_INDIAN_FINANCIAL_QUARTER')

    values = {}
    for metric in ('revenue', 'other_income', 'total_income', 'raw_materials', 'traded_goods_purchases',
                   'inventory_change', 'employee_benefits', 'finance_costs', 'depreciation_amortisation',
                   'freight_distribution', 'other_expenses', 'total_expenses',
                   'pbt_before_exceptional', 'profit_before_tax', 'pat', 'ebitda'):
        cell = column.get('cells', {}).get(metric)
        if cell is None:
            continue
        # Every mapped cell must bind to the same document, page and column.
        if (cell.get('document_hash'), cell.get('pdf_page'), cell.get('column_index')) != (digest, page, index):
            errors.append(f'CELL_SOURCE_MISMATCH:{metric}')
            continue
        raw = cell.get('value')
        try:
            if type(raw) not in (str, int, float):
                raise ValueError('Invalid value')
            number = Decimal(str(raw))
            if not number.is_finite():
                raise ValueError('Nonfinite value')
            values[metric] = number
        except (InvalidOperation, ValueError):
            errors.append(f'INVALID_NUMBER:{metric}')
    if 'revenue' not in values or 'pat' not in values:
        errors.append('CORE_METRICS_MISSING')
    income_check = 'NOT_CHECKABLE'
    if all(key in values for key in ('revenue', 'other_income', 'total_income')):
        # Tolerance is in original source units, never scaled to company size.
        residual = abs(values['revenue'] + values['other_income'] - values['total_income'])
        income_check = 'PASS' if residual <= Decimal('0.02') else 'FAIL'
    if income_check != 'PASS':
        errors.append('INCOME_RECONCILIATION_' + income_check)
    return {'status': 'HOLD' if errors else 'CHECKED_PENDING_REVIEW',
            'quarter': quarter, 'basis': column.get('basis'),
            'source_unit': column.get('unit'), 'income_check': income_check,
            'values_inr_crore': {key: str(value * factor) for key, value in values.items()} if factor is not None and not errors else {},
            'source_column': column, 'issues': errors,
            'creates_approved_facts': False, 'changes_verdict': False,
            'requires_meta_review': True, 'requires_human_review': True}
