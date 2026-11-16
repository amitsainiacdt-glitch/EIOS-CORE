"""Bridge smoke tests: evidence-first FOX is callable through DecisionOffice."""
import unittest
from modules.decision.decision_office import DecisionOffice
from modules.decision.test_fox_add_engine import case
from modules.decision.fox_add_engine import FoxAction
from modules.decision.fox_completion_audit import Case

class BridgeTests(unittest.TestCase):
    def test_explicit_fox_underwriting_path_is_reachable(self):
        r=DecisionOffice().evaluate_fox_research(case(research_zone=None))
        self.assertEqual(r.action,FoxAction.EIP_ADD)
        self.assertEqual(r.capital_deployment_rupees,0)
    def test_completion_queue_from_decision_office(self):
        c=Case("ABC","2026-11-01","2026-11-10","UNDERWRITING_INCOMPLETE",
               "FOX analyst",("cash flow",),"2026-11-18 filing","2026-11-17",False,
               ("https://nsearchives.nseindia.com/example.pdf",))
        v=DecisionOffice().audit_fox_research_queue((c,),"2026-11-16")
        self.assertEqual(v["incomplete"],1)
        self.assertEqual(v["stale_14"],1)
        self.assertEqual(v["capital_deployment_rupees"],0)
if __name__=="__main__":unittest.main()
