import unittest
from modules.company_intelligence.quarterly_plain_english import explain_quarterly_financials


def assessment(**figures):
    values={'revenue':'100','other_income':'5','total_income':'105','pat':'10'}; values.update(figures)
    return {'technical_checks_passed':True,'figures_for_review_inr_crore':values,'not_checked':['Cash flow']}


class QuarterlyPlainEnglishTests(unittest.TestCase):
    def test_single_period_does_not_invent_a_trend(self):
        result=explain_quarterly_financials(assessment())
        self.assertEqual(result['posture'],'SINGLE_PERIOD_CONTEXT_ONLY')
        self.assertIn('not a trend',result['summary'])
        self.assertIn('10.00%',result['headline'])

    def test_growth_and_margin_are_explained_from_comparable_figures(self):
        result=explain_quarterly_financials(assessment(), prior_comparable={'revenue':'80','pat':'6'})
        self.assertEqual(result['posture'],'COMPARATIVE_CONTEXT_AVAILABLE')
        self.assertIn('profit growing faster',result['summary'])
        self.assertTrue(any('percentage points' in text for text in result['figure_explanations']))

    def test_applies_note_is_explained_and_pending_note_is_disclosed(self):
        notes={'candidates':[{'topic':'IMPAIRMENT','human_review':{'decision':'APPLIES','rationale':'Current quarter'}},
                             {'topic':'COMPARABILITY','human_review':None}]}
        result=explain_quarterly_financials(assessment(),notes)
        self.assertIn('asset-value reduction',result['accounting_note_explanations'][0]['meaning'])
        self.assertIn('1 reporting-note',result['accounting_note_explanations'][1]['meaning'])

    def test_failed_extraction_is_not_interpreted(self):
        result=explain_quarterly_financials({'technical_checks_passed':False,'not_checked':[]})
        self.assertEqual(result['posture'],'FIGURES_WITHHELD')
        self.assertEqual(result['figure_explanations'],[])


if __name__=='__main__': unittest.main()
