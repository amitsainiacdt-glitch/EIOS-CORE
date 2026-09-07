"""Compare native and OCR cell readings in normalized page coordinates."""
from decimal import Decimal
import math
from modules.company_intelligence.quarterly_table_candidates import NUMBER


def numeric_reading(text):
    text = text.strip()
    negative = text.startswith('(') and text.endswith(')')
    token = text[1:-1].strip() if negative else text
    if not NUMBER.fullmatch(token) or (negative and token.startswith('-')):
        return None
    return Decimal(token.replace(',', '')) * (-1 if negative else 1)


def compare_page(page, ocr, receipt, document_hash, alignment=None):
    """Never infer approval from agreement between two fallible extractors."""
    if (receipt.get('document_hash') != document_hash
            or receipt.get('pdf_page') != page.get('pdf_page')
            or receipt.get('image_sha256') != ocr.get('input_sha256')
            or not receipt.get('image_sha256')):
        raise ValueError('OCR source binding mismatch')
    transform = receipt['render_transform']
    sx, sy = transform['pixels_per_pdf_x'], transform['pixels_per_pdf_y']
    if any(type(value) not in (int, float) or not math.isfinite(value) or value <= 0 for value in (sx, sy)):
        raise ValueError('Invalid render scale')
    if (ocr['image_width'], ocr['image_height']) != (transform['image_width'], transform['image_height']):
        raise ValueError('OCR dimensions mismatch')
    origin_x, origin_y = transform['normalized_page_bbox'][:2]
    words = [word for line in ocr['lines'] for word in line['words']]
    alignment_ok = alignment is not None and alignment.get('status') == 'ALIGNMENT_CHECKED_FOR_COMPARISON'
    def center(word):
        x = origin_x + (word['x'] + word['width'] / 2) / sx
        y = origin_y + (word['y'] + word['height'] / 2) / sy
        if alignment_ok:
            return tuple(sum(a * b for a, b in zip(row, [1, x, y])) for row in alignment['ocr_to_native'])
        return x, y
    comparisons = []
    for column in page['company_mapping_columns']:
        left, right = column['x_bounds']
        for cell in column['cells']:
            native_words = cell['words']
            selected = []
            if native_words:
                top = min(w['top'] for w in native_words) - 1
                bottom = max(w['bottom'] for w in native_words) + 1
                selected = [w for w in words if left <= center(w)[0] < right and top <= center(w)[1] <= bottom]
            # Joining separate OCR fragments could change a number: retain spaces.
            raw_ocr = ' '.join(w['text'] for w in sorted(selected, key=lambda w: (w['y'], w['x'])))
            native = numeric_reading(cell['raw_text'])
            reading = numeric_reading(raw_ocr)
            if alignment is not None and not alignment_ok:
                status = 'HOLD_ALIGNMENT_VALIDATION'
            elif cell['boundary_overlap']:
                status = 'HOLD_CELL_BOUNDARY_OVERLAP'
            elif native is None or reading is None:
                status = 'HOLD_UNREADABLE_OR_MISSING'
            elif native != reading:
                status = 'HOLD_EXTRACTOR_DISAGREEMENT'
            else:
                status = 'READINGS_AGREE_PENDING_REVIEW'
            comparisons.append({'pdf_page': page['pdf_page'], 'column_index': column['column_index'],
                'row_label': cell['row_label'], 'native_text': cell['raw_text'], 'ocr_text': raw_ocr,
                'status': status, 'creates_approved_facts': False})
    return {'document_hash': document_hash, 'image_sha256': receipt['image_sha256'],
            'alignment_applied': alignment_ok,
            'cells': comparisons, 'agreement_count': sum(c['status'] == 'READINGS_AGREE_PENDING_REVIEW' for c in comparisons),
            'hold_count': sum(c['status'] != 'READINGS_AGREE_PENDING_REVIEW' for c in comparisons),
            'creates_approved_facts': False, 'changes_verdict': False}
