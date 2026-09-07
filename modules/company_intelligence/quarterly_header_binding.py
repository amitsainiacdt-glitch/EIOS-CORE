"""Bind text/OCR header candidates to detected ruled cells; never approve data."""
import re
from modules.company_intelligence.quarterly_shared_headers import resolve_shared_headers
from modules.company_intelligence.quarterly_heading_partition import propose_duration_partition
from modules.company_intelligence.quarterly_date_comparison import compare_date_cells
from modules.company_intelligence.quarterly_unit_reading import assess_unit_reading


def header_meaning(text):
    patterns = {'basis': {'STANDALONE': r'\bstandalone\b', 'CONSOLIDATED': r'\bconsolidated\b'},
                'duration': {'Quarter ended': r'\bquarter\s+ended\b', 'Year ended': r'\byear\s+ended\b'}}
    result = {}
    for kind, choices in patterns.items():
        matches = [value for value, pattern in choices.items() if re.search(pattern, text, re.I)]
        if matches:
            result[kind] = matches
    return result


def bind_page_headers(page, ocr, receipt, alignment):
    if (receipt.get('image_sha256') != ocr.get('input_sha256') or not receipt.get('document_hash')
            or receipt.get('pdf_page') != page.get('pdf_page')):
        raise ValueError('Header source binding mismatch')
    if alignment.get('status') != 'ALIGNMENT_CHECKED_FOR_COMPARISON':
        return {'status': 'HOLD_ALIGNMENT', 'tables': [], 'creates_approved_facts': False}
    transform = receipt['render_transform']
    if (ocr['image_width'], ocr['image_height']) != (transform['image_width'], transform['image_height']):
        raise ValueError('Header image dimensions mismatch')
    ox, oy = transform['normalized_page_bbox'][:2]
    mapped = []
    for line in ocr['lines']:
        for word in line['words']:
            x = ox + (word['x'] + word['width'] / 2) / transform['pixels_per_pdf_x']
            y = oy + (word['y'] + word['height'] / 2) / transform['pixels_per_pdf_y']
            nx, ny = [sum(a * b for a, b in zip(row, [1, x, y])) for row in alignment['ocr_to_native']]
            # Horizontal extent is conservative under the checked affine map.
            half_width = abs(alignment['ocr_to_native'][0][1]) * word['width'] / transform['pixels_per_pdf_x'] / 2
            half_width += abs(alignment['ocr_to_native'][0][2]) * word['height'] / transform['pixels_per_pdf_y'] / 2
            mapped.append({'text': word['text'], 'x': nx, 'y': ny, 'x0': nx - half_width, 'x1': nx + half_width})
    def read_box(box):
        selected = [w for w in mapped if box[0] <= w['x'] < box[2] and box[1] <= w['y'] < box[3]]
        return ' '.join(w['text'] for w in sorted(selected, key=lambda w: (round(w['y'] / 3), w['x'])))
    tables = []
    for table in page.get('ruled_tables', []):
        binding = {'document_hash': receipt['document_hash'], 'pdf_page': page['pdf_page'], 'table_id': table['table_id']}
        spans, readings, proposed_partitions = [], [], []
        for cell in table['spanning_header_cells']:
            native, recognized = header_meaning(cell['raw_text']), header_meaning(read_box(cell['bbox']))
            entry = {'native_text': cell['raw_text'], 'ocr_text': read_box(cell['bbox']),
                     'covered_columns': cell['covered_columns'], 'bbox': cell['bbox'], 'issues': []}
            for kind in ('basis', 'duration'):
                candidates = set(native.get(kind, []) + recognized.get(kind, []))
                multiple_durations = kind == 'duration' and max(
                    len(re.findall(r'\bended\b', text, re.I)) for text in (entry['native_text'], entry['ocr_text'])) > 1
                if len(candidates) > 1 or multiple_durations:
                    entry['issues'].append('AMBIGUOUS_' + kind.upper())
                    if kind == 'duration':
                        box = cell['bbox']
                        proposals = propose_duration_partition(
                            [w for w in mapped if box[0] <= w['x'] < box[2] and box[1] <= w['y'] < box[3]],
                            [c for c in table['columns'] if c['column_index'] in cell['covered_columns']])
                        if proposals:
                            proposed_partitions.append({'source_bbox': box, 'source_readings': entry,
                                'spans': [{**binding, **p} for p in proposals], 'creates_approved_facts': False})
                elif len(candidates) == 1:
                    spans.append({**binding, 'kind': kind, 'text': next(iter(candidates)),
                                  'first_column': min(cell['covered_columns']), 'last_column': max(cell['covered_columns']),
                                  'source_readings': entry, 'status': 'HEADER_CANDIDATE_NOT_APPROVED'})
            readings.append(entry)
        # Currency/unit must be explicit in the narrow region above this table.
        box = table['bbox']
        unit_text = read_box([box[0], max(0, box[1] - 12), box[2], box[1]])
        unit_assessment = assess_unit_reading(unit_text)
        units = [label for label, pattern in [('INR crore', r'crores?'), ('INR lakh', r'lakhs?'), ('INR million', r'millions?')]
                 if re.search(r'\b' + pattern + r'\b', unit_text, re.I)]
        currency_explicit = bool(re.search(r'₹|\bINR\b|\bRs\.?\b|\brupees\b', unit_text, re.I))
        foreign = bool(re.search(r'\b(?:USD|EUR|GBP)\b|[$€£]', unit_text, re.I))
        if len(units) == 1 and currency_explicit and not foreign and unit_assessment['status'] == 'UNIT_CANDIDATE_PENDING_REVIEW':
            spans.append({**binding, 'kind': 'unit', 'text': units[0], 'first_column': 0,
                          'last_column': len(table['columns']) - 1, 'raw_text': unit_text})
        columns = []
        for column in table['columns']:
            # Insert a space between joined day/month OCR tokens; preserve source.
            native_date = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', column['date_header_text'])
            resolved = resolve_shared_headers({**binding, **column, 'date_header_text': native_date}, spans)
            dates = compare_date_cells(column['date_header_text'], read_box(column['date_header_bbox']))
            if dates['status'] != 'DATE_READINGS_AGREE_PENDING_REVIEW':
                resolved = {**resolved, 'status': 'HOLD',
                            'issues': [*resolved.get('issues', []), dates['status']]}
            columns.append({'column_index': column['column_index'], 'resolution': resolved,
                            'date_comparison': {**binding, 'column_index': column['column_index'],
                                                'source_bbox': column['date_header_bbox'], **dates}})
        tables.append({'table_id': table['table_id'], 'readings': readings, 'unit_source_text': unit_text,
                       'unit_assessment': {**binding, **unit_assessment},
                       'proposed_duration_partitions': proposed_partitions,
                       'spans': spans, 'columns': columns})
    return {'status': 'HEADER_CANDIDATES_PENDING_REVIEW', 'tables': tables, 'creates_approved_facts': False}
