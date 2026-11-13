import unittest
from modules.validation.fox_history_quality import check_raw_continuity

def row(day,isin="INE294Z01018",series="EQ"):
    return {"ticker":"ANUP","session":day,"isin":isin,"series":series}

class HistoryQualityTests(unittest.TestCase):
    def test_continuous_raw_still_not_backtest_ready(self):
        x=check_raw_continuity([row("2024-10-28"),row("2024-10-29")],["2024-10-28","2024-10-29"],"ANUP")
        self.assertEqual(x.status,"RAW_CONTINUOUS_UNADJUSTED")
        self.assertFalse(x.backtest_admissible)
    def test_missing_session_flagged(self):
        x=check_raw_continuity([row("2024-10-28")],["2024-10-28","2024-10-29"],"ANUP")
        self.assertEqual(x.missing_ticker_sessions,("2024-10-29",))
    def test_identifier_change_flagged(self):
        x=check_raw_continuity([row("2024-10-28"),row("2024-10-29","INE294Z01026")],["2024-10-28","2024-10-29"],"ANUP")
        self.assertEqual(x.status,"NEEDS_LINEAGE_AND_LIQUIDITY_REVIEW")
    def test_series_change_flagged(self):
        x=check_raw_continuity([row("2024-10-28"),row("2024-10-29",series="BE")],["2024-10-28","2024-10-29"],"ANUP")
        self.assertTrue(x.series_changes)
    def test_duplicates_flagged(self):
        x=check_raw_continuity([row("2024-10-28"),row("2024-10-28")],["2024-10-28"],"ANUP")
        self.assertEqual(x.status,"INCOMPLETE")
    def test_unsorted_expected_days_fail(self):
        with self.assertRaises(ValueError):
            check_raw_continuity([],["2024-10-29","2024-10-28"],"ANUP")

if __name__=="__main__":
    unittest.main()
