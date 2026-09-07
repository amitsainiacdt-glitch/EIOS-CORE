from datetime import datetime, timezone
from hashlib import sha256
from types import SimpleNamespace
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


if __name__ == "__main__":
    unittest.main()
