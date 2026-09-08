"""Run exactly one governed live primary-indicator job as a low-cost canary."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.company_intelligence.primary_indicator_cycle import process_primary_indicator_results
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_jobs
from modules.external_intelligence.research_runtime_bootstrap import ResearchRuntimeBootstrap, ResearchRuntimeBootstrapConfig


STATUS_PATH = ROOT / "data/runtime/primary_indicator_canary_status.json"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    args = parser.parse_args(argv)
    started = datetime.now(timezone.utc)
    status = {"status": "RUNNING", "job_id": args.job_id, "started_at": started.isoformat(),
              "paid_search_job_limit": 1, "errors": []}
    try:
        if not os.environ.get("TAVILY_API_KEY", "").strip():
            raise ValueError("live-search credential is unavailable")
        jobs = [job for job in load_quarterly_monitoring_jobs() if job.job_id == args.job_id]
        if len(jobs) != 1:
            raise ValueError("canary job ID must match exactly one primary-indicator job")
        config = ResearchRuntimeBootstrapConfig(
            tavily_api_key=os.environ["TAVILY_API_KEY"],
            observation_path=ROOT / "data/observations.json",
            offline_mode=False,
            scheduler_state_path=ROOT / "data/runtime/research_schedule_state.json",
        )
        runtime, result = ResearchRuntimeBootstrap(config, job_provider=lambda: jobs).run_once(
            started.replace(tzinfo=None)
        )
        indicator = process_primary_indicator_results(
            result.results,
            ledger_path=ROOT / "data/company_intelligence/primary_indicator_records.jsonl",
            recorded_at=started,
        )
        collection = []
        for item in result.results:
            collection.append({
                "job_id": item.job_id,
                "selected_source_count": len(item.selected_sources),
                "selected_source_domains": sorted({
                    (urlsplit(source.result.url).hostname or "").casefold()
                    for source in item.selected_sources
                }),
                "retrieved_content_count": len(item.retrieved_content),
                "source_assessment_count": len(item.source_assessments),
                "observation_count": len(item.observations),
                "retrieval_failures": [
                    {"url": failure.url, "error_type": failure.error_type}
                    for failure in item.retrieval_failures
                ],
            })
        status.update(status="SUCCESS", executed_jobs=len(result.executed_jobs),
                      observations=runtime.observation_count(), collection=collection,
                      primary_indicators=indicator)
        return 0
    except Exception as exc:
        status.update(status="FAILED", errors=[f"{type(exc).__name__}: {exc}"])
        return 1
    finally:
        status["finished_at"] = datetime.now(timezone.utc).isoformat()
        STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATUS_PATH.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: value for key, value in status.items() if key not in {"errors"}}, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
