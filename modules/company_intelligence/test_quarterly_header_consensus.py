import copy
import unittest
from modules.company_intelligence.quarterly_header_consensus import compare_header_passes, reconcile_header_region


class HeaderConsensusTests(unittest.TestCase):
    def binding(self, basis='STANDALONE'):
        return {'tables': [{'table_id': 'table-0', 'columns': [{'column_index': 0}],
                'spans': [{'kind': 'basis', 'text': basis, 'first_column': 0, 'last_column': 0}]}]}

    def test_agreement_does_not_approve(self):
        result = compare_header_passes(self.binding(), self.binding())
        self.assertEqual(result['columns'][0]['fields']['basis']['status'], 'READINGS_AGREE_PENDING_REVIEW')
        self.assertFalse(result['creates_approved_facts'])
        self.assertEqual(result['columns'][0]['status'], 'RESEARCH_HOLD')

    def test_conflict_is_not_replaced_by_new_reading(self):
        first = self.binding()
        original = copy.deepcopy(first)
        result = compare_header_passes(first, self.binding('CONSOLIDATED'))
        self.assertEqual(result['columns'][0]['fields']['basis']['status'], 'CONFLICT_HOLD')
        self.assertEqual(first, original)

    def test_missing_currency_stays_incomplete(self):
        result = compare_header_passes(self.binding(), self.binding())
        self.assertEqual(result['columns'][0]['fields']['unit']['status'], 'INCOMPLETE_HOLD')

    def test_missing_second_table_does_not_imply_agreement(self):
        result = compare_header_passes(self.binding(), {})
        self.assertEqual(result['columns'][0]['fields']['basis']['status'], 'INCOMPLETE_HOLD')

    def test_ambiguous_source_is_not_relabelled_missing(self):
        first = self.binding()
        first['tables'][0]['readings'] = [{'covered_columns': [0], 'issues': ['AMBIGUOUS_DURATION']}]
        result = compare_header_passes(first, self.binding())
        self.assertEqual(result['columns'][0]['fields']['duration']['status'], 'AMBIGUOUS_HOLD')

    def inputs(self):
        digest = 'a' * 64
        page = {'pdf_page': 1, 'ruled_tables': [{'table_id': 'table-0'}]}
        receipt = {'document_hash': digest, 'pdf_page': 1, 'header_binding': self.binding(),
                   'alignment_diagnostics': {'status': 'HOLD_ALIGNMENT_VALIDATION'}}
        region = {'document_hash': digest, 'pdf_page': 1, 'table_id': 'table-0',
                  'image_sha256': 'b' * 64, 'crop_bbox': [0, 0, 100, 50],
                  'image_width': 200, 'image_height': 100, 'pixels_per_pdf_x': 2, 'pixels_per_pdf_y': 2}
        ocr = {'input_sha256': 'b' * 64, 'image_width': 200, 'image_height': 100}
        return page, receipt, region, ocr, digest

    def test_wrong_document_rejected(self):
        args = list(self.inputs())
        args[-1] = 'c' * 64
        with self.assertRaises(ValueError):
            reconcile_header_region(*args)

    def test_wrong_scale_rejected(self):
        args = self.inputs()
        args[2]['pixels_per_pdf_x'] = float('nan')
        with self.assertRaises(ValueError):
            reconcile_header_region(*args)

    def test_rejected_alignment_does_not_create_matches(self):
        result = reconcile_header_region(*self.inputs())
        self.assertEqual(result['second_pass_binding']['status'], 'HOLD_ALIGNMENT')
        self.assertEqual(result['columns'][0]['fields']['basis']['status'], 'INCOMPLETE_HOLD')
