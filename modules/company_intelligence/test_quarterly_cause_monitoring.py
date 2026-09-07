import unittest
from modules.company_intelligence.quarterly_cause_monitoring import build_quarterly_cause_monitoring, evaluate_direction


RULE = {'id':'r1','indicator':'Input price','family':'COMMODITY_INPUT','unit':'USD/t',
        'favourable_direction':'DOWN','source_requirement':'Primary source','source_domain':'example.gov.in','cadence':'Quarterly',
        'improvement_meaning':'Lower cost pressure','deterioration_meaning':'Higher cost pressure'}


class CauseMonitoringTests(unittest.TestCase):
    def test_builds_rules_without_creating_catalyst(self):
        packet={'items':[{'id':'c1','cause':'cost','effect':'PRESSURE','monitoring_rules':[RULE]}]}
        result=build_quarterly_cause_monitoring(packet)
        self.assertEqual('MONITORING_PLAN_READY',result['status'])
        self.assertFalse(result['creates_catalyst'])
        self.assertEqual('AWAITING_NEW_OBSERVATION',result['rules'][0]['latest_signal'])

    def test_evaluates_direction_but_not_verdict(self):
        result=evaluate_direction(RULE,previous='1700',current='1500')
        self.assertEqual('FAVOURABLE_DIRECTION',result['status'])
        self.assertFalse(result['changes_verdict'])

    def test_invalid_number_is_rejected(self):
        with self.assertRaises(ValueError): evaluate_direction(RULE,previous='1700',current='nan')


if __name__ == '__main__': unittest.main()
