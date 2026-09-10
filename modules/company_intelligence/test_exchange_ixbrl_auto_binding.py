import unittest
from modules.company_intelligence.exchange_ixbrl_auto_binding import assess_automatic_column_binding,apply_automatic_column_binding

def candidate(columns=1, contexts=None):
    values={name:[str(base+i) for i in range(columns)] for name,base in {'revenue':100,'other_income':2,'total_income':102,'raw_materials':40,'total_expenses':90,'profit_before_tax':12,'pat':10}.items()}
    result={'schema_version':1,'source_url':'https://nsearchives.nseindia.com/x.html','document_hash':'a'*64,'source_authority':'NSE_OFFICIAL_IXBRL','metadata':{'ticker':'TEST','company':'Test Limited','period_start':'01-04-2026','period_end':'30-06-2026','basis':'Standalone'},'values_inr_lakh':values,'status':'EXCHANGE_CORROBORATION_CANDIDATE','creates_approved_facts':False,'requires_meta_review':True,'requires_human_review':True}
    if contexts is not None:result['column_contexts']=contexts
    return result

class ExchangeIxbrlAutoBindingTests(unittest.TestCase):
    def test_single_column_is_automatically_bound_but_remains_provisional(self):
        item=candidate(); assessment=assess_automatic_column_binding(item)
        self.assertEqual(assessment['status'],'AUTO_BOUND_PROVISIONAL');self.assertFalse(assessment['requires_human_review'])
        bound=apply_automatic_column_binding(item,assessment)
        self.assertEqual(bound['values_inr_lakh']['revenue'],['100']);self.assertEqual(bound['column_binding']['validation_status'],'PROVISIONAL')
    def test_unique_explicit_period_and_basis_match_is_automatic(self):
        contexts=[{'period_start':'01-04-2025','period_end':'30-06-2025','basis':'Standalone'},{'period_start':'01-04-2026','period_end':'30-06-2026','basis':'Standalone'}]
        assessment=assess_automatic_column_binding(candidate(2,contexts))
        self.assertEqual(assessment['selected_column'],1);self.assertEqual(assessment['status'],'AUTO_BOUND_PROVISIONAL')
    def test_ambiguous_missing_and_conflicting_context_route_to_human(self):
        exact={'period_start':'01-04-2026','period_end':'30-06-2026','basis':'Standalone'}
        for item in (candidate(2),candidate(2,[exact,exact]),candidate(2,[{'period_start':'x'}, {'period_start':'y'}]),candidate(2,[exact])):
            with self.subTest(item=item):
                assessment=assess_automatic_column_binding(item)
                self.assertEqual(assessment['status'],'NEEDS_HUMAN_COLUMN_REVIEW');self.assertTrue(assessment['requires_human_review'])
                with self.assertRaises(ValueError):apply_automatic_column_binding(item,assessment)
    def test_changed_candidate_invalidates_saved_assessment(self):
        item=candidate(); assessment=assess_automatic_column_binding(item);item['values_inr_lakh']['revenue'][0]='999'
        with self.assertRaisesRegex(ValueError,'current'):apply_automatic_column_binding(item,assessment)

if __name__=='__main__':unittest.main()
