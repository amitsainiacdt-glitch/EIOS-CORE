import unittest
from modules.company_intelligence.quarterly_crop_alignment import check_crop_alignment


class CropAlignmentTests(unittest.TestCase):
    def inputs(self):
        native, words = [], []
        for x in (10,35,60,85):
            for y in (10,35,60,85):
                native.append({'text': 'March', 'x0': x-3, 'x1': x+3, 'top': y-2, 'bottom': y+2})
                words.append({'text': 'March', 'x': x-3, 'y': y-2, 'width': 6, 'height': 4})
        return native, {'lines': [{'words': words}]}, {
            'crop_bbox': [0,0,100,100], 'pixels_per_pdf_x': 1, 'pixels_per_pdf_y': 1}, {
            'status': 'ALIGNMENT_CHECKED_FOR_COMPARISON', 'ocr_to_native': [[0,1,0],[0,0,1]]}

    def test_repeated_labels_with_unique_spatial_matches(self):
        result = check_crop_alignment(*self.inputs())
        self.assertEqual(result['status'], 'CROP_ALIGNMENT_CHECKED_FOR_COMPARISON')
        self.assertEqual(result['anchor_count'], 16)
        self.assertFalse(result['creates_approved_facts'])

    def test_shifted_crop_rejected_without_refitting(self):
        args = self.inputs()
        for word in args[1]['lines'][0]['words']:
            word['x'] += 5
        self.assertEqual(check_crop_alignment(*args)['status'], 'HOLD_CROP_ALIGNMENT')

    def test_narrow_anchor_coverage_rejected(self):
        args = self.inputs()
        args[2]['crop_bbox'] = [0,0,400,400]
        self.assertIn('INSUFFICIENT_HORIZONTAL_COVERAGE', check_crop_alignment(*args)['issues'])

    def test_numbers_do_not_validate_alignment(self):
        args = self.inputs()
        for word in args[1]['lines'][0]['words']:
            word['text'] = '2026'
        self.assertEqual(check_crop_alignment(*args)['anchor_count'], 0)

    def test_duplicate_candidates_not_counted_twice(self):
        args = self.inputs()
        args[0].extend(list(args[0]))
        self.assertEqual(check_crop_alignment(*args)['anchor_count'], 0)

    def test_unchecked_full_page_transform_rejected(self):
        args = self.inputs()
        args[3]['status'] = 'HOLD'
        self.assertEqual(check_crop_alignment(*args)['status'], 'HOLD_CROP_ALIGNMENT')
