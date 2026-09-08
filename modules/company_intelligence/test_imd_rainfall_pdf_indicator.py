import unittest

from modules.company_intelligence.imd_rainfall_pdf_indicator import parse_imd_country_rainfall_pdf_text


TEXT = '''India Meteorological Department
SUBDIVISION-WISE RAINFALL (MM) DISTRIBUTION
DAY: 07-09-2026 to 07-09-2026 PERIOD: 01-06-2026 to 07-09-2026
S.No METEOROLOGICAL SUBDIVISIONS ACTUAL(mm) NORMAL(mm) %DEP. CAT. ACTUAL(mm) NORMAL(mm) %DEP. CAT.
COUNTRY AS A WHOLE 4.1 6.7 -39% D 642.9 748.3 -14% N'''


class ImdRainfallPdfIndicatorTests(unittest.TestCase):
    def test_extracts_cumulative_not_daily_departure_and_reconciles(self):
        result = parse_imd_country_rainfall_pdf_text(TEXT)
        self.assertEqual('2026-09-07', result['reporting_date'])
        self.assertEqual('2026-06-01', result['period_start'])
        self.assertEqual('-14', result['cumulative_departure'])
        self.assertEqual('14', result['deficit_magnitude'])
        self.assertEqual('642.9', result['cumulative_actual'])
        self.assertEqual('748.3', result['cumulative_normal'])

    def test_rejects_ambiguous_period_or_country_row(self):
        with self.assertRaisesRegex(ValueError, 'unique cumulative period'):
            parse_imd_country_rainfall_pdf_text(TEXT.replace('01-06-2026 to 07-09-2026', ''))
        with self.assertRaisesRegex(ValueError, 'unique country-as-a-whole row'):
            parse_imd_country_rainfall_pdf_text(TEXT + '\n' + TEXT.splitlines()[-1])

    def test_rejects_non_reconciling_departure(self):
        with self.assertRaisesRegex(ValueError, 'does not reconcile'):
            parse_imd_country_rainfall_pdf_text(TEXT.replace('-14% N', '-4% N'))

    def test_surplus_has_zero_deficit_magnitude(self):
        result = parse_imd_country_rainfall_pdf_text(TEXT.replace('642.9 748.3 -14% N', '755.8 748.3 1% N'))
        self.assertEqual('1', result['cumulative_departure'])
        self.assertEqual('0', result['deficit_magnitude'])

    def test_accepts_imd_whole_percent_rounding(self):
        result = parse_imd_country_rainfall_pdf_text(TEXT.replace('642.9 748.3 -14% N', '645.5 754.5 -14% N'))
        self.assertEqual('14', result['deficit_magnitude'])


if __name__ == '__main__':
    unittest.main()
