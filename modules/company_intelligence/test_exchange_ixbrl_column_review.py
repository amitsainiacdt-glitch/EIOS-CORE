from datetime import datetime,timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from modules.company_intelligence.exchange_ixbrl_financial import parse_exchange_ixbrl_financial
from modules.company_intelligence.exchange_ixbrl_column_review import ExchangeIxbrlColumnReviewLedger,prepare_column_review,apply_column_review

class ExchangeIxbrlColumnReviewTests(unittest.TestCase):
    def candidate(self):
        labels={'NSE Symbol':('TEST',),'ISIN':('INE000000001',),'Name of company':('Test Limited',),'Description of presentation currency':('INR',),'Level of rounding used in financial results':('Lakhs',),'Reporting Type':('Quarterly',),'Reporting Quarter':('First quarter',),'Nature of report standalone or consolidated':('Standalone',),'Date of start of reporting period':('01-04-2026',),'Date of end of reporting period':('30-06-2026',),'Revenue from operations':('100.25','90'),'Other income':('2','1'),'Total income':('102.25','91'),'Cost of materials consumed':('40','35'),'Total expenses':('90','80'),'Total profit before tax':('12.25','11'),'Total profit (loss) for period':('10','9')}
        html='<table>'+''.join('<tr><td>'+key+'</td>'+''.join(f'<td>{value}</td>' for value in values)+'</tr>' for key,values in labels.items())+'</table>'
        return parse_exchange_ixbrl_financial(html,source_url='https://nsearchives.nseindia.com/x.html',document_hash='a'*64)
    def test_preview_keeps_all_columns_and_never_approves(self):
        preview=prepare_column_review(self.candidate())
        self.assertEqual(preview['column_count'],2);self.assertFalse(preview['creates_approved_facts'])
    def test_persisted_selection_binds_one_column(self):
        with TemporaryDirectory() as directory:
            candidate=self.candidate(); ledger=ExchangeIxbrlColumnReviewLedger(Path(directory)/'review.jsonl')
            review=ledger.record(candidate,review_id='R1',decision='SELECT',selected_column=1,reviewer='Human',rationale='Matched period header.',reviewed_at=datetime.now(timezone.utc))
            bound=apply_column_review(candidate,review)
            self.assertEqual(bound['values_inr_lakh']['revenue'],['90'])
            self.assertEqual(ledger.read_all(),(review,))
    def test_hold_tamper_and_out_of_range_fail_closed(self):
        with TemporaryDirectory() as directory:
            candidate=self.candidate(); ledger=ExchangeIxbrlColumnReviewLedger(Path(directory)/'review.jsonl'); now=datetime.now(timezone.utc)
            with self.assertRaisesRegex(ValueError,'outside'): ledger.record(candidate,review_id='R',decision='SELECT',selected_column=2,reviewer='H',rationale='x',reviewed_at=now)
            review=ledger.record(candidate,review_id='R',decision='HOLD',selected_column=None,reviewer='H',rationale='Header unclear.',reviewed_at=now)
            with self.assertRaisesRegex(ValueError,'not selected'): apply_column_review(candidate,review)
            path=Path(directory)/'review.jsonl'; path.write_text(path.read_text().replace('Header unclear.','Changed'))
            with self.assertRaisesRegex(ValueError,'fingerprint'): ledger.read_all()

if __name__=='__main__':unittest.main()
