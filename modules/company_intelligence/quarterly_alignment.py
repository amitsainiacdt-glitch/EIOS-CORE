"""Measure native/OCR registration from unique textual labels, not numbers."""
from collections import Counter
from statistics import median
import re


# Two PDF points are about 0.7 mm and remain far below a financial column's
# detected width. This gate compares held-out text anchors, never numeric cells.
MAX_HELD_OUT_ANCHOR_ERROR_PDF_UNITS = 2.0


def _key(text):
    text = text.strip('.,:;()').lower()
    return text if re.fullmatch(r'[a-z]{4,}', text) else None


def _solve(matrix, values):
    rows = [list(row) + [value] for row, value in zip(matrix, values)]
    for i in range(3):
        pivot = max(range(i, 3), key=lambda j: abs(rows[j][i]))
        rows[i], rows[pivot] = rows[pivot], rows[i]
        if abs(rows[i][i]) < 1e-9:
            raise ValueError('Degenerate anchors')
        scale = rows[i][i]
        rows[i] = [x / scale for x in rows[i]]
        for j in range(3):
            if j != i:
                scale = rows[j][i]
                rows[j] = [a - scale * b for a, b in zip(rows[j], rows[i])]
    return [row[-1] for row in rows]


def _fit(points):
    basis = [[1, p['ocr'][0], p['ocr'][1]] for p in points]
    matrix = [[sum(v[i] * v[j] for v in basis) for j in range(3)] for i in range(3)]
    return [_solve(matrix, [sum(v[i] * p['native'][axis] for v, p in zip(basis, points)) for i in range(3)]) for axis in (0, 1)]


def validate_alignment(estimate):
    """Cross-check with each anchor omitted from its own fit; not accuracy proof."""
    points = estimate.get('anchors', [])
    issues = []
    if len(points) < 12:
        return {**estimate, 'status': 'HOLD_ALIGNMENT_VALIDATION', 'issues': ['TOO_FEW_VALIDATION_ANCHORS']}
    if any(max(p['ocr'][axis] for p in points) - min(p['ocr'][axis] for p in points) < 150 for axis in (0, 1)):
        issues.append('ANCHOR_COVERAGE_TOO_NARROW')
    errors = []
    try:
        coefficients = _fit(points)
        for i, point in enumerate(points):
            fit = _fit(points[:i] + points[i + 1:])
            errors.append(max(abs(sum(a * b for a, b in zip(row, [1, *point['ocr']])) - point['native'][axis])
                              for axis, row in enumerate(fit)))
        x, y = coefficients
        if (abs(x[0]) > 20 or abs(y[0]) > 20 or abs(x[1] - 1) > .03
                or abs(y[2] - 1) > .03 or abs(x[2]) > .06 or abs(y[1]) > .06):
            issues.append('EXCESSIVE_GEOMETRIC_DISTORTION')
        if max(errors) > MAX_HELD_OUT_ANCHOR_ERROR_PDF_UNITS:
            issues.append('HELD_OUT_ANCHOR_ERROR')
    except ValueError:
        issues.append('DEGENERATE_VALIDATION')
    return {**estimate, 'status': 'HOLD_ALIGNMENT_VALIDATION' if issues else 'ALIGNMENT_CHECKED_FOR_COMPARISON',
            'ocr_to_native': coefficients if not issues else None,
            'issues': issues, 'max_leave_one_out_error': max(errors) if errors else None,
            'creates_approved_facts': False}


def estimate_alignment(native_words, ocr, transform):
    words = [w for line in ocr['lines'] for w in line['words']]
    native_counts = Counter(_key(w['text']) for w in native_words)
    ocr_counts = Counter(_key(w['text']) for w in words)
    lookup = {_key(w['text']): w for w in words if _key(w['text'])}
    sx, sy = transform['pixels_per_pdf_x'], transform['pixels_per_pdf_y']
    ox, oy = transform['normalized_page_bbox'][:2]
    points = []
    for word in native_words:
        key = _key(word['text'])
        if key and native_counts[key] == 1 and ocr_counts[key] == 1:
            other = lookup[key]
            points.append({'label': key,
                'native': [(word['x0'] + word['x1']) / 2, (word['top'] + word['bottom']) / 2],
                'ocr': [ox + (other['x'] + other['width'] / 2) / sx, oy + (other['y'] + other['height'] / 2) / sy]})
    original_count = len(points)
    for _ in range(4):
        if len(points) < 8:
            return {'status': 'HOLD_INSUFFICIENT_ALIGNMENT_ANCHORS', 'anchor_count': len(points)}
        try:
            coefficients = _fit(points)
        except ValueError:
            return {'status': 'HOLD_DEGENERATE_ALIGNMENT', 'anchor_count': len(points)}
        residuals = [max(abs(sum(a * b for a, b in zip(row, [1, *p['ocr']])) - p['native'][axis])
                         for axis, row in enumerate(coefficients)) for p in points]
        threshold = max(2, median(residuals) * 3)
        kept = [p for p, error in zip(points, residuals) if error <= threshold]
        if len(kept) == len(points):
            break
        points = kept
    if len(points) < 8:
        return {'status': 'HOLD_INSUFFICIENT_ALIGNMENT_ANCHORS', 'anchor_count': len(points)}
    try:
        coefficients = _fit(points)
    except ValueError:
        return {'status': 'HOLD_DEGENERATE_ALIGNMENT', 'anchor_count': len(points)}
    residuals = [max(abs(sum(a * b for a, b in zip(row, [1, *p['ocr']])) - p['native'][axis])
                     for axis, row in enumerate(coefficients)) for p in points]
    # Diagnostics only. A fit is not permission to realign financial cells yet.
    return {'status': 'ALIGNMENT_ESTIMATE_PENDING_VALIDATION', 'anchor_count': len(points),
            'original_anchor_count': original_count, 'ocr_to_native': coefficients,
            'max_residual_pdf_units': max(residuals), 'anchors': points,
            'creates_approved_facts': False}
