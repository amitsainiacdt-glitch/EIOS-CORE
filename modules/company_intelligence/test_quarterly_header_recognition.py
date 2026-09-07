import unittest
from modules.company_intelligence.quarterly_header_recognition import recognize_quarterly_header


class QuarterlyHeaderRecognitionTests(unittest.TestCase):
    def test_supported_dates_and_units(self):
        for date in ('30 June 2026', '30 Jun 2026', '30.06.2026', '2026-06-30'):
            header = recognize_quarterly_header(f'Consolidated INR crore Quarter ended {date}')
            self.assertEqual(header['quarter'], 'Q1-FY2027')
            self.assertEqual(header['period_start'], '2026-04-01')

    def test_march_quarter(self):
        header = recognize_quarterly_header('Standalone Rs. lakhs Three months ended 31 March 2026')
        self.assertEqual(header['quarter'], 'Q4-FY2026')
        self.assertEqual(header['unit'], 'INR_LAKH')

    def test_ambiguous_and_incomplete_headers_held(self):
        for header in (
            'Quarter ended 30 June 2026',
            'Standalone Consolidated INR crore Quarter ended 30 June 2026',
            'Standalone INR crore Quarter ended 30 June 2026 30 June 2025',
            'Standalone INR crore Year ended 31 March 2026',
            'Standalone INR crore Quarter ended 30 June 2026 YTD',
            'Standalone USD million Quarter ended 30 June 2026',
            'Standalone INR crore USD Quarter ended 30 June 2026',
            'Standalone INR lakh crore Quarter ended 30 June 2026',
            'Standalone INR crore Quarter ended 31 June 2026',
            'Standalone INR crore Quarter ended 30 June 2026 Q1-FY2026',
        ):
            with self.subTest(header=header):
                self.assertEqual(recognize_quarterly_header(header)['status'], 'HOLD')
