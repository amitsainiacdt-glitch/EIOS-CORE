from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine, CompanyCandidateMetaReviewWriter
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate


def candidate(**changes):
    values = dict(
        schema_version=1, candidate_id="CANDIDATE-1", company="Coromandel International",
        event_type="CAPACITY_CHANGE", statement_posture="ASSERTED",
        source_passage="Coromandel International commissioned new fertilizer capacity worth INR 125 crore on 28 August 2026.",
        explicit_amounts=("INR 125 crore",), explicit_dates=("28 August 2026",), pdf_page=7,
        source_url="https://www.coromandel.biz/report.pdf", document_hash="a" * 64,
        extraction_id="EXT-1", extraction_method="pypdf_text_layer_v1",
    )
    values.update(changes)
    return CompanyFactReviewCandidate(**values)


class CompanyCandidateMetaReviewTests(unittest.TestCase):
    def test_material_primary_candidate_reaches_human_review_only(self):
        result = CompanyCandidateMetaReviewEngine().assess(candidate(), reviewed_at=datetime.now(timezone.utc))
        self.assertEqual(result.decision, "READY_FOR_HUMAN_REVIEW")
        self.assertEqual(result.authority_status, "VERIFIED_PRIMARY_LINEAGE")
        self.assertFalse(result.creates_evidence)
        self.assertFalse(result.creates_catalyst)
        self.assertFalse(result.changes_verdict)
        self.assertIn("EARNINGS_AND_VALUATION_CAUSALITY_UNPROVEN", result.reason_codes)

    def test_missing_page_and_company_reference_force_hold(self):
        result = CompanyCandidateMetaReviewEngine().assess(
            candidate(pdf_page=None, source_passage="A facility may expand in future."),
            reviewed_at=datetime.now(timezone.utc),
        )
        self.assertEqual(result.decision, "HOLD_FOR_RESEARCH")
        self.assertIn("PDF_PAGE_CITATION_MISSING", result.reason_codes)
        self.assertIn("DIRECT_COMPANY_REFERENCE_MISSING", result.reason_codes)

    def test_writer_preserves_non_authority_boundary(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "meta.json"
            CompanyCandidateMetaReviewWriter().write((candidate(),), output_path=output, reviewed_at=datetime.now(timezone.utc))
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["ready_for_human_review"], 1)
            self.assertFalse(payload["creates_evidence"])
            self.assertTrue(payload["requires_mandatory_meta"])


if __name__ == "__main__":
    unittest.main()
