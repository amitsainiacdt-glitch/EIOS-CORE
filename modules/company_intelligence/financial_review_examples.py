"""Prepare real, source-linked review examples without recording decisions."""
from decimal import Decimal
from hashlib import sha256
import json
import math
import re


def build_cash_flow_review_examples(pack):
    examples, seen = [], set()
    for row in pack['periods']:
        period = row['period']
        if period in seen:
            raise ValueError('Duplicate period')
        seen.add(period)
        if row.get('basis') != 'STANDALONE' or row.get('review_status') != 'PENDING_META_REVIEW' or row.get('creates_evidence') is not False:
            raise ValueError('Only standalone pending-review source records are supported')
        inputs = {}
        for key in ('operating_cash_flow', 'cash_capex'):
            fact = row['facts'][key]
            if (type(fact.get('value')) not in (int, float) or not math.isfinite(fact['value'])
                or fact.get('unit') != 'INR_CRORE' or fact.get('raw_unit') != 'INR_LAKH'
                or not re.fullmatch('[0-9a-f]{64}', fact.get('document_hash', ''))
                or type(fact.get('pdf_page')) is not int or fact['pdf_page'] < 1
                or type(fact.get('column')) is not int or fact['column'] not in (1, 2)
                or len(fact.get('column_periods', [])) != 2
                or fact['column_periods'][fact['column'] - 1] != period
                or not fact.get('source_passage') or not fact.get('source_url', '').startswith('https://')):
                raise ValueError('Unbound source figure')
            raw = fact['raw_value'].replace(',', '').strip()
            number = -Decimal(raw[1:-1]) if raw.startswith('(') and raw.endswith(')') else Decimal(raw)
            expected = abs(number) / 100 if key == 'cash_capex' else number / 100
            if not expected.is_finite() or expected != Decimal(str(fact['value'])):
                raise ValueError('Source amount and displayed value disagree')
            inputs[key] = dict(fact)
        if len({(f['document_hash'], f['column'], tuple(f['column_periods'])) for f in inputs.values()}) != 1:
            raise ValueError('Mixed document versions or year columns')
        free_cash = Decimal(str(inputs['operating_cash_flow']['value'])) - Decimal(str(inputs['cash_capex']['value']))
        if free_cash != Decimal(str(row['derived']['free_cash_flow'])):
            raise ValueError('Free cash flow arithmetic mismatch')
        fingerprint = sha256(json.dumps({'company': pack['company'], 'period': period, 'inputs': inputs}, sort_keys=True).encode()).hexdigest()
        examples.append({'example_id': fingerprint, 'company': pack['company'], 'period': period,
            'inputs': inputs, 'calculated_free_cash_flow': float(free_cash),
            'definition': row['derived']['free_cash_flow_definition'],
            'meaning': 'Fixed-asset cash purchases exceeded operating cash.' if free_cash < 0 else 'Operating cash covered these fixed-asset purchases.',
            'review_questions': ['Does the original PDF show these figures in the stated year column?',
                'Are the statement basis, lakh-to-crore conversion and spending sign correct?',
                'Do restatements or excluded payments require a qualification?'],
            'status': 'AWAITING_SOURCE_REVIEW', 'human_decision': None,
            'creates_evidence': False, 'changes_verdict': False})
    return {'schema_version': 1, 'example_count': len(examples), 'examples': examples,
            'meaning': 'Prepared from existing extraction records, not an independent re-reading of the PDFs. No human approval or learned correction has been recorded.'}
