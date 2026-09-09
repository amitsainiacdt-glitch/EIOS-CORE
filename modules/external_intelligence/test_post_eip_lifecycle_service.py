import unittest
from datetime import datetime, timedelta, timezone

from modules.external_intelligence.post_eip_lifecycle import (
    PostEIPConfirmationType, PostEIPEvidence, PostEIPLifecycleAction,
    PostEIPLifecycleAssessment, PostEIPRelationship,
)
from modules.external_intelligence.post_eip_lifecycle_service import PostEIPLifecycleService
from modules.external_intelligence.reader_eip_classification import ReaderEIPClassification, ReaderEIPClassificationResult
from modules.external_intelligence.reader_eip_classification_service import ReaderEIPClassificationService


class PostEIPLifecycleServiceTests(unittest.TestCase):
    def setUp(self):
        self.eip_at = datetime(2026, 9, 9, tzinfo=timezone.utc)
        self.reader = ReaderEIPClassificationResult(
            "PACKET-1", "a" * 64, ReaderEIPClassification.EARLIEST_INVESTABLE_POINT,
            "STAGE_3_EARLIEST_INVESTABLE_POINT", "Earliest Investable Point", "Reviewed.", (), False,
            ReaderEIPClassificationService.NON_AUTHORITY)
        self.service = PostEIPLifecycleService()

    def evidence(self, evidence_id, kind, relationship, group, *, kill=None, days=30):
        return PostEIPEvidence(
            evidence_id, kind, relationship, self.eip_at + timedelta(days=days),
            (f"SOURCE-{evidence_id}",), group, "Later public evidence addresses the original thesis.", kill)

    def assessment(self, evidence=(), **changes):
        values = dict(
            schema_version=1, assessment_id="LIFE-1", reader_packet_fingerprint="a" * 64,
            eip_identified_at=self.eip_at, evidence=tuple(evidence), unresolved_uncertainties=(),
            monitoring_requirements=("Continue monitoring the original causal indicator.",),
            public_information_only=True, non_authority_statement=PostEIPLifecycleService.NON_AUTHORITY)
        values.update(changes)
        return PostEIPLifecycleAssessment(**values)

    def test_two_independent_later_confirmations_allow_scale_review_only(self):
        evidence = (
            self.evidence("E-1", PostEIPConfirmationType.OPERATING_RESULT, PostEIPRelationship.CONFIRMS, "COMPANY-FILING"),
            self.evidence("E-2", PostEIPConfirmationType.CAUSAL_LEADING_INDICATOR, PostEIPRelationship.CONFIRMS, "INDUSTRY-DATA"),
        )
        result = self.service.evaluate(reader_classification=self.reader, assessment=self.assessment(evidence))
        self.assertEqual(result.action, PostEIPLifecycleAction.SCALE_REVIEW)
        self.assertFalse(result.authorizes_portfolio_action)
        self.assertFalse(result.changes_original_eip_date)

    def test_reported_results_are_later_confirmation_not_backdated_eip_evidence(self):
        evidence = (self.evidence("RESULT", PostEIPConfirmationType.FINANCIAL_RESULT,
                                  PostEIPRelationship.CONFIRMS, "FINANCIAL-RESULT"),)
        result = self.service.evaluate(reader_classification=self.reader, assessment=self.assessment(evidence))
        self.assertEqual(result.action, PostEIPLifecycleAction.WAIT_FOR_CONFIRMATION)
        self.assertFalse(result.changes_original_eip_date)

    def test_contradiction_holds_and_kill_test_has_priority(self):
        contradiction = self.evidence("C-1", PostEIPConfirmationType.OPERATING_RESULT,
                                      PostEIPRelationship.CONTRADICTS, "COMPANY")
        held = self.service.evaluate(reader_classification=self.reader, assessment=self.assessment((contradiction,)))
        self.assertEqual(held.action, PostEIPLifecycleAction.HOLD)
        killed = self.evidence("K-1", PostEIPConfirmationType.CAUSAL_LEADING_INDICATOR,
                               PostEIPRelationship.CONTRADICTS, "INDUSTRY", kill="Product spread reverses")
        result = self.service.evaluate(reader_classification=self.reader, assessment=self.assessment((contradiction, killed)))
        self.assertEqual(result.action, PostEIPLifecycleAction.KILL_THESIS_REVIEW)
        self.assertFalse(result.authorizes_portfolio_action)

    def test_unresolved_uncertainty_blocks_scale_review(self):
        evidence = (
            self.evidence("E-1", PostEIPConfirmationType.ANALYST_REVISION, PostEIPRelationship.CONFIRMS, "ANALYST"),
            self.evidence("E-2", PostEIPConfirmationType.FINANCIAL_RESULT, PostEIPRelationship.CONFIRMS, "FILING"),
        )
        result = self.service.evaluate(reader_classification=self.reader, assessment=self.assessment(
            evidence, unresolved_uncertainties=("Debt refinancing is unresolved.",)))
        self.assertEqual(result.action, PostEIPLifecycleAction.HOLD)

    def test_pre_eip_or_same_time_evidence_cannot_be_relabelled_as_confirmation(self):
        item = PostEIPEvidence("OLD", PostEIPConfirmationType.MANAGEMENT_GUIDANCE,
            PostEIPRelationship.CONFIRMS, self.eip_at, ("SOURCE",), "MANAGEMENT", "Old guidance", None)
        with self.assertRaisesRegex(ValueError, "after the original EIP"):
            self.service.evaluate(reader_classification=self.reader, assessment=self.assessment((item,)))

    def test_requires_exact_packet_and_governed_eip_status(self):
        with self.assertRaisesRegex(ValueError, "bind to reader packet"):
            self.service.evaluate(reader_classification=self.reader,
                                  assessment=self.assessment(reader_packet_fingerprint="b" * 64))
        early = ReaderEIPClassificationResult(**{**self.reader.__dict__, "classification": ReaderEIPClassification.EARLY_WATCH})
        with self.assertRaisesRegex(ValueError, "requires a governed EIP"):
            self.service.evaluate(reader_classification=early, assessment=self.assessment())


if __name__ == "__main__":
    unittest.main()
