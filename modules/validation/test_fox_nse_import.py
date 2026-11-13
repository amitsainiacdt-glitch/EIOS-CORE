import csv,io,unittest,zipfile
from modules.validation.fox_nse_import import parse_udiff_zip,certify_adjusted

def archive():
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        z.writestr("udiff.csv","TckrSymb,SctySrs,TradDt,OpnPric,ClsPric\nANUP,EQ,2026-11-06,1200,1260\nANUP,BE,2026-11-06,1000,1010\n")
    return b.getvalue()
URL="https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_20261106_F_0000.csv.zip"
class ImportTests(unittest.TestCase):
    def test_raw_archive_never_marked_adjusted(self):
        a=parse_udiff_zip(archive(),URL,tickers=["ANUP"])
        self.assertEqual(len(a),1)
        self.assertFalse(a[0].verified_adjusted)
        self.assertEqual(a[0].close,1260)
    def test_untrusted_source_rejected(self):
        with self.assertRaises(ValueError):parse_udiff_zip(archive(),"https://example.com/data.zip")
    def test_missing_adjustment_review_cannot_certify(self):
        a=parse_udiff_zip(archive(),URL)
        self.assertEqual(certify_adjusted(a,{},[]),{})
    def test_explicit_review_and_factor_required(self):
        a=parse_udiff_zip(archive(),URL)
        v=certify_adjusted(a,{("ANUP","2026-11-06"):0.5},["ANUP"])
        self.assertEqual(v["ANUP"][0].close,630)
        self.assertTrue(v["ANUP"][0].verified_adjusted)
    def test_malformed_schema_rejected(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w") as z:z.writestr("x.csv","SYMBOL,OPEN,CLOSE\nANUP,1,2\n")
        with self.assertRaises(ValueError):parse_udiff_zip(b.getvalue(),URL)
if __name__=="__main__":unittest.main()
