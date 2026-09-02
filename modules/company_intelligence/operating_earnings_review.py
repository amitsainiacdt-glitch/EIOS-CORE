"""Explicit operating-earnings calculation; not an issuer-reported EBITDA claim."""
import re
from decimal import Decimal
import math
from copy import deepcopy
from modules.company_intelligence.local_cash_flow_extractor import PAIR, amount


def extract_operating_earnings(text, period, column, source):
    if column not in (0, 1) or source['column_periods'][column] != period:
        raise ValueError('Wrong earnings period/column')
    if not re.search(r'in\s+lakhs', text, re.I):
        raise ValueError('Earnings units missing')
    labels = {
        'revenue': r'^Revenue from operations\b',
        'other_income': r'^Other income\b',
        'finance_costs': r'^Finance costs\b',
        'depreciation_amortisation': r'^Depreciation and amortisation expenses?\b',
        'profit_before_exceptional_and_tax': r'^(?:III|V)\s+Profit before exceptional items and tax\b',
    }
    if not any(re.search(labels['profit_before_exceptional_and_tax'], l.strip()) for l in text.splitlines()):
        labels['profit_before_exceptional_and_tax'] = r'^(?:III|V)\s+Profit before tax\b'
        # Do not silently ignore an exceptional-item row in an unfamiliar layout.
        if re.search(r'(?im)^\s*IV\s+Exceptional', text):
            raise ValueError('Exceptional items require explicit pre-exceptional profit')
    facts = {}
    for key, pattern in labels.items():
        lines = [l.strip() for l in text.splitlines() if re.search(pattern, l.strip())]
        if len(lines) != 1 or not PAIR.search(lines[0]):
            raise ValueError(f'Missing/ambiguous earnings row: {key}')
        raw = PAIR.search(lines[0]).group(column + 1)
        facts[key] = {**source, 'raw_value': raw, 'raw_unit': 'INR_LAKH', 'unit': 'INR_CRORE',
                      'value': float(amount(raw)/100), 'source_passage': lines[0], 'column': column + 1}
    v = lambda key: Decimal(str(facts[key]['value']))
    calculation = v('profit_before_exceptional_and_tax') + v('finance_costs') + v('depreciation_amortisation') - v('other_income')
    return {'period': period, 'basis': 'STANDALONE', 'facts': facts,
            'calculated_operating_ebitda': float(calculation),
            'formula': 'Profit before exceptional items and tax + finance costs + depreciation/amortisation - other income',
            'limitation': 'Calculated measure, not an issuer-reported EBITDA quote. Includes all reported finance costs (including lease interest where applicable); accounting and business-scope changes still require review.',
            'review_status': 'PENDING_META_REVIEW', 'creates_evidence': False}


def validate_earnings_review(pack):
    """Recheck saved inputs and arithmetic before presentation, not META approval."""
    result = deepcopy(pack)
    seen = set()
    for row in result.get('periods', []):
        period = row['period']
        if period in seen or row.get('basis') != 'STANDALONE' or row.get('review_status') != 'PENDING_META_REVIEW' or row.get('creates_evidence') is not False:
            raise ValueError('Invalid/duplicate earnings review period')
        seen.add(period)
        keys = ('revenue', 'other_income', 'finance_costs', 'depreciation_amortisation', 'profit_before_exceptional_and_tax')
        sources = set()
        for key in keys:
            f = row['facts'][key]
            if (type(f.get('value')) not in (int, float) or not math.isfinite(f['value']) or
                f.get('unit') != 'INR_CRORE' or f.get('raw_unit') != 'INR_LAKH' or
                not re.fullmatch(r'[0-9a-f]{64}', f.get('document_hash', '')) or
                type(f.get('pdf_page')) is not int or f['pdf_page'] < 1 or f.get('column') not in (1, 2) or
                f.get('column_periods', [None, None])[f['column']-1] != period):
                raise ValueError('Unbound earnings input')
            if Decimal(str(f['value'])) != amount(f['raw_value']) / 100:
                raise ValueError('Raw and converted earnings inputs disagree')
            sources.add((f['document_hash'], f['pdf_page'], f['column']))
        if len(sources) != 1:
            raise ValueError('Mixed source versions in earnings calculation')
        v = lambda key: Decimal(str(row['facts'][key]['value']))
        expected = v(keys[4]) + v(keys[2]) + v(keys[3]) - v(keys[1])
        supplied = row.get('calculated_operating_ebitda')
        if type(supplied) not in (int, float) or not math.isfinite(supplied) or Decimal(str(supplied)) != expected:
            raise ValueError('Operating earnings arithmetic mismatch')
        row['arithmetic_status'] = 'INPUTS_AND_CALCULATION_CHECKED'
    return result
