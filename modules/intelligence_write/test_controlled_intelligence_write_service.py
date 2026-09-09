"""Contract and negative-path tests for the non-production write boundary."""

import dataclasses
import hashlib
import unittest
from datetime import datetime, timezone

from modules.external_intelligence.causal_first_eip_packet import CausalFirstEIPDecisionPacket
from modules.intelligence_write import (
    ActorOrigin, ActorType, AuthorityScope, ControlledIntelligenceWriteService,
    InformationClass, OriginType, SourceReference, ValidationStatus, WriteCommand,
    WriteOperation, WriteReceiptStatus, command_fingerprint, verify_receipt_fingerprint,
)


NOW = datetime(2026, 9, 9, 12, 0, tzinfo=timezone.utc)
SOURCE = SourceReference("NSE-1", "EXCHANGE_FILING", "https://nseindia.com/filing/1", "a" * 64, "page 2")


def actor(actor_type=ActorType.HUMAN, scopes=(AuthorityScope.PROPOSE_FACT,), actor_id="analyst-1"):
    origins = {
        ActorType.HUMAN: OriginType.HUMAN_REVIEW,
        ActorType.AI_MODEL: OriginType.AI_ANALYSIS,
        ActorType.EXTRACTION_SERVICE: OriginType.AUTOMATED_EXTRACTION,
        ActorType.RESEARCH_JOB: OriginType.SCHEDULED_RESEARCH,
        ActorType.SYSTEM_ENGINE: OriginType.DETERMINISTIC_ENGINE,
        ActorType.DECISION_ORCHESTRATOR: OriginType.GOVERNED_DECISION,
    }
    return ActorOrigin(actor_id, actor_type, "v1", "origin-1", origins[actor_type], tuple(scopes))


def fact_command(**changes):
    values = dict(
        schema_version=1, command_id="cmd-1", idempotency_key="idem-1",
        operation=WriteOperation.PROPOSE_FACT, actor=actor(), requested_at=NOW,
        company_id="IN-TEST", entity="Test Limited", information_class=InformationClass.FACT,
        semantic_key="revenue|2026-06-30|standalone", payload={
            "metric": "REVENUE", "value": 100, "unit": "INR_CRORE",
            "period": "2026-06-30", "basis": "STANDALONE",
        }, source_references=(SOURCE,), confidence=90,
        requested_validation_status=ValidationStatus.PROVISIONAL,
    )
    values.update(changes)
    return WriteCommand(**values)


class ControlledWriteTests(unittest.TestCase):
    def service(self):
        return ControlledIntelligenceWriteService(clock=lambda: NOW)

    def assert_valid_receipt(self, service, receipt):
        self.assertTrue(verify_receipt_fingerprint(receipt))
        self.assertIn(receipt, service.receipts())

    def test_machine_and_ai_facts_are_forced_provisional(self):
        for actor_type in (ActorType.AI_MODEL, ActorType.EXTRACTION_SERVICE, ActorType.RESEARCH_JOB):
            service = self.service()
            command = fact_command(
                command_id=f"cmd-{actor_type.value}", idempotency_key=f"idem-{actor_type.value}",
                actor=actor(actor_type, (AuthorityScope.PROPOSE_FACT,), actor_id=actor_type.value),
                requested_validation_status=ValidationStatus.VERIFIED,
            )
            receipt = service.submit(command)
            self.assertEqual(receipt.status, WriteReceiptStatus.ACCEPTED_PROVISIONAL)
            self.assertEqual(service.get_record(receipt.record_id).validation_status, ValidationStatus.PROVISIONAL)
            self.assertIn("MACHINE_FACT_FORCED_PROVISIONAL", receipt.validation_codes)
            self.assert_valid_receipt(service, receipt)

    def test_ai_cannot_verify_fact(self):
        service = self.service(); created = service.submit(fact_command())
        prior = service.get_record(created.record_id)
        verification = fact_command(
            command_id="verify-1", idempotency_key="verify-idem", operation=WriteOperation.VERIFY_RECORD,
            actor=actor(ActorType.AI_MODEL, (AuthorityScope.VERIFY_FACT,), "ai-1"),
            prior_record_id=prior.record_id, expected_current_revision=prior.record_fingerprint,
            requested_validation_status=ValidationStatus.VERIFIED,
        )
        receipt = service.submit(verification)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("AI_CANNOT_VERIFY_FACT", receipt.rejection_codes)
        self.assert_valid_receipt(service, receipt)

    def test_authorized_human_can_verify_exact_revision(self):
        service = self.service(); created = service.submit(fact_command())
        prior = service.get_record(created.record_id)
        verification = fact_command(
            command_id="verify-human", idempotency_key="verify-human-idem", operation=WriteOperation.VERIFY_RECORD,
            actor=actor(ActorType.HUMAN, (AuthorityScope.VERIFY_FACT,), "reviewer-2"),
            prior_record_id=prior.record_id, expected_current_revision=prior.record_fingerprint,
            requested_validation_status=ValidationStatus.VERIFIED,
        )
        receipt = service.submit(verification)
        self.assertEqual(receipt.status, WriteReceiptStatus.ACCEPTED)
        self.assertEqual(service.get_record(receipt.record_id).validation_status, ValidationStatus.VERIFIED)

    def test_verification_cannot_change_fact_payload(self):
        service = self.service(); created = service.submit(fact_command())
        prior = service.get_record(created.record_id)
        changed = fact_command(
            command_id="verify-mutated", idempotency_key="verify-mutated-idem",
            operation=WriteOperation.VERIFY_RECORD,
            actor=actor(ActorType.HUMAN, (AuthorityScope.VERIFY_FACT,), "reviewer-5"),
            prior_record_id=prior.record_id, expected_current_revision=prior.record_fingerprint,
            requested_validation_status=ValidationStatus.VERIFIED,
            payload={"metric": "REVENUE", "value": 999, "unit": "INR_CRORE", "period": "2026-06-30", "basis": "STANDALONE"},
        )
        receipt = service.submit(changed)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("VERIFICATION_CANNOT_CHANGE_RECORD", receipt.rejection_codes)

    def test_information_classes_cannot_masquerade(self):
        service = self.service()
        masquerade = fact_command(payload={
            "metric": "REVENUE", "value": 100, "unit": "INR_CRORE", "period": "FY26",
            "basis": "STANDALONE", "mechanism": "demand improved",
        })
        receipt = service.submit(masquerade)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("INFORMATION_CLASS_MASQUERADE", receipt.rejection_codes)

    def test_operation_class_mismatch_is_rejected(self):
        service = self.service()
        receipt = service.submit(fact_command(information_class=InformationClass.INFERENCE))
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("INFORMATION_CLASS_OPERATION_MISMATCH", receipt.rejection_codes)

    def test_derived_metric_requires_formula_and_inputs(self):
        service = self.service()
        command = fact_command(
            operation=WriteOperation.RECORD_DERIVED_METRIC,
            actor=actor(ActorType.SYSTEM_ENGINE, (AuthorityScope.RECORD_DERIVED_METRIC,)),
            information_class=InformationClass.DERIVED_METRIC, source_references=(),
            semantic_key="ebitda-margin|2026-06-30|standalone",
            payload={"metric": "EBITDA_MARGIN", "value": 12, "unit": "PERCENT"},
        )
        receipt = service.submit(command)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("INFORMATION_CLASS_REQUIRED_FIELDS_MISSING", receipt.rejection_codes)

    def test_duplicate_fact_is_idempotent_without_new_record(self):
        service = self.service(); first = service.submit(fact_command())
        second = service.submit(fact_command(command_id="cmd-2", idempotency_key="idem-2"))
        self.assertEqual(second.status, WriteReceiptStatus.DUPLICATE_NO_CHANGE)
        self.assertEqual(second.record_id, first.record_id)
        self.assertEqual(len(service.records()), 1)

    def test_duplicate_source_references_are_rejected_with_receipt(self):
        service = self.service()
        receipt = service.submit(fact_command(source_references=(SOURCE, SOURCE)))
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("DUPLICATE_SOURCE_REFERENCE", receipt.rejection_codes)
        self.assert_valid_receipt(service, receipt)

    def test_idempotency_key_reuse_with_changed_request_is_rejected(self):
        service = self.service(); service.submit(fact_command())
        changed = fact_command(command_id="changed", payload={
            "metric": "REVENUE", "value": 101, "unit": "INR_CRORE",
            "period": "2026-06-30", "basis": "STANDALONE",
        })
        receipt = service.submit(changed)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST", receipt.rejection_codes)

    def test_conflicting_facts_are_preserved_and_not_trusted(self):
        service = self.service(); first = service.submit(fact_command())
        conflict = fact_command(
            command_id="cmd-conflict", idempotency_key="idem-conflict",
            payload={"metric": "REVENUE", "value": 125, "unit": "INR_CRORE", "period": "2026-06-30", "basis": "STANDALONE"},
        )
        second = service.submit(conflict)
        self.assertEqual(second.status, WriteReceiptStatus.CONFLICT_RECORDED)
        self.assertEqual(len(service.records()), 2)
        self.assertEqual(service.get_record(first.record_id).validation_status, ValidationStatus.CONFLICTED)
        self.assertEqual(service.trusted_records(), ())

    def test_standalone_and_consolidated_are_distinct_semantic_identities(self):
        service = self.service(); service.submit(fact_command())
        consolidated = fact_command(
            command_id="cmd-con", idempotency_key="idem-con", semantic_key="revenue|2026-06-30|consolidated",
            payload={"metric": "REVENUE", "value": 125, "unit": "INR_CRORE", "period": "2026-06-30", "basis": "CONSOLIDATED"},
        )
        receipt = service.submit(consolidated)
        self.assertEqual(receipt.status, WriteReceiptStatus.ACCEPTED_PROVISIONAL)
        self.assertEqual(len(service.records()), 2)

    def test_fact_semantic_identity_must_include_period_and_basis(self):
        service = self.service()
        receipt = service.submit(fact_command(semantic_key="revenue"))
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("FACT_SEMANTIC_KEY_SCOPE_MISMATCH", receipt.rejection_codes)

    def test_restatement_supersedes_but_does_not_erase(self):
        service = self.service(); created = service.submit(fact_command())
        prior = service.get_record(created.record_id)
        restatement = fact_command(
            command_id="restatement", idempotency_key="restatement-idem",
            operation=WriteOperation.SUPERSEDE_RECORD,
            actor=actor(ActorType.HUMAN, (AuthorityScope.SUPERSEDE_INFORMATION, AuthorityScope.VERIFY_FACT), "reviewer-3"),
            payload={"metric": "REVENUE", "value": 102, "unit": "INR_CRORE", "period": "2026-06-30", "basis": "STANDALONE"},
            requested_validation_status=ValidationStatus.VERIFIED,
            supersedes_record_id=prior.record_id, expected_current_revision=prior.record_fingerprint,
        )
        receipt = service.submit(restatement)
        self.assertEqual(receipt.status, WriteReceiptStatus.ACCEPTED)
        self.assertEqual(len(service.records()), 2)
        self.assertEqual(service.get_record(prior.record_id).validation_status, ValidationStatus.SUPERSEDED)
        self.assertEqual(service.get_record(receipt.record_id).validation_status, ValidationStatus.VERIFIED)

    def test_stale_supersession_is_rejected(self):
        service = self.service(); created = service.submit(fact_command())
        restatement = fact_command(
            command_id="stale", idempotency_key="stale-idem", operation=WriteOperation.SUPERSEDE_RECORD,
            actor=actor(ActorType.HUMAN, (AuthorityScope.SUPERSEDE_INFORMATION,), "reviewer-4"),
            requested_validation_status=ValidationStatus.VERIFIED,
            supersedes_record_id=created.record_id, expected_current_revision="b" * 64,
        )
        receipt = service.submit(restatement)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("STALE_OR_MISSING_EXPECTED_REVISION", receipt.rejection_codes)

    def test_unauthorized_decision_write_is_rejected(self):
        service = self.service()
        command = fact_command(
            operation=WriteOperation.CREATE_DECISION_SNAPSHOT, information_class=InformationClass.DECISION,
            actor=actor(ActorType.AI_MODEL, (AuthorityScope.RECORD_INFERENCE,), "ai-cio"), source_references=(),
            semantic_key="decision|2026-09-09", payload={
                "decision": "BUY", "input_packet_fingerprint": "c" * 64, "reason_codes": ["TEST"],
            }, requested_validation_status=ValidationStatus.PENDING_REVIEW,
        )
        receipt = service.submit(command)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("DECISION_ORCHESTRATOR_REQUIRED", receipt.rejection_codes)

    def test_declared_request_fingerprint_detects_tampering(self):
        service = self.service(); original = fact_command()
        altered = dataclasses.replace(original, declared_request_fingerprint="0" * 64)
        receipt = service.submit(altered)
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("REQUEST_FINGERPRINT_MISMATCH", receipt.rejection_codes)

    def test_receipt_tampering_is_detected(self):
        service = self.service(); receipt = service.submit(fact_command())
        self.assertTrue(verify_receipt_fingerprint(receipt))
        self.assertFalse(verify_receipt_fingerprint(dataclasses.replace(receipt, status=WriteReceiptStatus.REJECTED)))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            receipt.status = WriteReceiptStatus.REJECTED

    def test_validation_lifecycle_is_complete_and_closed(self):
        self.assertEqual(
            {item.value for item in ValidationStatus},
            {"PROVISIONAL", "PENDING_REVIEW", "VERIFIED", "CONFLICTED", "REJECTED", "SUPERSEDED", "STALE"},
        )

    def test_every_rejection_has_an_auditable_receipt(self):
        service = self.service()
        receipt = service.submit(fact_command(source_references=()))
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertTrue(receipt.rejection_codes)
        self.assert_valid_receipt(service, receipt)

    def test_malformed_actor_is_rejected_instead_of_escaping_audit(self):
        service = self.service()
        receipt = service.submit(fact_command(actor="not-an-actor"))
        self.assertEqual(receipt.status, WriteReceiptStatus.REJECTED)
        self.assertIn("MALFORMED_COMMAND_CONTRACT", receipt.rejection_codes)
        self.assert_valid_receipt(service, receipt)

    def test_existing_eip_packet_contract_is_unchanged(self):
        self.assertEqual(
            tuple(field.name for field in dataclasses.fields(CausalFirstEIPDecisionPacket)),
            ("schema_version", "packet_id", "meta_assessment_id", "pre_inflection_preview_id",
             "causal_chain_id", "regime_assessment_id", "recognition_assessment_id",
             "expectation_gap_assessment_id", "normalized_valuation_assessment_id",
             "survivability_assessment_id", "component_fingerprints", "decision", "reason_codes",
             "all_components_ready", "creates_eip", "non_authority_statement"),
        )
        self.assertNotIn("modules.intelligence_write", CausalFirstEIPDecisionPacket.__module__)


if __name__ == "__main__":
    unittest.main()
