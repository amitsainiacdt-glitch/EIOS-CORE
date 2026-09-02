import json
import tempfile
import unittest
from pathlib import Path

from modules.company_intelligence.company_coverage_job_provider import load_company_coverage_jobs


class CompanyCoverageJobProviderTests(unittest.TestCase):
    def test_loads_typed_jobs_from_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = {"schema_version": 1, "jobs": [{"job_id": "EX-NEWS", "company": "Example", "ticker": "EX", "question": "Check news", "intent": "CURRENT_NEWS", "frequency_minutes": 360}]}
            (root / "example_coverage_plan.json").write_text(json.dumps(payload), encoding="utf-8")
            jobs = load_company_coverage_jobs(root)
            self.assertEqual([job.job_id for job in jobs], ["EX-NEWS"])

    def test_duplicate_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = {"schema_version": 1, "jobs": [{"job_id": "DUP", "company": "Example", "ticker": "EX", "question": "Check news", "intent": "CURRENT_NEWS", "frequency_minutes": 360}]}
            (root / "a_coverage_plan.json").write_text(json.dumps(payload), encoding="utf-8")
            (root / "b_coverage_plan.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_company_coverage_jobs(root)


if __name__ == "__main__":
    unittest.main()
