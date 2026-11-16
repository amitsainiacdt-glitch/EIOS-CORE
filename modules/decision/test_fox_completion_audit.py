"""Synthetic FOX completion auditing regressions; no market feed."""
import unittest
from modules.decision.fox_completion_audit import Case, audit
class Tests(unittest.TestCase):
    def case(self, **kw):
        data=dict(ticker="ABC",discovered="2026-10-28",last_review="2026-11-10",
                  decision="UNDERWRITING_INCOMPLETE",owner="research",missing_facts=("cash bridge",),
                  next_event="quarterly disclosure",due="2026-11-12",valuation_complete=False,
                  evidence_urls=("https://nseindia.com/filing",),portfolio=True)
        data.update(kw)
        return Case(**data)
    def test_stale_is_counted(self):
        r=audit((self.case(),),"2026-11-16")
        self.assertEqual((r["stale_7"],r["stale_14"],r["incomplete"]),(1,1,1))
        self.assertTrue(r["cases"][0]["overdue"])
        self.assertEqual(r["capital_deployment_rupees"],0)
    def test_open_age_differs_from_unreviewed_age(self):
        r=audit((self.case(last_review="2026-11-15",due="2026-11-20"),),"2026-11-16")
        self.assertEqual(r["stale_14"],1)
        self.assertEqual(r["unreviewed_7"],0)
        self.assertEqual(r["cases"][0]["days_unreviewed"],1)
    def test_overdue_but_recently_reviewed(self):
        r=audit((self.case(last_review="2026-11-15"),),"2026-11-16")
        self.assertTrue(r["cases"][0]["overdue"])
        self.assertFalse(r["cases"][0]["unreviewed_7"])
    def test_missing_completion_fields(self):
        r=audit((self.case(owner="",missing_facts=(),next_event="",due="",evidence_urls=()),),"2026-11-16")
        self.assertEqual(len(r["cases"][0]["missing"]),5)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): audit((self.case(),self.case()),"2026-11-16")
    def test_closed_without_valuation_flagged(self):
        r=audit((self.case(decision="RESEARCH_ADD"),),"2026-11-16")
        self.assertIn("closed without valuation",r["cases"][0]["missing"])
if __name__=="__main__": unittest.main()
