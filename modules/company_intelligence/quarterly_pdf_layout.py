"""Geometry-preserving PDF column candidates; not approved financial records."""
from io import BytesIO
import re
from modules.company_intelligence.quarterly_header_recognition import recognize_quarterly_header


def group_rows(words, tolerance=2):
    rows = []
    for word in sorted(words, key=lambda w: (w['top'], w['x0'])):
        if not rows or abs(word['top'] - rows[-1][0]['top']) > tolerance:
            rows.append([word])
        else:
            rows[-1].append(word)
    return [sorted(row, key=lambda w: w['x0']) for row in rows]


def classify_table(words):
    """Use explicit table labels; revenue mentions alone never qualify a table."""
    lines = [' '.join(w['text'] for w in row) for row in group_rows(words)]
    first_revenue = next((i for i, line in enumerate(lines)
                          if re.search(r'revenue from operations', line, re.I)), len(lines))
    header = ' '.join(lines[:first_revenue])
    text = ' '.join(lines)
    if re.search(r'\bsegment\s+(?:reporting|information|results)\b', header, re.I):
        return {'kind': 'SEGMENT_TABLE', 'eligible_for_company_financial_mapping': False,
                'reason': 'Segment headings precede the revenue rows.'}
    if (re.search(r'statement of .*?financial results', header, re.I)
            and all(re.search(pattern, text, re.I) for pattern in
                    ('revenue from operations', 'total income', 'net profit after tax'))):
        return {'kind': 'MAIN_STATEMENT_CANDIDATE', 'eligible_for_company_financial_mapping': True,
                'reason': 'Financial-results heading and core statement rows are present; not approval.'}
    return {'kind': 'UNKNOWN_TABLE', 'eligible_for_company_financial_mapping': False,
            'reason': 'Insufficient explicit statement labels; no financial mapping permitted.'}


def column_candidates(words):
    rows = group_rows(words)
    revenue = next((row for row in rows if re.search(r'revenue from operations', ' '.join(w['text'] for w in row), re.I)), None)
    if revenue is None:
        return []
    header_rows = [row for row in rows if row[0]['top'] < revenue[0]['top']]
    year_rows = [(row, [w for w in row if re.fullmatch(r'20\d{2}', w['text'])]) for row in header_rows]
    eligible = [(row, years) for row, years in year_rows if len(years) >= 2]
    if not eligible:
        return []
    _, anchors = eligible[-1]
    centers = [(w['x0'] + w['x1']) / 2 for w in anchors]
    if any(b - a < 10 for a, b in zip(centers, centers[1:])):
        return []
    edges = [centers[0] - (centers[1] - centers[0]) / 2]
    edges += [(a + b) / 2 for a, b in zip(centers, centers[1:])]
    edges += [centers[-1] + (centers[-1] - centers[-2]) / 2]
    columns = []
    for index, (left, right) in enumerate(zip(edges, edges[1:])):
        def within(row):
            return [w for w in row if left <= (w['x0'] + w['x1']) / 2 < right]
        # Shared headings are retained separately, never blindly inherited.
        header = ' '.join(w['text'] for row in header_rows for w in within(row))
        cells = []
        for row in rows:
            if row[0]['top'] < revenue[0]['top']:
                continue
            label = ' '.join(w['text'] for w in row if w['x1'] < edges[0])
            if not re.search(r'revenue from operations|other income|total income|net profit after tax', label, re.I):
                continue
            selected = within(row)
            cells.append({'row_label': label, 'raw_text': ' '.join(w['text'] for w in selected),
                          'words': selected,
                          'boundary_overlap': any(w['x0'] < left or w['x1'] > right for w in selected)})
        columns.append({'column_index': index, 'x_bounds': [left, right],
                        'header_text': header,
                        'header_assessment': recognize_quarterly_header(header),
                        'cells': cells, 'status': 'HOLD_SHARED_HEADER_RECONCILIATION'})
    return columns


def covered_columns(cell_box, columns, tolerance=1):
    """Only fully contained ruled column bands belong to a spanning cell."""
    left, _, right, _ = cell_box
    return [column['column_index'] for column in columns
            if left - tolerance <= column['x_bounds'][0]
            and column['x_bounds'][1] <= right + tolerance]


def ruled_table_geometry(page):
    tables = []
    for table_index, table in enumerate(page.find_tables()):
        extracted = table.extract()
        # A repeated year row gives the individual value cells. Merged cells
        # are not expanded by guessing equal widths.
        date_row = next((i for i, row in enumerate(extracted)
                         if sum(bool(text and re.search(r'\b20\d{2}\b', text)) for text in row) >= 2), None)
        if date_row is None:
            continue
        columns = []
        for text, box in zip(extracted[date_row], table.rows[date_row].cells):
            if box is not None and text and re.search(r'\b20\d{2}\b', text):
                columns.append({'column_index': len(columns), 'x_bounds': [box[0], box[2]],
                                'date_header_text': text, 'date_header_bbox': list(box)})
        headers = []
        for row_index in range(date_row):
            for text, box in zip(extracted[row_index], table.rows[row_index].cells):
                if box is None or not text:
                    continue
                covered = covered_columns(box, columns)
                if not covered:
                    continue
                headers.append({'raw_text': text, 'bbox': list(box),
                                'covered_columns': covered,
                                'status': 'BOUNDARY_DETECTED_TEXT_NOT_VERIFIED'})
        tables.append({'table_id': f'ruled-{table_index}', 'bbox': list(table.bbox),
                       'columns': columns, 'spanning_header_cells': headers,
                       'status': 'HOLD_HEADER_TEXT_REVIEW', 'creates_approved_facts': False})
    return tables


def extract_pdf_layout(path):
    from pypdf import PdfReader, PdfWriter
    import pdfplumber
    output = []
    for number, page in enumerate(PdfReader(path).pages, 1):
        rotation = page.rotation
        # Normalize a memory-only copy. Original bytes and hash never change.
        page.rotate(-rotation)
        writer = PdfWriter()
        writer.add_page(page)
        memory = BytesIO()
        writer.write(memory)
        memory.seek(0)
        with pdfplumber.open(memory) as document:
            words = document.pages[0].extract_words(x_tolerance=1, y_tolerance=2)
            columns = column_candidates(words)
            if columns:
                classification = classify_table(words)
                output.append({'pdf_page': number, 'rotation_normalized': rotation,
                               'table_classification': classification,
                               'ruled_tables': ruled_table_geometry(document.pages[0]),
                               'company_mapping_columns': columns if classification['eligible_for_company_financial_mapping'] else [],
                               'page_words': words, 'columns': columns})
    return {'pages': output, 'creates_approved_facts': False, 'changes_verdict': False,
            'status': 'LAYOUT_CANDIDATES_HELD' if output else 'NO_LAYOUT_IDENTIFIED'}
