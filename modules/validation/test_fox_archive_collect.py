"""Synthetic fixture checks: never claim official price validation from test data."""
import io,tempfile,unittest,zipfile
from datetime import date
from pathlib import Path
from modules.validation.fox_archive_collect import udiff_url,download,validate_archive

def fixture(d=date(2024,10,30),rows=110):
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        data="TradDt,TckrSymb,SctySrs,OpnPric,ClsPric\n"+"".join(f"{d.isoformat()},SYM{i},EQ,100,101\n" for i in range(rows))
        z.writestr("bhav.csv",data)
    return b.getvalue()

class FOXArchiveTests(unittest.TestCase):
    def test_nse_archive_path(self):self.assertIn("20241030",udiff_url(date(2024,10,30)))
    def test_legacy_format_is_not_udiff(self):
        with self.assertRaises(ValueError):udiff_url(date(2023,10,30))
    def test_valid_zip(self):self.assertEqual(validate_archive(fixture(),date(2024,10,30))["eq_rows"],110)
    def test_day_mismatch(self):
        with self.assertRaises(ValueError):validate_archive(fixture(),date(2024,10,31))
    def test_missing_rows(self):
        with self.assertRaises(ValueError):validate_archive(fixture(rows=4),date(2024,10,30))
    def test_manifest_never_certifies_adjustment(self):
        with tempfile.TemporaryDirectory() as td:
            meta=download(date(2024,10,30),Path(td),tries=1,fetch=lambda _:fixture())
            self.assertFalse(meta["corporate_actions_adjusted"])
            self.assertFalse(meta["research_backtest_admissible"])
            self.assertTrue((Path(td)/"archive_manifest.json").exists())
    def test_transport_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(RuntimeError):
                download(date(2024,10,30),Path(td),tries=1,fetch=lambda _:(_ for _ in ()).throw(ConnectionError("blocked")))
            self.assertFalse((Path(td)/"archive_manifest.json").exists())
if __name__=="__main__":unittest.main()
