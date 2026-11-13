import unittest
from modules.validation.fox_data_audit import audit

def row(**kw):
    x=dict(event_id="a",ticker="ANUP",source_url="https://nsearchives.nseindia.com/a.pdf",
           published_at_ist="2026-11-06T12:49:58+05:30",
           source_timestamp_verified="yes",evidence_cutoff_ist="2026-11-06T12:49:58+05:30",
           case_type="candidate",action="INVESTIGATE",sector="Capital Goods",
           price_adjustments_verified="yes")
    x.update(kw)
    return x

class DatasetAuditTests(unittest.TestCase):
    def test_complete_row_admissible(self):
        self.assertEqual(audit([row()]).admissible,1)
    def test_unverified_timestamp_blocked(self):
        self.assertEqual(audit([row(source_timestamp_verified="no")]).admissible,0)
    def test_unadjusted_prices_blocked(self):
        self.assertEqual(audit([row(price_adjustments_verified="no")]).admissible,0)
    def test_hindsight_blocked(self):
        self.assertEqual(audit([row(evidence_cutoff_ist="2026-11-08T12:00:00+05:30")]).admissible,0)
    def test_naive_timestamp_blocked(self):
        self.assertEqual(audit([row(published_at_ist="2026-11-06T12:49:58")]).admissible,0)
    def test_duplicates_blocked(self):
        self.assertEqual(audit([row(),row()]).admissible,1)
    def test_negative_control_counted(self):
        self.assertEqual(audit([row(case_type="negative_control")]).counts_by_type["negative_control"],1)
    def test_no_100_case_claim_with_one_event(self):
        self.assertFalse(audit([row()]).minimum_100_met)
    def test_100_verified_rows_required(self):
        rows=[row(event_id=f"a{i}") for i in range(100)]
        self.assertTrue(audit(rows).minimum_100_met)
        rows[0]["price_adjustments_verified"]="no"
        self.assertFalse(audit(rows).minimum_100_met)
if __name__=="__main__": unittest.main()
