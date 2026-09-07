import unittest
from types import SimpleNamespace
from modules.company_intelligence.quarterly_search_target import quarterly_search_plan, assess_quarterly_search_results


class QuarterlySearchTargetTests(unittest.TestCase):
    def assess(self, title, url='https://www.coromandel.biz/report.pdf'):
        plan = quarterly_search_plan('Coromandel', 'coromandel.biz', '2026-06-30')
        return assess_quarterly_search_results([SimpleNamespace(title=title,url=url)],plan)['results'][0]['status']

    def test_indian_fiscal_year_mapping(self):
        self.assertEqual(quarterly_search_plan('Example','example.com','2026-06-30')['label'],'Q1 FY2027')
        self.assertEqual(quarterly_search_plan('Example','example.com','2026-03-31')['label'],'Q4 FY2026')

    def test_wrong_quarter_rejected(self):
        self.assertEqual(self.assess('Q3 FY26 results'),'DIFFERENT_QUARTER')

    def test_same_quarter_wrong_year_rejected(self):
        self.assertEqual(self.assess('Q1 FY2026 results'),'DIFFERENT_QUARTER')

    def test_correct_target_still_only_candidate(self):
        self.assertEqual(self.assess('Q1 FY27 results'),'TARGET_QUARTER_CANDIDATE')

    def test_fiscal_range(self):
        self.assertEqual(self.assess('Q1 FY2026-27 results'),'TARGET_QUARTER_CANDIDATE')

    def test_multiple_periods_ambiguous(self):
        self.assertEqual(self.assess('Q1 FY27 versus Q1 FY26'),'AMBIGUOUS_PERIOD_METADATA')

    def test_upload_path_not_reporting_date(self):
        self.assertEqual(self.assess('Financial results','https://coromandel.biz/2026/07/Q1.pdf'),'PERIOD_UNCONFIRMED')

    def test_lookalike_rejected(self):
        self.assertEqual(self.assess('Q1 FY27','https://coromandel.biz.evil.com/a.pdf'),'UNTRUSTED_SOURCE_LOCATION')

    def test_invalid_target_rejected(self):
        with self.assertRaises(ValueError):
            quarterly_search_plan('Example','example.com','2026-06-29')

    def test_invalid_year_range_not_accepted(self):
        self.assertEqual(self.assess('Q1 FY2025-27'),'AMBIGUOUS_PERIOD_METADATA')

    def test_previous_live_result_titles_do_not_match(self):
        titles = ['Coromandel International Delivers Resilient Q3 FY26 Results',
                  'Coromandel International Limited Posts FY26 Results Sustains Growth Momentum',
                  'Coromandel International Investor Presentation – Q4 FY26',
                  '“Coromandel International Limited Q3 FY26 Earnings ...',
                  'Coromandel International Limited']
        self.assertEqual([self.assess(title) for title in titles],
                         ['DIFFERENT_QUARTER','PERIOD_UNCONFIRMED','DIFFERENT_QUARTER',
                          'DIFFERENT_QUARTER','PERIOD_UNCONFIRMED'])
