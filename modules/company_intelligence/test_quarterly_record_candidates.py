import unittest
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates, metric_for_label


class RecordCandidateTests(unittest.TestCase):
    def test_complementary_readings_can_be_uniquely_triangulated_by_total(self):
        page, receipt, ticker, digest = self.fixture()
        revenue = next(c for c in receipt['comparison']['cells'] if c['column_index'] == 0 and 'Revenue' in c['row_label'])
        other = next(c for c in receipt['comparison']['cells'] if c['column_index'] == 0 and 'Other income' in c['row_label'])
        revenue['native_text'] = 'unreadable'; revenue['status'] = 'HOLD_UNREADABLE_OR_MISSING'
        other['ocr_text'] = 'unreadable'; other['status'] = 'HOLD_UNREADABLE_OR_MISSING'
        result = build_record_candidates(page, receipt, ticker, digest)['records'][0]
        self.assertEqual(result['status'], 'CHECKED_PENDING_REVIEW')
        self.assertEqual(result['source_column']['cells']['revenue']['source_reading']['selected_reading'], 'OCR')
        self.assertEqual(result['source_column']['cells']['other_income']['source_reading']['selected_reading'], 'NATIVE')

    def test_triangulation_rejects_values_that_do_not_explain_total(self):
        page, receipt, ticker, digest = self.fixture()
        revenue = next(c for c in receipt['comparison']['cells'] if c['column_index'] == 0 and 'Revenue' in c['row_label'])
        other = next(c for c in receipt['comparison']['cells'] if c['column_index'] == 0 and 'Other income' in c['row_label'])
        revenue['native_text'] = 'unreadable'; revenue['ocr_text'] = '999'; revenue['status'] = 'HOLD_UNREADABLE_OR_MISSING'
        other['ocr_text'] = 'unreadable'; other['status'] = 'HOLD_UNREADABLE_OR_MISSING'
        result = build_record_candidates(page, receipt, ticker, digest)['records'][0]
        self.assertEqual(result['status'], 'HOLD')
        self.assertIn('UNRESOLVED_CELL:revenue', result['issues'])
    def fixture(self):
        digest = 'a' * 64
        column = {'column_index': 0, 'x_bounds': [10,60]}
        page = {'pdf_page': 1, 'ruled_tables': [{'table_id': 't', 'columns': [column]}],
                'company_mapping_columns': [dict(column)]}
        header = {'status': 'HEADER_RECOGNIZED_PENDING_REVIEW', 'header_text': 'STANDALONE Quarter ended INR crore 30 June 2026',
                  'period_start': '2026-04-01', 'period_end': '2026-06-30', 'quarter': 'Q1-FY2027',
                  'basis': 'STANDALONE', 'unit': 'INR_CRORE'}
        cells = [{'pdf_page': 1, 'column_index': 0, 'row_label': label, 'native_text': value,
                  'ocr_text': value, 'status': 'READINGS_AGREE_PENDING_REVIEW'} for label,value in
                 [('(a) Revenue from operations','100'),('(b) Other income','2'),('Total income','102'),
                  ('9 Net profit after tax (7-8)','10')]]
        receipt = {'document_hash': digest, 'pdf_page': 1, 'image_sha256': 'b' * 64,
                   'comparison': {'document_hash': digest, 'image_sha256': 'b' * 64,
                                  'alignment_applied': True, 'cells': cells},
                   'header_binding': {'tables': [{'table_id': 't', 'columns': [{'column_index': 0, 'resolution': header}]}]}}
        return page, receipt, 'EXAMPLE', digest

    def test_consistent_record_still_requires_reviews(self):
        result = build_record_candidates(*self.fixture())
        self.assertEqual(result['checked_count'], 1)
        record = result['records'][0]
        self.assertEqual(record['values_inr_crore']['revenue'], '100')
        self.assertTrue(record['requires_meta_review'])
        self.assertTrue(record['requires_human_review'])
        self.assertFalse(record['creates_approved_facts'])

    def test_wrong_source_rejected(self):
        args = list(self.fixture())
        args[-1] = 'c' * 64
        self.assertEqual(build_record_candidates(*args)['status'], 'HOLD_SOURCE_BINDING')

    def test_shifted_column_rejected(self):
        args = self.fixture()
        args[0]['company_mapping_columns'][0]['x_bounds'] = [60,110]
        record = build_record_candidates(*args)['records'][0]
        self.assertEqual(record['status'], 'HOLD')
        self.assertEqual(record['values_inr_crore'], {})

    def test_small_boundary_detection_difference_is_not_a_column_mismatch(self):
        args = self.fixture()
        args[0]['company_mapping_columns'][0]['x_bounds'] = [12, 59]
        self.assertNotIn('HEADER_VALUE_COLUMN_GEOMETRY_MISMATCH',
                         build_record_candidates(*args)['records'][0]['issues'])

    def test_grouped_space_is_used_only_when_exchange_value_matches(self):
        page, receipt, ticker, digest = self.fixture()
        total = next(c for c in receipt['comparison']['cells'] if c['row_label'] == 'Total income')
        total.update(native_text='unreadable', ocr_text='0 102.00', status='HOLD_UNREADABLE_OR_MISSING')
        exchange = {'status':'EXCHANGE_CORROBORATION_CANDIDATE', 'document_hash':'b' * 64,
                    'source_url':'https://nsearchives.nseindia.com/report.html',
                    'metadata':{'ticker':'EXAMPLE','basis':'STANDALONE','period_end':'30-06-2026'},
                    'values_inr_lakh':{'total_income':['102.00']}}
        record = build_record_candidates(page, receipt, ticker, digest, exchange)['records'][0]
        self.assertEqual(record['values_inr_crore']['total_income'], '102.00')
        total['ocr_text'] = '0 103.00'
        self.assertEqual(build_record_candidates(page, receipt, ticker, digest, exchange)['records'][0]['status'], 'HOLD')

    def test_duplicate_metric_does_not_pick_first(self):
        args = self.fixture()
        cells = args[1]['comparison']['cells']
        cells.append(dict(cells[0]))
        self.assertEqual(build_record_candidates(*args)['held_count'], 1)

    def test_disagreement_rechecked_despite_status(self):
        args = self.fixture()
        args[1]['comparison']['cells'][0]['ocr_text'] = '101'
        self.assertEqual(build_record_candidates(*args)['held_count'], 1)

    def test_income_total_mismatch_held(self):
        args = self.fixture()
        args[1]['comparison']['cells'][2].update(native_text='103', ocr_text='103')
        record = build_record_candidates(*args)['records'][0]
        self.assertEqual(record['income_check'], 'FAIL')

    def test_held_header_never_creates_record(self):
        args = self.fixture()
        args[1]['header_binding']['tables'][0]['columns'][0]['resolution']['status'] = 'HOLD'
        self.assertEqual(build_record_candidates(*args)['records'], [])

    def test_owner_profit_and_pretax_not_total_pat(self):
        for label in ('Profit attributable to owners', 'Net profit before tax', 'Segment profit'):
            self.assertIsNone(metric_for_label(label))

    def test_expense_and_profit_rows_are_explicitly_mapped(self):
        expected = {'Cost of raw materials and packing materials consumed':'raw_materials',
                    'Purchases of traded goods':'traded_goods_purchases',
                    'Changes in inventories of finished goods':'inventory_change',
                    'Employee benefits expense':'employee_benefits', 'Finance costs':'finance_costs',
                    'Depreciation and amortisation expense':'depreciation_amortisation',
                    'Freight and distribution expense':'freight_distribution', 'Other expenses':'other_expenses',
                    'Total expenses':'total_expenses',
                    'Profit before exceptional items and tax (3+4)':'pbt_before_exceptional',
                    'Profit before tax (5+6)':'profit_before_tax'}
        for label, metric in expected.items():
            with self.subTest(label=label): self.assertEqual(metric_for_label(label), metric)

    def test_common_issuer_profit_and_material_labels_are_mapped(self):
        self.assertEqual(metric_for_label('7 Profit for the period/year (5-6)'), 'pat')
        self.assertEqual(metric_for_label('(a) Cost of materials consumed'), 'raw_materials')

    def test_unique_eight_line_expense_sum_recovers_disagreements(self):
        page,receipt,ticker,digest=self.fixture()
        labels=[('Cost of raw materials','40'),('Purchases of traded goods','30'),
                ('Changes in inventories','(5)'),('Employee benefits expense','10'),('Finance costs','2'),
                ('Depreciation and amortisation expense','3'),('Freight and distribution expense','4'),
                ('Other expenses','6 00'),('Total expenses','90')]
        for label,value in labels:
            receipt['comparison']['cells'].append({'pdf_page':1,'column_index':0,'row_label':label,
                'native_text':value,'ocr_text':value if value!='6 00' else 'bad',
                'status':'READINGS_AGREE_PENDING_REVIEW' if value!='6 00' else 'HOLD_UNREADABLE_OR_MISSING'})
        result=build_record_candidates(page,receipt,ticker,digest)['records'][0]
        self.assertEqual(result['values_inr_crore']['other_expenses'],'6.00')
        self.assertEqual(result['source_column']['cells']['other_expenses']['source_reading']['status'],
                         'EXPENSE_SUM_TRIANGULATED_PENDING_REVIEW')

    def test_non_reconciling_expense_options_remain_supplemental_hold(self):
        page,receipt,ticker,digest=self.fixture()
        labels=[('Cost of raw materials','40'),('Purchases of traded goods','30'),
                ('Changes in inventories','(5)'),('Employee benefits expense','10'),('Finance costs','2'),
                ('Depreciation and amortisation expense','3'),('Freight and distribution expense','4'),
                ('Other expenses','7 00'),('Total expenses','84')]
        for label,value in labels:
            receipt['comparison']['cells'].append({'pdf_page':1,'column_index':0,'row_label':label,
                'native_text':value,'ocr_text':value if value!='7 00' else 'bad',
                'status':'READINGS_AGREE_PENDING_REVIEW' if value!='7 00' else 'HOLD_UNREADABLE_OR_MISSING'})
        result=build_record_candidates(page,receipt,ticker,digest)['records'][0]
        self.assertNotIn('other_expenses',result['values_inr_crore'])
        self.assertIn('UNRESOLVED_CELL:other_expenses',result['source_column']['supplemental_issues'])
