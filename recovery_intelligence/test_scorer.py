import unittest
from recovery_intelligence.scorer import eligible_evidence, assess

CUTOFF = "2024-03-31T15:30:00+05:30"
def ev(date, mechanism="orders", verified=True):
    return {"published_at": date, "mechanism": mechanism,
            "source_url": "https://www.nseindia.com/example",
            "independently_verified": verified}
SCORES = dict(causal=5, trend=4, earnings_leverage=4, cash_balance=4, valuation=4, recognition_gap=3)

class RecoveryTests(unittest.TestCase):
    def test_future_document_excluded(self):
        rows=[ev("2024-04-01T09:00:00+05:30"), ev("2024-03-29T18:00:00+05:30")]
        self.assertEqual(len(eligible_evidence(rows, CUTOFF)),1)
    def test_false_verification_excluded(self):
        self.assertEqual(eligible_evidence([ev("2024-03-25T09:00:00+05:30",verified=False)],CUTOFF),[])
    def test_no_score_if_missing(self):
        s=dict(SCORES); s["cash_balance"]=None
        out=assess(s,[ev("2024-03-25T10:00:00+05:30"),ev("2024-03-26T10:00:00+05:30","collections")],CUTOFF)
        self.assertIsNone(out["score"])
    def test_fatal_flag_blocks(self):
        out=assess(SCORES,[ev("2024-03-25T10:00:00+05:30"),ev("2024-03-26T10:00:00+05:30","collections")],CUTOFF,["opaque_dilution"])
        self.assertEqual(out["research_status"],"BLOCKED_RISK")
        self.assertEqual(out["capital_deployment_inr"],0)
    def test_one_mechanism_insufficient(self):
        out=assess(SCORES,[ev("2024-03-25T10:00:00+05:30"),ev("2024-03-26T10:00:00+05:30")],CUTOFF)
        self.assertEqual(out["research_status"],"INSUFFICIENT_DATA")
    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            eligible_evidence([ev("2024-03-30T10:00:00")],CUTOFF)

if __name__=="__main__":
    unittest.main()
