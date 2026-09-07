import unittest
from modules.company_intelligence.quarterly_ocr_comparison import compare_page, numeric_reading


class OcrComparisonTests(unittest.TestCase):
    def test_failed_alignment_holds_even_matching_numbers(self):
        result = compare_page(*self.fixture(), 'a' * 64, alignment={'status': 'HOLD_ALIGNMENT_VALIDATION'})
        self.assertEqual(result['agreement_count'], 0)
        self.assertEqual(result['cells'][0]['status'], 'HOLD_ALIGNMENT_VALIDATION')

    def test_checked_alignment_used_for_cell_selection(self):
        page, ocr, receipt = self.fixture()
        ocr['lines'][0]['words'][0]['y'] += 40
        alignment = {'status': 'ALIGNMENT_CHECKED_FOR_COMPARISON', 'ocr_to_native': [[0, 1, 0], [-20, 0, 1]]}
        self.assertEqual(compare_page(page, ocr, receipt, 'a' * 64, alignment)['agreement_count'], 1)

    def fixture(self, text='100.00'):
        page = {'pdf_page': 1, 'company_mapping_columns': [{'column_index': 0, 'x_bounds': [0, 50],
            'cells': [{'row_label': 'Revenue', 'raw_text': '100.00', 'boundary_overlap': False,
                       'words': [{'top': 10, 'bottom': 20}]}]}]}
        ocr = {'input_sha256': 'b' * 64, 'image_width': 200, 'image_height': 100,
               'lines': [{'words': [{'text': text, 'x': 10, 'y': 20, 'width': 20, 'height': 10}]}]}
        receipt = {'document_hash': 'a' * 64, 'pdf_page': 1, 'image_sha256': 'b' * 64,
                   'render_transform': {'pixels_per_pdf_x': 2, 'pixels_per_pdf_y': 2,
                      'normalized_page_bbox': [0, 0, 100, 50], 'image_width': 200, 'image_height': 100}}
        return page, ocr, receipt

    def test_agreement_does_not_approve(self):
        result = compare_page(*self.fixture(), 'a' * 64)
        self.assertEqual(result['agreement_count'], 1)
        self.assertFalse(result['creates_approved_facts'])

    def test_disagreement_and_corruption_held(self):
        for text in ('1000.00', '1OO.OO', ''):
            self.assertEqual(compare_page(*self.fixture(text), 'a' * 64)['hold_count'], 1)

    def test_hash_or_dimensions_mismatch_rejected(self):
        for key, value in [('input_sha256', 'wrong'), ('image_width', 400)]:
            page, ocr, receipt = self.fixture()
            ocr[key] = value
            with self.assertRaises(ValueError):
                compare_page(page, ocr, receipt, 'a' * 64)

    def test_neighboring_cell_not_used(self):
        page, ocr, receipt = self.fixture()
        ocr['lines'][0]['words'][0]['x'] = 160
        self.assertEqual(compare_page(page, ocr, receipt, 'a' * 64)['hold_count'], 1)

    def test_strict_numeric_semantics(self):
        self.assertEqual(numeric_reading('(1,000.25)'), -numeric_reading('1000.25'))
        self.assertEqual(numeric_reading('0'), 0)
        self.assertIsNone(numeric_reading('-'))
        self.assertIsNone(numeric_reading('31,479,54'))
