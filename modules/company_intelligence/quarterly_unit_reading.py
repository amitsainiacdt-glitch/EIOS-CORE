"""Assess explicit currency/unit labels without guessing damaged symbols."""
import re


def assess_unit_reading(text):
    raw = text
    text = text if isinstance(text, str) else ''
    units = [label for label, pattern in [('crore', r'crores?'), ('lakh', r'lakhs?'), ('million', r'millions?')]
             if re.search(r'\b' + pattern + r'\b', text, re.I)]
    inr = bool(re.search(r'₹|\b(?:INR|Rs\.?|rupees)\b', text, re.I))
    foreign = bool(re.search(r'\b(?:USD|EUR|GBP|dollars|euros|rand|ZAR)\b|[$€£]', text, re.I))
    issues = []
    if len(units) != 1:
        issues.append('UNIT_MISSING_OR_AMBIGUOUS')
    if not inr:
        issues.append('EXPLICIT_INR_MARKER_MISSING')
    if foreign:
        issues.append('FOREIGN_OR_CONFLICTING_CURRENCY')
    return {'status': 'NEEDS_UNIT_REVIEW' if issues else 'UNIT_CANDIDATE_PENDING_REVIEW',
            'raw_text': raw, 'unit_candidates': units, 'issues': issues,
            'currency': 'INR' if inr and not foreign else None, 'creates_approved_facts': False}
