import unittest

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.official_linked_asset_discovery import discover_official_linked_assets


class OfficialLinkedAssetDiscoveryTests(unittest.TestCase):
    def page(self, content, url='https://mausam.imd.gov.in/responsive/rainfall_statistics.php?PAGE=8'):
        return RetrievedContent(url, 200, content, 'text/html; charset=UTF-8', {})

    def test_selects_relevant_same_domain_pdf_and_images_with_parent_provenance(self):
        assets = discover_official_linked_assets(self.page(
            '<a href="../Rainfall/SUBDIVISION_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf#page=1">PDF</a>'
            '<img src="../Rainfall/tmpg/rainfall-0.png"><img src="../Rainfall/tmpg/rainfall-0.png">'
            '<a href="https://evil.example/rainfall.pdf">bad</a><img src="/img/logo.png">'),
            approved_domain='mausam.imd.gov.in', relevance_terms=('rainfall', 'country_india'))
        self.assertEqual(2, len(assets))
        self.assertEqual('PDF', assets[0].asset_type)
        self.assertNotIn('#', assets[0].url)
        self.assertEqual('https://mausam.imd.gov.in/responsive/rainfall_statistics.php?PAGE=8', assets[0].parent_url)
        self.assertTrue(all('mausam.imd.gov.in' in item.url for item in assets))

    def test_rejects_parent_domain_spoof_and_insecure_or_irrelevant_assets(self):
        with self.assertRaisesRegex(ValueError, 'exact approved domain'):
            discover_official_linked_assets(self.page('', 'https://mausam.imd.gov.in.evil.example/page'),
                approved_domain='mausam.imd.gov.in', relevance_terms=('rainfall',))
        assets = discover_official_linked_assets(self.page(
            '<a href="http://mausam.imd.gov.in/Rainfall/rainfall.pdf">http</a>'
            '<a href="/reports/unrelated.pdf">unrelated</a>'),
            approved_domain='mausam.imd.gov.in', relevance_terms=('rainfall',))
        self.assertEqual([], assets)

    def test_is_bounded_and_html_only(self):
        html = ''.join(f'<img src="/Rainfall/rainfall-{n}.png">' for n in range(25))
        assets = discover_official_linked_assets(self.page(html), approved_domain='mausam.imd.gov.in',
            relevance_terms=('rainfall',), max_assets=3)
        self.assertEqual(3, len(assets))
        pdf = RetrievedContent('https://mausam.imd.gov.in/a.pdf', 200, 'x', 'application/pdf', {})
        self.assertEqual([], discover_official_linked_assets(pdf, approved_domain='mausam.imd.gov.in',
            relevance_terms=('rainfall',)))


if __name__ == '__main__':
    unittest.main()
