import unittest
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_jobs


class QuarterlyMonitoringJobProviderTests(unittest.TestCase):
    def test_loads_six_primary_source_jobs(self):
        jobs=load_quarterly_monitoring_jobs()
        self.assertEqual(6,len(jobs))
        self.assertTrue(all(job.intent=='PRIMARY_INDICATOR_MONITORING' for job in jobs))
        self.assertEqual(6,len({job.job_id for job in jobs}))
        self.assertTrue(all(job.entity_domain for job in jobs))


if __name__=='__main__': unittest.main()
