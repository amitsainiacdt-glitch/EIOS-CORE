import unittest
from modules.company_intelligence.quarterly_plain_english import explain_quarterly_financials


def assessment(**figures):
    values={'revenue':'100','other_income':'5','total_income':'105','pat':'10','total_expenses':'90',
            'pbt_before_exceptional':'15','employee_benefits':'8','freight_distribution':'4'}; values.update(figures)
    return {'technical_checks_passed':True,'figures_for_review_inr_crore':values,'not_checked':['Cash flow']}


class QuarterlyPlainEnglishTests(unittest.TestCase):
    def test_single_period_does_not_invent_a_trend(self):
        result=explain_quarterly_financials(assessment())
        self.assertEqual(result['posture'],'SINGLE_PERIOD_CONTEXT_ONLY')
        self.assertIn('not a trend',result['summary'])
        self.assertIn('10.00%',result['headline'])

    def test_growth_and_margin_are_explained_from_comparable_figures(self):
        result=explain_quarterly_financials(assessment(), prior_comparable={'revenue':'80','pat':'6','other_income':'4',
            'total_expenses':'70','pbt_before_exceptional':'14','employee_benefits':'7','freight_distribution':'3'})
        self.assertEqual(result['posture'],'COMPARATIVE_CONTEXT_AVAILABLE')
        self.assertIn('profit growing faster',result['summary'])
        self.assertTrue(any('percentage points' in text for text in result['figure_explanations']))
        self.assertEqual(result['profit_bridge']['revenue_change_crore'],'20.00')
        self.assertEqual(result['profit_bridge']['pat_at_prior_margin_crore'],'7.50')
        self.assertEqual(result['profit_bridge']['profit_gap_vs_prior_margin_crore'],'2.50')
        self.assertEqual(result['profit_bridge']['other_income_change_crore'],'1.00')
        self.assertEqual(result['cost_attribution']['total_expense_change_crore'],'20.00')
        self.assertEqual(result['cost_attribution']['unallocated_expense_change_crore'],'18.00')
        self.assertEqual(len(result['cost_attribution']['comparable_lines']),2)
        self.assertEqual(result['cost_attribution']['dominant_pressures'][0]['label'],'Employee benefits')

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
