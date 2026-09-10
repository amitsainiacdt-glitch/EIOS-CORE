import unittest
from modules.company_intelligence.quarterly_exchange_match import select_exchange_corroboration

def report(period='30-06-2026',basis='Standalone'):
    return {'status':'EXCHANGE_CORROBORATION_CANDIDATE','metadata':{'ticker':'TEST','period_end':period,'basis':basis}}
def page():
    return {'statement_context':{'basis_candidates':['STANDALONE'],'current_quarter_end_text':'June 30, 2026'},'ruled_tables':[]}

class QuarterlyExchangeMatchTests(unittest.TestCase):
    def test_exact_identity_period_and_basis_selects_one(self):
        target=report();self.assertIs(select_exchange_corroboration(page(),[report('30-06-2025'),target],ticker='TEST'),target)
    def test_mismatch_returns_none_and_duplicates_fail(self):
        self.assertIsNone(select_exchange_corroboration(page(),[report(basis='Consolidated')],ticker='TEST'))
        with self.assertRaisesRegex(ValueError,'multiple'):select_exchange_corroboration(page(),[report(),report()],ticker='TEST')
    def test_missing_unambiguous_pdf_basis_does_not_guess(self):
        item=page();item['statement_context']['basis_candidates']=[]
        self.assertIsNone(select_exchange_corroboration(item,[report()],ticker='TEST'))

if __name__=='__main__':unittest.main()
