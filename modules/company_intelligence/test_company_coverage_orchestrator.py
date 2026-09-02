import unittest

from modules.company_intelligence.company_coverage_orchestrator import CompanyCoverageProfile, build_company_coverage_plan


class CompanyCoverageOrchestratorTests(unittest.TestCase):
    def profile(self):
        return CompanyCoverageProfile("IN-COROMANDEL", "Coromandel International", "COROMANDEL", "NSE", "Fertilizers", "https://www.coromandel.biz/investors/")

    def test_standard_plan_covers_all_mandatory_monitoring_families(self):
        plan = build_company_coverage_plan(self.profile())
        self.assertEqual(len(plan.jobs), 8)
        self.assertIn("OFFICIAL_DOCUMENT_DISCOVERY", {job.intent for job in plan.jobs})
        self.assertIn("CURRENT_NEWS", {job.intent for job in plan.jobs})
        self.assertIn("CATALYST_AND_EXPECTATION_GAP", {job.intent for job in plan.jobs})

    def test_job_ids_are_unique_and_ticker_scoped(self):
        plan = build_company_coverage_plan(self.profile())
        ids = [job.job_id for job in plan.jobs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(job_id.startswith("COROMANDEL-") for job_id in ids))
        self.assertTrue(all(job.entity_domain == "www.coromandel.biz" for job in plan.jobs))

    def test_invalid_issuer_source_is_rejected(self):
        with self.assertRaises(ValueError):
            CompanyCoverageProfile("ID", "Example", "EX", "NSE", "Sector", "http://example.com")

    def test_disabled_company_produces_disabled_jobs(self):
        profile = CompanyCoverageProfile("ID", "Example", "EX", "NSE", "Sector", "https://example.com/investors", enabled=False)
        self.assertTrue(all(not job.enabled for job in build_company_coverage_plan(profile).jobs))


if __name__ == "__main__":
    unittest.main()
