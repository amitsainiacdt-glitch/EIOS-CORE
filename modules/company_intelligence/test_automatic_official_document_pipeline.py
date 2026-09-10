from datetime import datetime, timezone
from hashlib import sha256
from types import SimpleNamespace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline
from modules.company_intelligence.official_document_fallback import OfficialDocumentDeliveryProvenance
from modules.external_intelligence.research_job import ResearchJob


class FakeArchive:
    def __init__(self):
        self.urls = []

    def preserve(self, result, **kwargs):
        self.urls.append(result.url)
        return SimpleNamespace(change_status=result.change_status)


class FakeAdapter:
    calls = []

    def __init__(self, registry, ledger):
        self.registry = registry

    def acquire(self, **kwargs):
        self.calls.append(kwargs["url"])
        status = "UNCHANGED" if "unchanged" in kwargs["url"] else "FIRST_SEEN"
        return SimpleNamespace(document_bytes=b"document", url=kwargs["url"], change_status=status)


class FailingAdapter(FakeAdapter):
    def acquire(self, **kwargs):
        raise ValueError("malformed document")


class BlockedAdapter(FakeAdapter):
    def acquire(self, **kwargs):
        return SimpleNamespace(document_bytes=None, receipt=SimpleNamespace(requested_url=kwargs["url"]))


class GovernedFallback:
    def __init__(self):
        self.calls = 0

    def acquire_after_failure(self, primary_result, **kwargs):
        self.calls += 1
        body = b"%PDF provider-delivered official copy"
        return SimpleNamespace(
            document_bytes=body,
            retrieved_content=SimpleNamespace(content_type="application/pdf"),
            receipt=SimpleNamespace(
                requested_url=kwargs["url"], document_hash=sha256(body).hexdigest(),
                bytes_received=len(body), source_url=kwargs["url"], content_type="application/pdf",
                acquisition_id=kwargs["acquisition_id"],
            ),
            delivery_provenance=OfficialDocumentDeliveryProvenance(
                "APPROVED_PROVIDER", "https://provider.example/delivery", kwargs["url"]),
            source=SimpleNamespace(source_id="ISSUER-COROMANDEL"),
            url=kwargs["url"], change_status="FIRST_SEEN",
        )


def job(intent="OFFICIAL_DOCUMENT_DISCOVERY"):
    return ResearchJob(
        "COROMANDEL-OFFICIAL", "Coromandel International", "COROMANDEL",
        "Check official documents", intent, 60, entity_domain="www.coromandel.biz",
    )


class AutomaticOfficialDocumentPipelineTests(unittest.TestCase):
    def setUp(self):
        FakeAdapter.calls = []

    def test_only_approved_official_urls_are_archived(self):
        archive = FakeArchive()
        selected = [
            SimpleNamespace(result=SimpleNamespace(url="https://www.coromandel.biz/reports/new.pdf")),
            SimpleNamespace(result=SimpleNamespace(url="https://www.nseindia.com/filing/unchanged.pdf")),
            SimpleNamespace(result=SimpleNamespace(url="https://third-party.example/report.pdf")),
        ]
        summary = AutomaticOfficialDocumentPipeline(archive, object(), adapter_factory=FakeAdapter).run(
            [job()], [SimpleNamespace(selected_sources=selected)],
            cycle_id="CYCLE-1", acquired_at=datetime.now(timezone.utc),
        )
        self.assertEqual(summary.candidates_seen, 3)
        self.assertEqual(summary.approved_urls, 2)
        self.assertEqual(summary.archived, 2)
        self.assertEqual(summary.unchanged, 1)
        self.assertEqual(len(FakeAdapter.calls), 2)

    def test_non_official_job_is_ignored(self):
        summary = AutomaticOfficialDocumentPipeline(FakeArchive(), object(), adapter_factory=FakeAdapter).run(
            [job("CURRENT_NEWS")], [SimpleNamespace(selected_sources=[])],
            cycle_id="CYCLE-1", acquired_at=datetime.now(timezone.utc),
        )
        self.assertEqual(summary.candidates_seen, 0)

    def test_one_document_failure_is_counted_without_raising(self):
        selected = [SimpleNamespace(result=SimpleNamespace(url="https://www.coromandel.biz/reports/bad.pdf"))]
        summary = AutomaticOfficialDocumentPipeline(FakeArchive(), object(), adapter_factory=FailingAdapter).run(
            [job()], [SimpleNamespace(selected_sources=selected)],
            cycle_id="CYCLE-1", acquired_at=datetime.now(timezone.utc),
        )
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.archived, 0)

    def test_blocked_document_uses_governed_fallback_then_normal_archive(self):
        archive = FakeArchive()
        fallback = GovernedFallback()
        url = "https://www.coromandel.biz/reports/blocked.pdf"
        selected = [SimpleNamespace(result=SimpleNamespace(url=url))]
        summary = AutomaticOfficialDocumentPipeline(
            archive, object(), adapter_factory=BlockedAdapter, fallback_provider=fallback,
        ).run([job()], [SimpleNamespace(selected_sources=selected)],
              cycle_id="CYCLE-1", acquired_at=datetime.now(timezone.utc))
        self.assertEqual(fallback.calls, 1)
        self.assertEqual(archive.urls, [url])
        self.assertEqual(summary.archived, 1)
        self.assertEqual(summary.fallback_attempted, 1)
        self.assertEqual(summary.fallback_retrieved, 1)
        self.assertEqual(summary.fallback_unavailable, 0)
        self.assertEqual(summary.fallback_providers, {"APPROVED_PROVIDER": 1})

    def test_missing_fallback_document_is_reported_without_false_success(self):
        class EmptyFallback:
            def acquire_after_failure(self, primary_result, **kwargs):
                return None
        url = "https://www.coromandel.biz/reports/missing.pdf"
        summary = AutomaticOfficialDocumentPipeline(
            FakeArchive(), object(), adapter_factory=BlockedAdapter, fallback_provider=EmptyFallback(),
        ).run([job()], [SimpleNamespace(selected_sources=[SimpleNamespace(result=SimpleNamespace(url=url))])],
              cycle_id="CYCLE-1", acquired_at=datetime.now(timezone.utc))
        self.assertEqual(summary.archived, 0)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.fallback_attempted, 1)
        self.assertEqual(summary.fallback_unavailable, 1)

    def test_new_official_nse_ixbrl_is_staged_for_review(self):
        rows = [
            ('NSE Symbol','COROMANDEL'),('ISIN','INE169A01031'),('Name of company','Coromandel International'),
            ('Description of presentation currency','INR'),('Level of rounding used in financial results','Lakhs'),
            ('Reporting Type','Quarterly'),('Reporting Quarter','First quarter'),
            ('Nature of report standalone or consolidated','Standalone'),
            ('Date of start of reporting period','01-04-2026'),('Date of end of reporting period','30-06-2026'),
            ('Revenue from operations','100'),('Other income','2'),('Total income','102'),
            ('Cost of materials consumed','40'),('Total expenses','90'),('Total profit before tax','12'),
            ('Total profit (loss) for period','10')]
        body = ('<table>'+''.join('<tr>'+''.join(f'<td>{v}</td>' for v in row)+'</tr>' for row in rows)+'</table>').encode()
        url = 'https://nsearchives.nseindia.com/corporate/result.html'
        class IxbrlAdapter(FakeAdapter):
            def acquire(self, **kwargs):
                return SimpleNamespace(document_bytes=body, url=url, change_status='FIRST_SEEN',
                    receipt=SimpleNamespace(source_url=url, content_type='text/html', document_hash=sha256(body).hexdigest()))
        with TemporaryDirectory() as directory:
            summary = AutomaticOfficialDocumentPipeline(
                FakeArchive(), object(), adapter_factory=IxbrlAdapter,
                extraction_ledger=object(), review_queue_root=Path(directory)).run(
                    [job('EXCHANGE_DISCLOSURES')],
                    [SimpleNamespace(selected_sources=[SimpleNamespace(result=SimpleNamespace(url=url))])],
                    cycle_id='CYCLE-1', acquired_at=datetime.now(timezone.utc))
            self.assertEqual(summary.exchange_ixbrl_candidates, 1)
            self.assertEqual(summary.exchange_ixbrl_holds, 0)
            self.assertEqual(summary.exchange_ixbrl_auto_bound, 1)
            self.assertEqual(summary.exchange_ixbrl_human_review_required, 0)
            self.assertEqual(len(list(Path(directory).rglob('exchange-ixbrl-candidate.json'))), 1)


if __name__ == "__main__":
    unittest.main()
