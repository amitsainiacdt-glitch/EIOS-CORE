from datetime import datetime, timezone
from types import SimpleNamespace
import unittest

from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline
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


if __name__ == "__main__":
    unittest.main()
