import unittest
from modules.company_intelligence.quarterly_shared_headers import resolve_shared_headers


class SharedHeaderTests(unittest.TestCase):
    def fixture(self):
        binding = {'document_hash': 'c' * 64, 'pdf_page': 1, 'table_id': 'main'}
        column = {**binding, 'column_index': 4, 'date_header_text': '30 June 2026'}
        spans = [{**binding, 'kind': kind, 'text': text, 'first_column': start, 'last_column': end}
                 for kind, text, start, end in [('basis', 'Standalone', 0, 3),
                                               ('basis', 'Consolidated', 4, 7),
                                               ('duration', 'Quarter ended', 4, 6),
                                               ('duration', 'Year ended', 7, 7),
                                               ('unit', 'INR crore', 0, 7)]]
        return column, spans

    def test_group_heading_resolves_correct_basis(self):
        column, spans = self.fixture()
        result = resolve_shared_headers(column, spans)
        self.assertEqual(result['basis'], 'CONSOLIDATED')
        self.assertEqual(result['quarter'], 'Q1-FY2027')
        self.assertFalse(result['creates_approved_facts'])

    def test_annual_column_not_treated_as_quarter(self):
        column, spans = self.fixture()
        column.update(column_index=7, date_header_text='31 March 2026')
        self.assertEqual(resolve_shared_headers(column, spans)['status'], 'HOLD')

    def test_overlap_held_not_nearest_heading(self):
        column, spans = self.fixture()
        spans[0]['last_column'] = 4
        self.assertEqual(resolve_shared_headers(column, spans)['status'], 'HOLD')

    def test_foreign_table_or_page_cannot_supply_header(self):
        for key, value in [('pdf_page', 2), ('table_id', 'segments'), ('document_hash', 'd' * 64)]:
            column, spans = self.fixture()
            spans[-1][key] = value
            self.assertEqual(resolve_shared_headers(column, spans)['status'], 'HOLD')

    def test_corrupt_header_not_repaired(self):
        column, spans = self.fixture()
        spans[1]['text'] = 'ConsoUdated'
        self.assertEqual(resolve_shared_headers(column, spans)['status'], 'HOLD')
