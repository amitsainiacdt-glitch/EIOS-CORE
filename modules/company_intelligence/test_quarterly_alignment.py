import unittest
from modules.company_intelligence.quarterly_alignment import estimate_alignment, validate_alignment


class AlignmentTests(unittest.TestCase):
    def test_validation_checks_omitted_anchor_predictions(self):
        points = [{'ocr': [x, y], 'native': [x + 3, y - 4]} for x in (0, 100, 200, 300) for y in (0, 100, 200, 300)]
        result = validate_alignment({'anchors': points})
        self.assertEqual(result['status'], 'ALIGNMENT_CHECKED_FOR_COMPARISON')
        points[0]['native'] = [50, 50]
        self.assertEqual(validate_alignment({'anchors': points})['status'], 'HOLD_ALIGNMENT_VALIDATION')

    def test_validation_rejects_narrow_coverage(self):
        points = [{'ocr': [x, y], 'native': [x, y]} for x in (0, 1, 2, 3) for y in (0, 1, 2, 3)]
        self.assertEqual(validate_alignment({'anchors': points})['status'], 'HOLD_ALIGNMENT_VALIDATION')

    def test_known_shift_and_tilt_recovered_without_numeric_anchors(self):
        native, words = [], []
        labels = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india']
        for i, label in enumerate(labels):
            x, y = (i % 3) * 100, (i // 3) * 100
            native.append({'text': label, 'x0': x, 'x1': x + 10, 'top': y, 'bottom': y + 10})
            words.append({'text': label, 'x': x + 3, 'y': y + 7, 'width': 10, 'height': 10})
        transform = {'pixels_per_pdf_x': 1, 'pixels_per_pdf_y': 1, 'normalized_page_bbox': [0, 0, 300, 300]}
        result = estimate_alignment(native, {'lines': [{'words': words}]}, transform)
        self.assertAlmostEqual(result['ocr_to_native'][0][0], -3)
        self.assertAlmostEqual(result['ocr_to_native'][1][0], -7)
        self.assertLess(result['max_residual_pdf_units'], 0.001)
        self.assertFalse(result['creates_approved_facts'])

    def test_insufficient_labels_are_held(self):
        result = estimate_alignment([], {'lines': []}, {'pixels_per_pdf_x': 1, 'pixels_per_pdf_y': 1, 'normalized_page_bbox': [0, 0, 10, 10]})
        self.assertEqual(result['status'], 'HOLD_INSUFFICIENT_ALIGNMENT_ANCHORS')
