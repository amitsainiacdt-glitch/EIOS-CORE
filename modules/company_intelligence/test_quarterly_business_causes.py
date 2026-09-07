import json
import tempfile
import unittest
from pathlib import Path
from modules.company_intelligence.quarterly_business_causes import load_quarterly_business_causes


class QuarterlyBusinessCauseTests(unittest.TestCase):
    def test_selects_exact_reporting_context(self):
        source = Path(__file__).parents[2] / 'data/company_intelligence/quarterly_business_causes.json'
        result = load_quarterly_business_causes(source, ticker='COROMANDEL', period_end='2026-06-30', basis='STANDALONE')
        self.assertEqual('SOURCE_BACKED_CAUSES_AVAILABLE', result['status'])
        self.assertEqual(4, len(result['items']))
        self.assertEqual(3, sum(item['status'] == 'CONFIRMED' for item in result['items']))

    def test_rejects_non_official_source(self):
        item = json.loads((Path(__file__).parents[2] / 'data/company_intelligence/quarterly_business_causes.json').read_text())['items'][0]
        item['source_url'] = 'https://example.com/claim'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'causes.json'; path.write_text(json.dumps({'items':[item]}))
            result = load_quarterly_business_causes(path, ticker='COROMANDEL', period_end='2026-06-30', basis='STANDALONE')
        self.assertEqual([], result['items'])
        self.assertEqual(1, result['invalidCount'])

    def test_wrong_period_is_not_leaked(self):
        source = Path(__file__).parents[2] / 'data/company_intelligence/quarterly_business_causes.json'
        result = load_quarterly_business_causes(source, ticker='COROMANDEL', period_end='2025-06-30', basis='STANDALONE')
        self.assertEqual([], result['items'])


if __name__ == '__main__': unittest.main()
