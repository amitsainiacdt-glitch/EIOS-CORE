"""Durability and corruption tests for the controlled-write journal."""

import json
import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.intelligence_write import (
    ActorType, AuthorityScope, ControlledIntelligenceWriteJournal,
    ControlledIntelligenceWriteService, ValidationStatus, WriteOperation,
    WriteReceiptStatus,
)
from modules.intelligence_write.test_controlled_intelligence_write_service import NOW, actor, fact_command


class ControlledWritePersistenceTests(unittest.TestCase):
    def open(self, path):
        journal = ControlledIntelligenceWriteJournal(path)
        return ControlledIntelligenceWriteService(clock=lambda: NOW, journal=journal)

    def test_accepted_and_rejected_receipts_survive_restart(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            service = self.open(path)
            accepted = service.submit(fact_command())
            rejected = service.submit(fact_command(
                command_id="bad", idempotency_key="bad-idem", source_references=(),
            ))
            restored = self.open(path)
            self.assertEqual(restored.receipts(), (accepted, rejected))
            self.assertEqual(restored.records(), service.records())
            self.assertEqual(rejected.status, WriteReceiptStatus.REJECTED)

    def test_idempotency_survives_restart(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            first = self.open(path).submit(fact_command())
            restored = self.open(path)
            replay = restored.submit(fact_command())
            self.assertEqual(replay.status, WriteReceiptStatus.DUPLICATE_NO_CHANGE)
            self.assertEqual(replay.record_id, first.record_id)
            self.assertEqual(len(restored.records()), 1)
            self.assertEqual(len(self.open(path).receipts()), 2)

    def test_conflict_and_trusted_block_survive_restart(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            service = self.open(path)
            first = service.submit(fact_command())
            second = service.submit(fact_command(
                command_id="conflict", idempotency_key="conflict-idem",
                payload={"metric": "REVENUE", "value": 125, "unit": "INR_CRORE", "period": "2026-06-30", "basis": "STANDALONE"},
            ))
            restored = self.open(path)
            self.assertEqual(second.status, WriteReceiptStatus.CONFLICT_RECORDED)
            self.assertEqual(restored.get_record(first.record_id).validation_status, ValidationStatus.CONFLICTED)
            self.assertEqual(restored.trusted_records(), ())

    def test_supersession_history_survives_restart(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            service = self.open(path)
            created = service.submit(fact_command())
            prior = service.get_record(created.record_id)
            restatement = fact_command(
                command_id="restated", idempotency_key="restated-idem",
                operation=WriteOperation.SUPERSEDE_RECORD,
                actor=actor(ActorType.HUMAN, (AuthorityScope.SUPERSEDE_INFORMATION, AuthorityScope.VERIFY_FACT), "reviewer"),
                payload={"metric": "REVENUE", "value": 102, "unit": "INR_CRORE", "period": "2026-06-30", "basis": "STANDALONE"},
                requested_validation_status=ValidationStatus.VERIFIED,
                supersedes_record_id=prior.record_id,
                expected_current_revision=prior.record_fingerprint,
            )
            replaced = service.submit(restatement)
            restored = self.open(path)
            self.assertEqual(len(restored.records()), 2)
            self.assertEqual(restored.get_record(prior.record_id).validation_status, ValidationStatus.SUPERSEDED)
            self.assertEqual(restored.get_record(replaced.record_id).validation_status, ValidationStatus.VERIFIED)

    def test_changed_entry_content_fails_closed(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            self.open(path).submit(fact_command())
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["receipt"]["status"] = "REJECTED"
            path.write_text(json.dumps(raw) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "fingerprint"):
                self.open(path)

    def test_missing_first_entry_breaks_sequence_chain(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            service = self.open(path)
            service.submit(fact_command())
            service.submit(fact_command(command_id="again", idempotency_key="again"))
            lines = path.read_text(encoding="utf-8").splitlines()
            path.write_text(lines[1] + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "sequence|chain"):
                self.open(path)

    def test_truncated_entry_fails_closed(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "journal.jsonl"
            self.open(path).submit(fact_command())
            content = path.read_text(encoding="utf-8")
            path.write_text(content[:-20], encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid controlled-write journal"):
                self.open(path)


if __name__ == "__main__":
    unittest.main()
