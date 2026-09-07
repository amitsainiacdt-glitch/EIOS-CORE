from copy import deepcopy
import json
from pathlib import Path
import unittest
from modules.company_intelligence.financial_review_examples import build_cash_flow_review_examples


class FinancialReviewExamplesTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[2] / 'data/company_intelligence/coromandel/coromandel_cash_flow_review.json'
        self.pack = json.loads(path.read_text(encoding='utf-8'))

    def test_real_examples_preserve_values_without_recording_decisions(self):
        before = deepcopy(self.pack)
        report = build_cash_flow_review_examples(self.pack)
        self.assertEqual(report['example_count'], 8)
        self.assertEqual(len({row['example_id'] for row in report['examples']}), 8)
        self.assertEqual(next(row for row in report['examples'] if row['period'] == 'FY2022-23')['calculated_free_cash_flow'], -45.01)
        for row in report['examples']:
            self.assertIsNone(row['human_decision'])
            self.assertFalse(row['creates_evidence'])
            self.assertFalse(row['changes_verdict'])
        self.assertEqual(self.pack, before)

    def test_tampered_amount_period_source_and_arithmetic_fail_closed(self):
        for key, value in [('value', 999), ('column', 2), ('document_hash', ''), ('pdf_page', 0), ('raw_value', '999')]:
            pack = deepcopy(self.pack)
            pack['periods'][0]['facts']['operating_cash_flow'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                build_cash_flow_review_examples(pack)
        self.pack['periods'][0]['derived']['free_cash_flow'] = 123
        with self.assertRaises(ValueError):
            build_cash_flow_review_examples(self.pack)

    def test_duplicate_years_and_wrong_review_status_are_rejected(self):
        pack = deepcopy(self.pack)
        pack['periods'].append(deepcopy(pack['periods'][0]))
        with self.assertRaises(ValueError):
            build_cash_flow_review_examples(pack)
        self.pack['periods'][0]['review_status'] = 'APPROVED'
        with self.assertRaises(ValueError):
            build_cash_flow_review_examples(self.pack)
