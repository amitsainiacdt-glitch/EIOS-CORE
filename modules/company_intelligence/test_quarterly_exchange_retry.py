from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime,timezone
import unittest
from modules.company_intelligence.quarterly_exchange_retry import QuarterlyExchangeRetryService

class QuarterlyExchangeRetryTests(unittest.TestCase):
    def setup(self,directory,matched=1):
        root=Path(directory);pdf=root/'report.pdf';pdf.write_bytes(b'%PDF-test');digest=sha256(pdf.read_bytes()).hexdigest();calls=[]
        def runner(path,**kwargs):calls.append((path,kwargs));return {'exchange_corroboration_matches':matched}
        service=QuarterlyExchangeRetryService(root/'retries.jsonl',workspace=root,runner=runner)
        item=service.schedule(ticker='TEST',company='Test Limited',pdf_path=pdf,pdf_hash=digest,source_url='https://issuer.example/q.pdf',recorded_at=datetime.now(timezone.utc))
        return service,item,pdf,calls
    def test_arriving_exchange_retries_and_completes(self):
        with TemporaryDirectory() as directory:
            service,item,pdf,calls=self.setup(directory)
            result=service.retry_for('TEST',[{'status':'EXCHANGE_CORROBORATION_CANDIDATE'}])
            self.assertEqual(result[0].status,'RECONCILED');self.assertEqual(result[0].attempts,1);self.assertEqual(len(calls),1)
            self.assertEqual(service.retry_for('TEST',[{}]),())
    def test_no_exact_match_stays_waiting_and_schedule_is_idempotent(self):
        with TemporaryDirectory() as directory:
            service,item,pdf,calls=self.setup(directory,matched=0)
            same=service.schedule(ticker='TEST',company='Test Limited',pdf_path=pdf,pdf_hash=item.pdf_hash,source_url=item.source_url)
            self.assertEqual(same,item);self.assertEqual(service.retry_for('TEST',[{}])[0].status,'WAITING_FOR_EXACT_MATCH')
    def test_changed_pdf_and_tampered_ledger_fail_closed(self):
        with TemporaryDirectory() as directory:
            service,item,pdf,calls=self.setup(directory);pdf.write_bytes(b'changed')
            self.assertEqual(service.retry_for('TEST',[{}])[0].status,'RETRY_FAILED_HOLD')
            ledger=Path(directory)/'retries.jsonl';ledger.write_text(ledger.read_text().replace('WAITING_FOR_EXCHANGE','RECONCILED'))
            with self.assertRaisesRegex(ValueError,'fingerprint'):service.read_all()
    def test_path_outside_workspace_rejected(self):
        with TemporaryDirectory() as directory:
            service=QuarterlyExchangeRetryService(Path(directory)/'x.jsonl',workspace=Path(directory))
            with self.assertRaisesRegex(ValueError,'inside workspace'):service.schedule(ticker='T',company='T',pdf_path=Path(directory).parent/'outside.pdf',pdf_hash='a'*64,source_url='https://x')

if __name__=='__main__':unittest.main()
