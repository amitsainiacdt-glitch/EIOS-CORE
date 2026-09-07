"""Conservative recognition of one isolated financial column's full header.

Shared/multi-column page headings are intentionally rejected. A layout adapter
must isolate the heading and include its applicable basis and unit labels.
"""
from calendar import monthrange
from datetime import date, datetime
import re


def recognize_quarterly_header(header):
    result = {'status': 'HOLD', 'header_text': header, 'issues': []}
    if not isinstance(header, str) or not header.strip():
        result['issues'].append('HEADER_MISSING')
        return result
    text = re.sub(r'\s+', ' ', header).strip()
    issues = result['issues']
    if not re.search(r'\b(?:quarter|three\s+months|3\s+months)\s+ended\b', text, re.I):
        issues.append('QUARTER_DURATION_NOT_EXPLICIT')
    if re.search(r'\b(?:year\s+ended|year\s+to\s+date|ytd|half[ -]year|six\s+months|nine\s+months)\b', text, re.I):
        issues.append('ANNUAL_OR_YTD_HEADER')

    bases = {basis.upper() for basis in re.findall(r'\b(standalone|consolidated)\b', text, re.I)}
    if len(bases) != 1:
        issues.append('BASIS_MISSING_OR_AMBIGUOUS')
    units = set()
    for label, pattern in [('INR_CRORE', r'crores?'), ('INR_LAKH', r'lakhs?'), ('INR_MILLION', r'millions?')]:
        if re.search(r'\b' + pattern + r'\b', text, re.I):
            units.add(label)
    inr = bool(re.search(r'₹|\b(?:INR|Rs\.?|rupees)\b', text, re.I))
    other_currency = bool(re.search(r'\b(?:USD|EUR|GBP|dollars|euros)\b|[$€£]', text, re.I))
    if len(units) != 1 or not inr or other_currency:
        issues.append('CURRENCY_OR_UNIT_MISSING_OR_AMBIGUOUS')

    # Day-first numeric dates only. Do not reinterpret ambiguous US dates.
    date_tokens = re.findall(r'\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}[./-]\d{1,2}[./-]\d{4}|\d{1,2}\s+[A-Za-z]+\s+\d{4})\b', text)
    dates = set()
    for token in date_tokens:
        parsed = None
        for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%d %B %Y', '%d %b %Y'):
            try:
                parsed = datetime.strptime(token, fmt).date()
                break
            except ValueError:
                pass
        if parsed is None:
            issues.append('INVALID_DATE_TOKEN')
        else:
            dates.add(parsed)
    if len(dates) != 1:
        issues.append('DATE_MISSING_OR_MULTIPLE_COLUMNS')
    else:
        end = next(iter(dates))
        if end.month not in (3, 6, 9, 12) or end.day != monthrange(end.year, end.month)[1]:
            issues.append('NONSTANDARD_QUARTER_END')
        else:
            start = date(end.year, end.month - 2, 1)
            quarter = f'Q{ {6: 1, 9: 2, 12: 3, 3: 4}[end.month]}-FY{end.year + (end.month > 3)}'
            # A printed FY label must agree with the date-derived quarter.
            printed = re.findall(r'\bQ[1-4]-FY\d{4}\b', text, re.I)
            if any(label.upper() != quarter for label in printed):
                issues.append('PRINTED_QUARTER_CONFLICT')
            if not issues:
                result.update(status='HEADER_RECOGNIZED_PENDING_REVIEW',
                              period_start=start.isoformat(), period_end=end.isoformat(),
                              quarter=quarter, basis=next(iter(bases)), unit=next(iter(units)))
    return result
