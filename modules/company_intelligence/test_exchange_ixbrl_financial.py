import unittest
from modules.company_intelligence.exchange_ixbrl_financial import parse_exchange_ixbrl_financial


class ExchangeIxbrlFinancialTests(unittest.TestCase):
    def html(self, *, currency="INR", revenue="100.25"):
        rows = [
            ("NSE Symbol", "TEST"), ("ISIN", "INE000000001"), ("Name of company", "Test Limited"),
            ("Description of presentation currency", currency),
            ("Level of rounding used in financial results", "Lakhs"),
            ("Reporting Type", "Quarterly"), ("Reporting Quarter", "First quarter"),
            ("Nature of report standalone or consolidated", "Standalone"),
            ("A", "Date of start of reporting period", "01-04-2026", "01-04-2026"),
            ("B", "Date of end of reporting period", "30-06-2026", "30-06-2026"),
            ("Revenue from operations", revenue, revenue), ("Other income", "2", "2"),
            ("Total income", "102.25", "102.25"), ("Cost of materials consumed", "40", "40"),
            ("Total expenses", "90", "90"), ("Total profit before tax", "12.25", "12.25"),
            ("Total profit (loss) for period", "10", "10"),
        ]
        return "<table>" + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>" for row in rows) + "</table>"

    def parse(self, html=None, url="https://nsearchives.nseindia.com/corporate/ixbrl/report.html"):
        return parse_exchange_ixbrl_financial(html or self.html(), source_url=url, document_hash="a" * 64)

    def test_extracts_source_bound_metadata_and_metrics_without_approval(self):
        result = self.parse()
        self.assertEqual(result["metadata"]["currency"], "INR")
        self.assertEqual(result["metadata"]["period_end"], "30-06-2026")
        self.assertEqual(result["values_inr_lakh"]["revenue"], ["100.25", "100.25"])
        self.assertFalse(result["creates_approved_facts"])

    def test_parenthesized_amount_is_negative(self):
        self.assertEqual(self.parse(self.html(revenue="(100.25)"))["values_inr_lakh"]["revenue"], ["-100.25", "-100.25"])

    def test_wrong_domain_and_currency_fail_closed(self):
        with self.assertRaises(ValueError):
            self.parse(url="https://nseindia.example/report.html")
        with self.assertRaises(ValueError):
            self.parse(self.html(currency="USD"))

    def test_conflicting_identity_fails_closed(self):
        with self.assertRaises(ValueError):
            self.parse(self.html() + "<table><tr><td>NSE Symbol</td><td>OTHER</td></tr></table>")
