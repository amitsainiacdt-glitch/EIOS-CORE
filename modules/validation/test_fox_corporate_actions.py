"""FOX corporate-action mechanics tests. Synthetic fixtures, not certified market data."""
import unittest
from dataclasses import replace
from modules.validation.fox_corporate_actions import (
    ObservedBar, CapitalEvent, ReviewAttestation, adjust_history,
)

SHA="a"*64
def bar(day,close,isin="INE945H01013",series="BE"):
    return ObservedBar("V2RETAIL",isin,series,day,close,close,SHA)
def reviewed(**kw):
    x=ReviewAttestation("V2RETAIL","2026-03-24","2026-03-26","2026-03-26",
                         corporate_actions_complete=True,distributions_reviewed=True,
                         rights_and_demergers_reviewed=True,
                         symbol_isin_history_reviewed=True,series_liquidity_reviewed=True,
                         primary_filing_timestamps_reviewed=True,reviewer_reference="independently-reviewed-evidence")
    return replace(x,**kw)
def event(**kw):
    x=CapitalEvent("V2RETAIL","2026-03-25","INE945H01013","INE945H01021",
                   "SPLIT",10,"https://nsearchives.nseindia.com/content/circulars/CML73355.pdf",
                   "2026-03-20T10:00:00+05:30",True)
    return replace(x,**kw)
def bars():
    return [bar("2026-03-24",1000),
            bar("2026-03-25",100,"INE945H01021"),
            bar("2026-03-26",110,"INE945H01021")]

class CorporateActionsTests(unittest.TestCase):
    def test_verified_split_10_to_1(self):
        x=adjust_history(bars(),[event()],reviewed())
        self.assertTrue(x.backtest_admissible)
        self.assertEqual([z.adjusted_close for z in x.adjusted_bars],[100,100,110])
        self.assertTrue(all(z.verified_adjusted for z in x.adjusted_bars))
    def test_no_attestation_blocks(self):
        x=adjust_history(bars(),[event()],reviewed(corporate_actions_complete=False))
        self.assertFalse(x.backtest_admissible)
        self.assertTrue(all(not z.verified_adjusted for z in x.adjusted_bars))
    def test_nonverified_event_blocks(self):
        x=adjust_history(bars(),[event(reviewer_confirmed=False)],reviewed())
        self.assertFalse(x.backtest_admissible)
    def test_unexplained_isin_change_blocks(self):
        x=adjust_history(bars(),[],reviewed())
        self.assertFalse(x.backtest_admissible)
        self.assertIn("Unexplained ISIN transition",x.blockers)
    def test_irrelevant_bonus_not_in_range_blocks(self):
        x=adjust_history(bars(),[event(effective_trade_date="2024-04-23")],reviewed())
        self.assertFalse(x.backtest_admissible)
    def test_incomplete_dividend_review_blocks(self):
        x=adjust_history(bars(),[event()],reviewed(distributions_reviewed=False))
        self.assertFalse(x.backtest_admissible)
    def test_mixed_series_blocks(self):
        v=bars()
        v[2]=replace(v[2],series="EQ")
        x=adjust_history(v,[event()],reviewed())
        self.assertFalse(x.backtest_admissible)
    def test_duplicate_date_blocks(self):
        v=bars()+[bars()[-1]]
        x=adjust_history(v,[event()],reviewed())
        self.assertFalse(x.backtest_admissible)
    def test_no_raw_bars(self):
        x=adjust_history([],[],reviewed())
        self.assertFalse(x.backtest_admissible)
    def test_no_unreviewed_history_claim(self):
        x=adjust_history(bars(),[event()],reviewed(primary_filing_timestamps_reviewed=False))
        self.assertFalse(x.backtest_admissible)
    def test_only_event_beyond_anchor_does_not_adjust_history(self):
        x=adjust_history([bar("2026-03-24",1000),bar("2026-03-25",100,"INE945H01021"),
                          bar("2026-03-26",110,"INE945H01021")],
                         [event()],reviewed(reference_session="2026-03-24"))
        self.assertTrue(x.backtest_admissible)
        self.assertEqual([z.adjusted_close for z in x.adjusted_bars],[1000,1000,1100])
    def test_reject_incomplete_checksum(self):
        v=bars()
        v[0]=replace(v[0],source_sha256="not-a-hash")
        self.assertFalse(adjust_history(v,[event()],reviewed()).backtest_admissible)

if __name__=="__main__":unittest.main()
