from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from modules.company_intelligence.automatic_exchange_ixbrl_intake import stage_exchange_ixbrl_candidate
from modules.company_intelligence.bound_exchange_corroboration_store import load_bound_exchange_corroborations

def html():
    rows=[('NSE Symbol','TEST'),('ISIN','INE000000001'),('Name of company','Test Limited'),('Description of presentation currency','INR'),('Level of rounding used in financial results','Lakhs'),('Reporting Type','Quarterly'),('Reporting Quarter','First quarter'),('Nature of report standalone or consolidated','Standalone'),('Date of start of reporting period','01-04-2026'),('Date of end of reporting period','30-06-2026'),('Revenue from operations','100'),('Other income','2'),('Total income','102'),('Cost of materials consumed','40'),('Total expenses','90'),('Total profit before tax','12'),('Total profit (loss) for period','10')]
    return ('<table>'+''.join('<tr>'+''.join(f'<td>{v}</td>' for v in row)+'</tr>' for row in rows)+'</table>').encode()

class BoundExchangeCorroborationStoreTests(unittest.TestCase):
    def test_verified_lineage_loads_and_tamper_fails(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);body=html();url='https://nsearchives.nseindia.com/x.html'
            acquisition=SimpleNamespace(document_bytes=body,receipt=SimpleNamespace(source_url=url,content_type='text/html',document_hash=sha256(body).hexdigest()))
            stage_exchange_ixbrl_candidate(acquisition,ticker='TEST',company='Test Limited',output_root=root)
            loaded=load_bound_exchange_corroborations(root,'TEST')
            self.assertEqual(len(loaded),1);self.assertEqual(loaded[0]['values_inr_lakh']['revenue'],['100'])
            path=next(root.rglob('exchange-ixbrl-bound-corroboration.json'));path.write_text(path.read_text().replace('"100"','"999"'))
            with self.assertRaisesRegex(ValueError,'lineage'):load_bound_exchange_corroborations(root,'TEST')
    def test_missing_company_store_is_empty(self):
        with TemporaryDirectory() as directory:self.assertEqual(load_bound_exchange_corroborations(Path(directory),'NONE'),())

if __name__=='__main__':unittest.main()
