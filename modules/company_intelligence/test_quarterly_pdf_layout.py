import unittest
from modules.company_intelligence.quarterly_pdf_layout import column_candidates, classify_table, covered_columns, statement_context


def word(text, x, y, width=10):
    return {'text': text, 'x0': x, 'x1': x + width, 'top': y, 'bottom': y + 5}


class QuarterlyPdfLayoutTests(unittest.TestCase):
    def test_shared_cell_covers_only_contained_columns(self):
        columns = [{'column_index': 0, 'x_bounds': [0, 40]},
                   {'column_index': 1, 'x_bounds': [40, 80]},
                   {'column_index': 2, 'x_bounds': [80, 120]}]
        self.assertEqual(covered_columns([0, 0, 80, 10], columns), [0, 1])
        self.assertEqual(covered_columns([20, 0, 60, 10], columns), [])

    def test_segment_table_is_not_company_statement(self):
        words = [word('Segment reporting', 0, 1), word('Revenue from operations', 0, 10),
                 word('Total income', 0, 20), word('Net profit after tax', 0, 30)]
        self.assertEqual(classify_table(words)['kind'], 'SEGMENT_TABLE')
        self.assertFalse(classify_table(words)['eligible_for_company_financial_mapping'])

    def test_main_statement_requires_heading_and_core_rows(self):
        words = [word('Statement of Unaudited Financial Results', 0, 1),
                 word('Revenue from operations', 0, 10), word('Total income', 0, 20),
                 word('Net profit after tax', 0, 30)]
        self.assertEqual(classify_table(words)['kind'], 'MAIN_STATEMENT_CANDIDATE')
        self.assertEqual(classify_table(words[1:])['kind'], 'UNKNOWN_TABLE')

    def test_main_statement_accepts_profit_for_period_label(self):
        words = [word('Statement of Consolidated Unaudited Financial Results', 0, 1),
                 word('Revenue from operations', 0, 10), word('Total income', 0, 20),
                 word('Profit for the period/year', 0, 30)]
        self.assertEqual(classify_table(words)['kind'], 'MAIN_STATEMENT_CANDIDATE')

    def test_unknown_text_does_not_grant_mapping(self):
        self.assertFalse(classify_table([word('Revenue from operations', 0, 1)])['eligible_for_company_financial_mapping'])

    def test_keeps_columns_and_missing_cells_separate(self):
        words = [word('2026', 100, 10), word('2025', 150, 10),
                 word('Revenue from operations', 5, 30, 65), word('100', 100, 30), word('bad', 150, 30),
                 word('Other income', 5, 40, 65), word('2', 150, 40)]
        columns = column_candidates(words)
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0]['cells'][1]['raw_text'], '')
        self.assertEqual(columns[1]['cells'][0]['raw_text'], 'bad')
        self.assertTrue(all(c['header_assessment']['status'] == 'HOLD' for c in columns))

    def test_no_header_does_not_guess_columns(self):
        self.assertEqual(column_candidates([word('Revenue from operations', 5, 30)]), [])

    def test_complete_dates_are_column_anchors(self):
        words = [word('30.06.2026', 100, 10, 35), word('30.06.2025', 160, 10, 35),
                 word('Revenue from operations', 5, 30, 65), word('100', 110, 30), word('90', 170, 30),
                 word('Profit for the period/year', 5, 40, 70), word('8', 110, 40), word('7', 170, 40)]
        columns = column_candidates(words)
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0]['cells'][1]['row_label'], 'Profit for the period/year')

    def test_statement_context_retains_explicit_basis_and_quarter_end(self):
        words = [word(text, i * 40, 1, 35) for i, text in enumerate(
            ('Statement', 'of', 'Consolidated', 'Unaudited', 'Financial', 'Results',
             'for', 'the', 'Quarter', 'Ended', 'June', '30,', '2026'))]
        words += [word('Revenue from operations', 5, 30, 65)]
        context = statement_context(words)
        self.assertEqual(context['basis_candidates'], ['CONSOLIDATED'])
        self.assertEqual(context['current_quarter_end_text'], 'June 30, 2026')
