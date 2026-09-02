import unittest

from modules.company_intelligence.annual_report_study import AnnualReportStudy, StudyFinding, StudyStatus


class AnnualReportStudyTests(unittest.TestCase):
    def test_coverage_is_calculated(self):
        study = AnnualReportStudy(1, "Example", "EX", 10, 10, 1, 0, StudyStatus.PARTIAL, (), (), "HOLD", "Incomplete")
        self.assertEqual(study.extraction_coverage_percent, 10)

    def test_complete_status_requires_all_years(self):
        with self.assertRaises(ValueError):
            AnnualReportStudy(1, "Example", "EX", 10, 10, 9, 0, StudyStatus.READY_FOR_HUMAN_REVIEW, (), (), "READY", "Complete")

    def test_finding_requires_traceable_fact(self):
        with self.assertRaises(ValueError):
            StudyFinding("F1", "FINANCIAL", "Headline", "Interpretation", (), 80)

    def test_study_cannot_create_recommendation(self):
        with self.assertRaises(ValueError):
            AnnualReportStudy(1, "Example", "EX", 10, 10, 1, 0, StudyStatus.PARTIAL, (), (), "HOLD", "Incomplete", creates_recommendation=True)


if __name__ == "__main__":
    unittest.main()
