"""Resolve source-bound spanning headers without nearest-label guessing.

Spans are explicit column ranges supplied by a layout adapter or review process.
This does not infer cell borders from raw word positions or repair OCR text.
"""
from modules.company_intelligence.quarterly_header_recognition import recognize_quarterly_header
import re


def resolve_shared_headers(column, spans):
    required = ('basis', 'duration', 'unit')
    issues = []
    selected = {}
    digest = column.get('document_hash')
    if (not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest)
            or type(column.get('pdf_page')) is not int or column['pdf_page'] < 1
            or not isinstance(column.get('table_id'), str) or not column['table_id'].strip()):
        return {'status': 'HOLD', 'issues': ['SOURCE_BINDING_INVALID'], 'creates_approved_facts': False}
    index = column.get('column_index')
    if type(index) is not int or index < 0:
        return {'status': 'HOLD', 'issues': ['COLUMN_INDEX_INVALID']}
    for kind in required:
        matches = []
        for span in spans:
            if span.get('kind') != kind:
                continue
            if (span.get('document_hash'), span.get('pdf_page'), span.get('table_id')) != (
                    column.get('document_hash'), column.get('pdf_page'), column.get('table_id')):
                continue
            start, end = span.get('first_column'), span.get('last_column')
            if type(start) is not int or type(end) is not int or start < 0 or end < start:
                issues.append('INVALID_SPAN:' + kind)
                continue
            if start <= index <= end:
                matches.append(span)
        if len(matches) != 1:
            issues.append('MISSING_OR_OVERLAPPING_SPAN:' + kind)
        elif not isinstance(matches[0].get('text'), str) or not matches[0]['text'].strip():
            issues.append('SPAN_TEXT_MISSING:' + kind)
        else:
            selected[kind] = matches[0]
    # A year/date alone must never determine whether a column is annual or quarterly.
    date_text = column.get('date_header_text')
    if not isinstance(date_text, str) or not date_text.strip():
        issues.append('DATE_HEADER_MISSING')
    if issues:
        return {'status': 'HOLD', 'issues': issues, 'creates_approved_facts': False}
    header = ' '.join(selected[kind]['text'] for kind in required) + ' ' + date_text
    assessment = recognize_quarterly_header(header)
    return {**assessment, 'spanning_source_headers': selected,
            'source_column': column, 'creates_approved_facts': False}
