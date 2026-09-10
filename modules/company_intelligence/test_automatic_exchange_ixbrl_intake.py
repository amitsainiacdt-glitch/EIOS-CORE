from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from modules.company_intelligence.automatic_exchange_ixbrl_intake import (
    is_nse_ixbrl_candidate, stage_exchange_ixbrl_candidate,
)
class AutomaticExchangeIxbrlIntakeTests(unittest.TestCase):
    @staticmethod
    def html():
        rows = [
            ("NSE Symbol", "TEST"), ("ISIN", "INE000000001"), ("Name of company", "Test Limited"),
            ("Description of presentation currency", "INR"),
            ("Level of rounding used in financial results", "Lakhs"),
            ("Reporting Type", "Quarterly"), ("Reporting Quarter", "First quarter"),
            ("Nature of report standalone or consolidated", "Standalone"),
            ("Date of start of reporting period", "01-04-2026"),
            ("Date of end of reporting period", "30-06-2026"),
            ("Revenue from operations", "100.25"), ("Other income", "2"),
            ("Total income", "102.25"), ("Cost of materials consumed", "40"),
            ("Total expenses", "90"), ("Total profit before tax", "12.25"),
            ("Total profit (loss) for period", "10"),
        ]
        return "<table>" + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>" for row in rows) + "</table>"

    def acquisition(self, body=None, url="https://nsearchives.nseindia.com/corporate/result.html"):
        body = (body or self.html()).encode()
        return SimpleNamespace(document_bytes=body, receipt=SimpleNamespace(
            source_url=url, content_type="text/html; charset=utf-8", document_hash=sha256(body).hexdigest()))

    def test_official_ixbrl_is_staged_but_not_approved(self):
        with TemporaryDirectory() as directory:
            acquisition = self.acquisition()
            self.assertTrue(is_nse_ixbrl_candidate(acquisition))
            result, path, automatic = stage_exchange_ixbrl_candidate(
                acquisition, ticker="TEST", company="Test Limited", output_root=Path(directory))
            self.assertTrue(path.is_file())
            self.assertTrue(path.with_name("exchange-ixbrl-column-review.json").is_file())
            self.assertTrue(path.with_name("exchange-ixbrl-auto-binding.json").is_file())
            self.assertTrue(path.with_name("exchange-ixbrl-bound-corroboration.json").is_file())
            self.assertEqual(result["status"], "EXCHANGE_CORROBORATION_CANDIDATE")
            self.assertFalse(result["creates_approved_facts"])
            self.assertEqual(automatic["status"], "AUTO_BOUND_PROVISIONAL")
            self.assertEqual(stage_exchange_ixbrl_candidate(
                acquisition, ticker="TEST", company="Test Limited", output_root=Path(directory))[1], path)

    def test_wrong_company_and_changed_bytes_fail_closed(self):
        with TemporaryDirectory() as directory:
            acquisition = self.acquisition()
            with self.assertRaisesRegex(ValueError, "identity"):
                stage_exchange_ixbrl_candidate(acquisition, ticker="OTHER", company="Test Limited",
                                               output_root=Path(directory))
            acquisition.document_bytes += b"changed"
            with self.assertRaisesRegex(ValueError, "receipt"):
                stage_exchange_ixbrl_candidate(acquisition, ticker="TEST", company="Test Limited",
                                               output_root=Path(directory))

    def test_lookalike_domain_is_not_eligible(self):
        self.assertFalse(is_nse_ixbrl_candidate(self.acquisition(
            url="https://nsearchives.nseindia.com.evil.example/result.html")))


if __name__ == "__main__":
    unittest.main()
