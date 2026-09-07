import unittest
from unittest.mock import patch
from modules.company_intelligence.quarterly_pdf_intake import plan_ocr, run_header_fallback


class IntakePlanTests(unittest.TestCase):
    def page(self, number, eligible=True, held=True):
        return {'pdf_page': number, 'table_classification': {'eligible_for_company_financial_mapping': eligible},
                'columns': [{'header_assessment': {'status': 'HOLD' if held else 'HEADER_RECOGNIZED_PENDING_REVIEW'}}]}

    def test_only_uncertain_main_tables(self):
        chosen, deferred = plan_ocr({'pages': [self.page(1), self.page(2, False), self.page(3, held=False)]})
        self.assertEqual([p['pdf_page'] for p in chosen], [1])
        self.assertEqual(deferred, [])

    def test_budget_defers_explicitly(self):
        chosen, deferred = plan_ocr({'pages': [self.page(1), self.page(2)]}, limit=1)
        self.assertEqual(len(chosen), 1)
        self.assertEqual(deferred, [2])

    def test_invalid_budget_rejected(self):
        for value in (0, 11, True):
            with self.assertRaises(ValueError):
                plan_ocr({'pages': []}, value)

    def report(self, status='HOLD'):
        return {'run_directory': 'saved-run', 'ocr_pages': [{'pdf_page': 1,
                'header_binding': {'tables': [{'columns': [{'resolution': {'status': status}}]}]}}]}

    @patch('modules.company_intelligence.quarterly_pdf_intake.extract_header_regions')
    def test_fallback_only_for_held_headers(self, extract):
        result = run_header_fallback(self.report('HEADER_RECOGNIZED_PENDING_REVIEW'), workspace='.')
        extract.assert_not_called()
        self.assertEqual(result['status'], 'NOT_REQUIRED')

    @patch('modules.company_intelligence.quarterly_pdf_intake.extract_header_regions')
    def test_held_headers_trigger_separate_diagnostic(self, extract):
        extract.return_value = {'status': 'DIAGNOSTIC_ONLY_PENDING_REVIEW', 'creates_approved_facts': False}
        report = self.report()
        result = run_header_fallback(report, workspace='.')
        extract.assert_called_once_with('saved-run', workspace='.', page_numbers=[1])
        self.assertFalse(result['creates_approved_facts'])
        self.assertEqual(report, self.report())

    @patch('modules.company_intelligence.quarterly_pdf_intake.extract_header_regions', side_effect=OSError('unavailable'))
    def test_fallback_failure_remains_held(self, extract):
        result = run_header_fallback(self.report(), workspace='.')
        self.assertEqual(result['status'], 'HEADER_OCR_FAILED_HOLD')
        self.assertFalse(result['creates_approved_facts'])
