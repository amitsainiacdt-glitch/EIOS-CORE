"""Offline end-to-end probe of the governed browser-capture fallback path."""

from datetime import datetime, timezone
import json
from pathlib import Path
from types import SimpleNamespace
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline
from modules.company_intelligence.browser_capture_fallback_provider import BrowserCaptureFallbackProvider
from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.company_intelligence.company_coverage_job_provider import load_company_coverage_jobs
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.search_result import ExternalSearchResult
from modules.external_intelligence.source_selection import SelectedSource


class DeliberatelyBlockedAdapter:
    """No-network primary adapter used only to prove fallback behavior."""
    def __init__(self, registry, ledger):
        self.registry = registry

    def acquire(self, **request):
        return SimpleNamespace(
            source=self.registry.resolve(request["url"]), document_bytes=None,
            receipt=SimpleNamespace(requested_url=request["url"], error_code="CONTROLLED_BLOCK"),
        )


def main() -> int:
    source_url = "https://www.coromandel.biz/wp-content/uploads/2026/07/Q1-results-1.pdf"
    job = next(item for item in load_company_coverage_jobs()
               if item.ticker == "COROMANDEL" and item.intent == "OFFICIAL_DOCUMENT_DISCOVERY")
    stamp = datetime.now(timezone.utc)
    output = ROOT / "data/runtime/browser_fallback_probe" / stamp.strftime("%Y%m%dT%H%M%SZ")
    acquisition_ledger = PublicSourceAcquisitionLedger(output / "acquisitions.jsonl")
    pipeline = AutomaticOfficialDocumentPipeline(
        CompanyDocumentArchive(output / "archive", output / "archive.jsonl"), acquisition_ledger,
        extraction_ledger=PublicDocumentExtractionLedger(output / "extractions.jsonl"),
        review_queue_root=output / "review_queue", adapter_factory=DeliberatelyBlockedAdapter,
        fallback_provider=BrowserCaptureFallbackProvider(
            ROOT / "data/runtime/browser_source_capture", workspace=ROOT, ledger=acquisition_ledger),
    )
    selected = SelectedSource(ExternalSearchResult(
        title="Coromandel Q1 FY2027 official results", url=source_url,
        snippet="Controlled offline fallback probe.", source="EIOS_PROBE"))
    summary = pipeline.run([job], [SimpleNamespace(selected_sources=[selected])],
                           cycle_id=f"BROWSER-FALLBACK-PROBE-{stamp.isoformat()}", acquired_at=stamp)
    payload = {**summary.__dict__, "network_used": False, "paid_search_used": False,
               "creates_approved_facts": False, "output": str(output)}
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if (summary.fallback_retrieved == 1 and summary.archived == 1
                 and summary.extracted == 1 and summary.quarterly_candidates >= 1) else 1


if __name__ == "__main__":
    raise SystemExit(main())
