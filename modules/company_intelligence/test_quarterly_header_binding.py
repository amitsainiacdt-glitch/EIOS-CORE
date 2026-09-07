import unittest
from unittest.mock import patch
from modules.company_intelligence.quarterly_header_binding import header_meaning, bind_page_headers


class HeaderBindingTests(unittest.TestCase):
    @patch('modules.company_intelligence.quarterly_header_binding.resolve_shared_headers',
           return_value={'status': 'HEADER_RECOGNIZED_PENDING_REVIEW', 'issues': []})
    def test_date_conflict_overrides_otherwise_recognized_header(self, resolve):
        page = {'pdf_page': 1, 'ruled_tables': [{'table_id': 't', 'bbox': [0, 0, 100, 100],
                'spanning_header_cells': [], 'columns': [{'column_index': 0,
                'date_header_text': '30 June 2026', 'date_header_bbox': [0, 10, 100, 30]}]}]}
        ocr = {'input_sha256': 'b' * 64, 'image_width': 100, 'image_height': 100,
               'lines': [{'words': [{'text': '30 June 2025', 'x': 10, 'y': 15, 'width': 70, 'height': 5}]}]}
        receipt = {'document_hash': 'a' * 64, 'image_sha256': 'b' * 64, 'pdf_page': 1,
                   'render_transform': {'normalized_page_bbox': [0,0,100,100], 'image_width': 100,
                   'image_height': 100, 'pixels_per_pdf_x': 1, 'pixels_per_pdf_y': 1}}
        result = bind_page_headers(page, ocr, receipt,
            {'status': 'ALIGNMENT_CHECKED_FOR_COMPARISON', 'ocr_to_native': [[0,1,0],[0,0,1]]})
        column = result['tables'][0]['columns'][0]
        self.assertEqual(column['resolution']['status'], 'HOLD')
        self.assertIn('DATE_CONFLICT_HOLD', column['resolution']['issues'])
        self.assertFalse(column['date_comparison']['creates_approved_facts'])

    def test_ambiguous_duration_preserved(self):
        self.assertEqual(len(header_meaning('Quarter ended Year ended')['duration']), 2)

    def test_corrupt_basis_not_guessed(self):
        self.assertEqual(header_meaning('ConsoUdated results'), {})
        self.assertEqual(header_meaning('Consolidated results')['basis'], ['CONSOLIDATED'])

    def test_source_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            bind_page_headers({'pdf_page': 1}, {'input_sha256': 'wrong'},
                              {'document_hash': 'a' * 64, 'image_sha256': 'b' * 64, 'pdf_page': 1}, {})
