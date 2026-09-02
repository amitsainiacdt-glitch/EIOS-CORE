from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionReceipt, PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition


def acquired(body: bytes, acquisition_id: str):
    from hashlib import sha256
    now = datetime(2026, 9, 1, tzinfo=timezone.utc)
    url = "https://www.coromandel.biz/reports/annual.pdf"
    receipt = PublicSourceAcquisitionReceipt(
        1, acquisition_id, "CYCLE-1", "COROMANDEL-OFFICIAL-DOCUMENTS",
        "OFFICIAL_DOCUMENT_DISCOVERY", url, url, url, "www.coromandel.biz",
        "PUBLIC", PublicSourceAcquisitionStatus.RETRIEVED, now, now, 200,
        "application/pdf", "CORO-AR", sha256(body).hexdigest(), len(body), None, None, "EIOS",
    )
    source = TrustedPublicSourceDefinition("COROMANDEL", "Coromandel International", ("coromandel.biz",), source_type="COMPANY_PRIMARY")
    return TrustedPublicAcquisitionResult(source, receipt, RetrievedContent(url, 200, "pdf", "application/pdf", {}), body)


class CompanyDocumentArchiveTests(unittest.TestCase):
    def test_first_unchanged_and_new_version_are_preserved(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive = CompanyDocumentArchive(root / "documents", root / "ledger.jsonl")
            first = archive.preserve(acquired(b"version one", "A-1"), company_id="IN-COROMANDEL", document_id="AR-2025", acquired_at=datetime.now(timezone.utc))
            unchanged = archive.preserve(acquired(b"version one", "A-2"), company_id="IN-COROMANDEL", document_id="AR-2025", acquired_at=datetime.now(timezone.utc))
            changed = archive.preserve(acquired(b"version two", "A-3"), company_id="IN-COROMANDEL", document_id="AR-2025", acquired_at=datetime.now(timezone.utc))
            self.assertEqual((first.change_status, unchanged.change_status, changed.change_status), ("FIRST_SEEN", "UNCHANGED", "NEW_VERSION"))
            self.assertEqual((first.version_number, unchanged.version_number, changed.version_number), (1, 1, 2))
            self.assertEqual(len(archive.read_all()), 3)

    def test_receipt_byte_mismatch_is_rejected(self):
        with TemporaryDirectory() as directory:
            result = acquired(b"correct", "A-1")
            broken = TrustedPublicAcquisitionResult(result.source, result.receipt, result.retrieved_content, b"wrong")
            with self.assertRaisesRegex(ValueError, "do not match"):
                CompanyDocumentArchive(Path(directory) / "documents", Path(directory) / "ledger.jsonl").preserve(
                    broken, company_id="IN-COROMANDEL", document_id="AR-2025", acquired_at=datetime.now(timezone.utc)
                )


if __name__ == "__main__":
    unittest.main()
