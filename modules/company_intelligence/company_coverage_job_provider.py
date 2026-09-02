"""Load recurring ResearchJob definitions from governed company coverage plans."""

from __future__ import annotations

import json
from pathlib import Path

from modules.external_intelligence.research_job import ResearchJob


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN_ROOT = ROOT / "data" / "company_intelligence"


def load_company_coverage_jobs(plan_root: Path = DEFAULT_PLAN_ROOT) -> list[ResearchJob]:
    jobs: list[ResearchJob] = []
    seen: set[str] = set()
    for path in sorted(plan_root.glob("**/*_coverage_plan.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError(f"unsupported coverage plan schema: {path.name}")
        for record in payload.get("jobs", []):
            job = ResearchJob(**record)
            job.validate()
            if job.job_id in seen:
                raise ValueError(f"duplicate company coverage job: {job.job_id}")
            seen.add(job.job_id)
            jobs.append(job)
    return jobs


__all__ = ["load_company_coverage_jobs"]
