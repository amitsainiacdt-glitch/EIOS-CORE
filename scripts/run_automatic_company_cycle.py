"""Run one unattended, fail-closed EIOS company intelligence cycle."""

from __future__ import annotations

import json
import os
import traceback
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.company_intelligence.company_coverage_job_provider import load_company_coverage_jobs
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_jobs
from modules.company_intelligence.primary_indicator_cycle import process_primary_indicator_observations
from modules.company_intelligence.automatic_imd_rainfall_monitor import run_automatic_imd_rainfall_monitor
from modules.company_intelligence.review_memory_report import build_review_memory_report
from modules.company_intelligence.collection_outcome import describe_document_collection
from modules.company_intelligence.quarterly_source_retry import run_source_retries
from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline
from modules.company_intelligence.local_document_fallback_provider import LocalDocumentFallbackProvider
from modules.company_intelligence.browser_capture_fallback_provider import BrowserCaptureFallbackProvider
from modules.company_intelligence.official_document_fallback import ChainedOfficialDocumentFallback
from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.research_job_configuration import ResearchJobConfiguration
from modules.external_intelligence.research_runtime_bootstrap import ResearchRuntimeBootstrap, ResearchRuntimeBootstrapConfig
from scripts.build_coromandel_annual_report_study import main as build_coromandel_study
from scripts.build_coromandel_company_intelligence_snapshot import main as build_coromandel_snapshot
from scripts.sync_local_status_dashboard import main as sync_dashboard
from scripts.check_financial_source_regression import run_check as check_financial_sources


RUNTIME_DIR = ROOT / "data" / "runtime"
LOCK_PATH = RUNTIME_DIR / "automatic_company_cycle.lock"
STATUS_PATH = RUNTIME_DIR / "automatic_company_cycle_status.json"
DOCUMENT_ARCHIVE_ROOT = ROOT / "data" / "company_intelligence" / "document_archive"
DOCUMENT_ARCHIVE_LEDGER = ROOT / "data" / "company_intelligence" / "document_archive_ledger.jsonl"
DOCUMENT_ACQUISITION_LEDGER = ROOT / "data" / "company_intelligence" / "company_document_acquisition_ledger.jsonl"
DOCUMENT_EXTRACTION_LEDGER = ROOT / "data" / "company_intelligence" / "company_document_extraction_ledger.jsonl"
FACT_REVIEW_QUEUE_ROOT = ROOT / "data" / "company_intelligence" / "fact_review_queue"
OFFICIAL_DOCUMENT_INBOX = ROOT / "data" / "runtime" / "official_document_inbox"


def all_automatic_jobs():
    jobs = [*ResearchJobConfiguration.all_jobs(), *load_company_coverage_jobs(), *load_quarterly_monitoring_jobs()]
    ids = [job.job_id for job in jobs]
    if len(ids) != len(set(ids)):
        raise ValueError("automatic research job IDs must be unique")
    return jobs


def write_status(payload: dict) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    temporary = STATUS_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATUS_PATH)


def main() -> int:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(descriptor)
    except FileExistsError:
        write_status({"status": "SKIPPED_OVERLAPPING_RUN", "recorded_at": datetime.now(timezone.utc).isoformat()})
        return 2

    started_at = datetime.now(timezone.utc)
    status = {"status": "RUNNING", "started_at": started_at.isoformat(), "job_count": 0, "executed_jobs": 0, "observations": None, "official_documents": None, "errors": []}
    write_status(status)
    try:
        os.chdir(ROOT)
        status["financial_source_consistency"] = check_financial_sources()
        if status["financial_source_consistency"]["issues"]:
            raise ValueError("Previously checked financial sources require re-review")
        status["review_memory"] = build_review_memory_report(
            ROOT / "data/company_intelligence/company_fact_human_reviews.jsonl",
            evaluated_at=started_at,
        )
        if status["review_memory"]["failed_review_ids"]:
            raise ValueError("Review-memory replay safeguards failed")
        config = ResearchRuntimeBootstrapConfig.from_environment()
        bootstrap = ResearchRuntimeBootstrap(config, job_provider=all_automatic_jobs)
        validation = bootstrap.validate()
        status["job_count"] = validation.job_count
        if not validation.ready:
            status["status"] = "CONFIGURATION_BLOCKED"
            status["errors"] = list(validation.errors)
            return 1

        # Saved document retries are independent of the search provider. Run them
        # after validation/safety gates but before search can fail.
        status['quarterly_source_retries'] = run_source_retries(ROOT, now=started_at,
                                                               offline=config.offline_mode, execute=True)
        write_status(status)
        runtime, result = bootstrap.run_once(now=started_at.replace(tzinfo=None))
        status["executed_jobs"] = len(result.executed_jobs)
        status["observations"] = runtime.observation_count()
        status['primary_indicators'] = process_primary_indicator_observations(
            runtime.observation_registry.all(), ledger_path=ROOT / 'data/company_intelligence/primary_indicator_records.jsonl',
            recorded_at=started_at)
        # Direct official-asset monitoring is independent of paid search. It is
        # internally weekly-cadenced and records only a hash-bound IMD baseline
        # or comparison; it cannot promote a catalyst or alter the verdict.
        status['official_indicator_assets'] = run_automatic_imd_rainfall_monitor(ROOT, now=started_at)

        acquisition_ledger = PublicSourceAcquisitionLedger(DOCUMENT_ACQUISITION_LEDGER)
        document_summary = AutomaticOfficialDocumentPipeline(
            CompanyDocumentArchive(DOCUMENT_ARCHIVE_ROOT, DOCUMENT_ARCHIVE_LEDGER),
            acquisition_ledger,
            extraction_ledger=PublicDocumentExtractionLedger(DOCUMENT_EXTRACTION_LEDGER),
            review_queue_root=FACT_REVIEW_QUEUE_ROOT,
            source_manifest=None if config.offline_mode else json.loads(
                (ROOT / 'data/company_intelligence/company_source_manifest.json').read_text(encoding='utf-8')),
            fallback_provider=ChainedOfficialDocumentFallback(
                BrowserCaptureFallbackProvider(RUNTIME_DIR / "browser_source_capture", workspace=ROOT, ledger=acquisition_ledger),
                LocalDocumentFallbackProvider(OFFICIAL_DOCUMENT_INBOX, workspace=ROOT, ledger=acquisition_ledger),
            ),
        ).run(result.executed_jobs, result.results, cycle_id=started_at.isoformat(), acquired_at=started_at)
        status["official_documents"] = document_summary.__dict__
        status["collection_outcome"] = describe_document_collection(status["official_documents"])

        # Rebuild read models after collection. These builders remain fail-closed:
        # they do not approve evidence or manufacture a verdict.
        build_coromandel_study()
        build_coromandel_snapshot()
        status["status"] = "SUCCESS"
        return 0
    except Exception as exc:
        status["status"] = "FAILED"
        status["errors"] = [f"{type(exc).__name__}: {exc}"]
        status["traceback"] = traceback.format_exc(limit=8)
        return 1
    finally:
        status["finished_at"] = datetime.now(timezone.utc).isoformat()
        write_status(status)
        LOCK_PATH.unlink(missing_ok=True)
        try:
            sync_dashboard()
        except Exception as dashboard_exc:
            status["dashboard_sync_error"] = f"{type(dashboard_exc).__name__}: {dashboard_exc}"
            write_status(status)


if __name__ == "__main__":
    raise SystemExit(main())
