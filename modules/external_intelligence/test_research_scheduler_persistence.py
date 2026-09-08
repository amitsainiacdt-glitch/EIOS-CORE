import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from modules.external_intelligence.research_job import ResearchJob
from modules.external_intelligence.research_scheduler import ResearchScheduler


def job():
    return ResearchJob(
        job_id="PERSISTED-JOB", company="Example Limited", ticker="EXAMPLE",
        question="Check official update", intent="GENERAL_RESEARCH",
        frequency_minutes=60, enabled=True, priority=50,
    )


class ResearchSchedulerPersistenceTests(unittest.TestCase):
    def test_restart_preserves_next_due_time(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "scheduler.json"
            first = ResearchScheduler(path)
            first.register(job())
            run_at = datetime(2026, 9, 8, 6, 0)
            first.mark_run(job(), run_at)

            restarted = ResearchScheduler(path)
            restarted.register(job())
            self.assertFalse(restarted.is_due(job(), run_at + timedelta(minutes=59)))
            self.assertTrue(restarted.is_due(job(), run_at + timedelta(minutes=60)))

    def test_corrupt_state_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "scheduler.json"
            path.write_text(json.dumps({"schema_version": 99, "jobs": {}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "persisted scheduler state"):
                ResearchScheduler(path)


if __name__ == "__main__":
    unittest.main()
