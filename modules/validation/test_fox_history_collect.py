"""FOX raw-history batching: synthetic fixtures, never financial validation."""
import io,tempfile,unittest,zipfile,re
from modules.validation.fox_history_collect import collect_history

def fixture(url):
    v=re.search(r"(20\d{6})",url).group(1)
    d=f"{v[:4]}-{v[4:6]}-{v[6:]}"
    h="TckrSymb,SctySrs,TradDt,OpnPric,ClsPric,ISIN\n"
    rows="".join(f"SYM{i},EQ,{d},100,101,INE{i:09d}\n" for i in range(110))
    rows+=f"ANUP,EQ,{d},120,122,INE294Z01018\n"
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w") as f:f.writestr("bhav.csv",h+rows)
    return z.getvalue()

class HistoryTests(unittest.TestCase):
    def test_eight_dates_creates_two_batches(self):
        ds=[f"2024-10-{x:02d}" for x in range(21,29)]
        with tempfile.TemporaryDirectory() as td:
            r=collect_history(ds,td,fetch=fixture)
            self.assertEqual(r["status"],"RAW_COMPLETE")
            self.assertEqual(r["raw_rows"],8)
            self.assertFalse(r["historical_returns_admissible"])
            self.assertEqual(r["coverage"]["ANUP"]["sessions"],8)
    def test_malformed_missing_date_no_invented_bar(self):
        ds=["2024-10-28","2024-10-29"]
        def fail_one(url):
            if "20241029" in url:raise FileNotFoundError("Not on archive")
            return fixture(url)
        with tempfile.TemporaryDirectory() as td:
            r=collect_history(ds,td,fetch=fail_one)
            self.assertEqual(r["status"],"RAW_INCOMPLETE")
            self.assertEqual(r["raw_rows"],1)
            self.assertEqual(len(r["verified_archive_sessions"]),1)
    def test_duplicate_date_rejected(self):
        with self.assertRaises(ValueError):
            collect_history(["2024-10-28","2024-10-28"],"/tmp/unused",fetch=fixture)
    def test_unsorted_dates_rejected(self):
        with self.assertRaises(ValueError):
            collect_history(["2024-10-29","2024-10-28"],"/tmp/unused",fetch=fixture)
    def test_no_dates_rejected(self):
        with self.assertRaises(ValueError):
            collect_history([],"/tmp/unused",fetch=fixture)

if __name__=="__main__":unittest.main()
