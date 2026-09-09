"""Strict isolated date-cell comparison; dates never imply a period duration."""
from datetime import date
import re


MONTHS = {name: i for i, names in enumerate((
    ('jan', 'january'), ('feb', 'february'), ('mar', 'march'), ('apr', 'april'),
    ('may',), ('jun', 'june'), ('jul', 'july'), ('aug', 'august'),
    ('sep', 'sept', 'september'), ('oct', 'october'), ('nov', 'november'), ('dec', 'december')
), 1) for name in names}


def parse_date_cell(raw):
    if not isinstance(raw, str) or not raw.strip():
        return {'status': 'HOLD', 'raw_text': raw, 'issue': 'DATE_MISSING'}
    text = re.sub(r'\s+', ' ', raw).strip()
    # Exact whole-cell patterns, not substring recovery from damaged text.
    iso = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', text)
    numeric = re.fullmatch(r'(\d{1,2})([./-])(\d{1,2})\2(\d{4})', text)
    named = re.fullmatch(r'(\d{1,2})\s*([A-Za-z]+)\s*(\d{4})', text)
    month_first = re.fullmatch(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', text)
    try:
        if iso:
            year, month, day = map(int, iso.groups())
        elif named and named[2].lower() in MONTHS:
            day, month, year = int(named[1]), MONTHS[named[2].lower()], int(named[3])
        elif month_first and month_first[1].lower() in MONTHS:
            month, day, year = MONTHS[month_first[1].lower()], int(month_first[2]), int(month_first[3])
        elif numeric:
            day, month, year = int(numeric[1]), int(numeric[3]), int(numeric[4])
            if day <= 12 and month <= 12 and day != month:
                return {'status': 'HOLD', 'raw_text': raw, 'issue': 'AMBIGUOUS_NUMERIC_DATE'}
        else:
            return {'status': 'HOLD', 'raw_text': raw, 'issue': 'UNREADABLE_OR_MULTIPLE_DATES'}
        value = date(year, month, day)
    except ValueError:
        return {'status': 'HOLD', 'raw_text': raw, 'issue': 'INVALID_CALENDAR_DATE'}
    return {'status': 'DATE_PARSED_NOT_APPROVED', 'raw_text': raw, 'date': value.isoformat()}


def compare_date_cells(native_text, ocr_text):
    native, ocr = parse_date_cell(native_text), parse_date_cell(ocr_text)
    if 'date' not in native or 'date' not in ocr:
        status = 'DATE_READING_INCOMPLETE_HOLD'
    elif native['date'] != ocr['date']:
        status = 'DATE_CONFLICT_HOLD'
    else:
        status = 'DATE_READINGS_AGREE_PENDING_REVIEW'
    return {'status': status, 'native': native, 'ocr': ocr, 'creates_approved_facts': False}
