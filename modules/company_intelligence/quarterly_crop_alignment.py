"""Check a transferred full-page transform against fresh crop OCR anchors."""
import math
import re


def check_crop_alignment(native_words, ocr, region, alignment):
    held = {'status': 'HOLD_CROP_ALIGNMENT', 'creates_approved_facts': False}
    if alignment.get('status') != 'ALIGNMENT_CHECKED_FOR_COMPARISON':
        return {**held, 'issues': ['FULL_PAGE_ALIGNMENT_UNCHECKED']}
    box = region['crop_bbox']
    def key(text):
        return text.lower() if re.fullmatch(r'[A-Za-z]{4,}', text) else None
    native = [{'text': key(w['text']), 'x': (w['x0']+w['x1'])/2, 'y': (w['top']+w['bottom'])/2}
              for w in native_words if key(w['text'])]
    mapped = []
    for line in ocr['lines']:
        for w in line['words']:
            if not key(w['text']):
                continue
            x = box[0] + (w['x']+w['width']/2)/region['pixels_per_pdf_x']
            y = box[1] + (w['y']+w['height']/2)/region['pixels_per_pdf_y']
            nx, ny = [sum(a*b for a,b in zip(row, (1,x,y))) for row in alignment['ocr_to_native']]
            if not math.isfinite(nx) or not math.isfinite(ny):
                return {**held, 'issues': ['NONFINITE_PROJECTION']}
            mapped.append({'text': key(w['text']), 'x': nx, 'y': ny})
    anchors = []
    def nearby(point, choices):
        return [i for i, other in enumerate(choices) if point['text'] == other['text']
                and max(abs(point['x']-other['x']), abs(point['y']-other['y'])) <= 1.5]
    for i, point in enumerate(mapped):
        matches = nearby(point, native)
        if len(matches) != 1 or nearby(native[matches[0]], mapped) != [i]:
            continue
        target = native[matches[0]]
        anchors.append({'text': point['text'], 'crop_projected': [point['x'], point['y']],
                        'native': [target['x'],target['y']],
                        'error': max(abs(point['x']-target['x']),abs(point['y']-target['y']))})
    issues = []
    if len(anchors) < 12:
        issues.append('TOO_FEW_CROP_ANCHORS')
    fraction = len(anchors)/len(mapped) if mapped else 0
    if fraction < .65:
        issues.append('TOO_MANY_UNMATCHED_CROP_LABELS')
    for axis, extent in ((0,box[2]-box[0]),(1,box[3]-box[1])):
        coverage = (max(a['native'][axis] for a in anchors)-min(a['native'][axis] for a in anchors)) if anchors else 0
        if coverage < extent * (.6 if axis == 0 else .4):
            issues.append('INSUFFICIENT_' + ('HORIZONTAL' if axis == 0 else 'VERTICAL') + '_COVERAGE')
    return {**held, 'status': 'HOLD_CROP_ALIGNMENT' if issues else 'CROP_ALIGNMENT_CHECKED_FOR_COMPARISON',
            'issues': issues, 'anchor_count': len(anchors), 'matched_fraction': fraction,
            'anchors': anchors, 'max_error': max((a['error'] for a in anchors), default=None)}
