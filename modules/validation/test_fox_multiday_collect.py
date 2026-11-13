"""Synthetic multi-date fixture tests; data never certified adjusted."""
import io,tempfile,unittest,zipfile
from datetime import date
from pathlib import Path
from modules.validation.fox_multiday_collect import collect

def fixture(url):
    import re
    ds=re.search(r"(20\d{6})",url).group(1)
    d=f"{ds[:4]}-{ds[4:6]}-{ds[6:]}"
    fields="TckrSymb,SctySrs,TradDt,OpnPric,ClsPric,ISIN\n"
    rows="".join(f"SYM{i},EQ,{d},100,101,INE{i:09d}\n" for i in range(110))
    rows+=f"ANUP,EQ,{d},120,121,INE294Z01018\n"
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w") as f:f.writestr("bhav.csv",fields+rows)
    return z.getvalue()

class MultiDayTests(unittest.TestCase):
    def test_two_day_provenance(self):
        with tempfile.TemporaryDirectory() as t:
            r=collect(["2024-10-29","2024-10-30"],t,fetch=fixture)
            self.assertEqual(len(r["collected_sessions"]),2)
            self.assertEqual(r["rows"],2)
            self.assertFalse(r["backtest_admissible"])
    def test_be_series_v2_retail_recognised(self):
        def with_be(url):
            import re
            ds=re.search(r"(20\d{6})",url).group(1)
            d=f"{ds[:4]}-{ds[4:6]}-{ds[6:]}"
            fields="TckrSymb,SctySrs,TradDt,OpnPric,ClsPric,ISIN\n"
            rows="".join(f"SYM{i},EQ,{d},100,101,INE{i:09d}\n" for i in range(110))
            rows+=f"V2RETAIL,BE,{d},123,125,INE945H01013\n"
            z=io.BytesIO()
            with zipfile.ZipFile(z,"w") as f:f.writestr("bhav.csv",fields+rows)
            return z.getvalue()
        with tempfile.TemporaryDirectory() as t:
            r=collect(["2024-10-29"],t,fetch=with_be)
            self.assertEqual(r["rows"],1)
            self.assertEqual(r["distinct_tickers"],1)
            self.assertEqual(r["non_EQ_series"],["V2RETAIL:BE"])
            self.assertNotIn("V2RETAIL",r["missing_pilot_tickers"])
            self.assertFalse(r["backtest_admissible"])
    def test_too_many_dates(self):
        with self.assertRaises(ValueError):
            collect([f"2024-10-{i:02d}" for i in range(20,28)],"/tmp/ignore",fetch=fixture)
    def test_duplicate_date(self):
        with self.assertRaises(ValueError):
            collect(["2024-10-29","2024-10-29"],"/tmp/ignore",fetch=fixture)
    def test_failed_archive_not_fabricated(self):
        with tempfile.TemporaryDirectory() as t:
            def fail(_):raise RuntimeError("unavailable")
            r=collect(["2024-10-29"],t,fetch=fail)
            self.assertEqual(len(r["failed_dates"]),1)
            self.assertEqual(r["rows"],0)
    def test_invalid_isin_header_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            def no_isin(url):
                z=io.BytesIO()
                with zipfile.ZipFile(z,"w") as f:
                    f.writestr("bhav.csv","TckrSymb,SctySrs,TradDt,OpnPric,ClsPric\n"+
                         "".join(f"SYM{i},EQ,2024-10-29,1,1\n" for i in range(110)))
                return z.getvalue()
            r=collect(["2024-10-29"],t,fetch=no_isin)
            self.assertEqual(r["rows"],0)
            self.assertTrue(r["failed_dates"])

if __name__=="__main__":unittest.main()
