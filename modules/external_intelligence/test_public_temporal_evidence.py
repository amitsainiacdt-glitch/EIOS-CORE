"""Offline tests for reviewed-fact Temporal Evidence and its repository."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.public_temporal_evidence_repository import PublicTemporalEvidenceRepository
from modules.external_intelligence.public_temporal_evidence_service import PublicTemporalEvidenceService
from modules.observation.observation import Observation, ObservationProvenance


def main():
    now = datetime(2026, 8, 29, 18, tzinfo=timezone.utc)

    def observation(index, posture, published_offset=None):
        published = None if published_offset is None else now + timedelta(days=published_offset)
        return Observation(
            f"Order {index}", f"Exact reviewed order passage {index}.", "https://www.nseindia.com/announcement",
            "PUBLIC_FACT_ORDER_CONTRACT", "Alpha Limited", 80, now + timedelta(days=index),
            ObservationProvenance(
                retrieved_at=now + timedelta(days=index), published_at=published,
                source_url="https://www.nseindia.com/announcement", observation_fingerprint=f"{index:064x}",
                document_hash=f"{index + 10:064x}", public_fact_candidate_id=f"C-{index}",
                public_fact_event_type="ORDER_CONTRACT", public_fact_statement_posture=posture,
                public_fact_proposal_id=f"P-{index}", public_fact_review_id=f"R-{index}",
            ),
        )

    service = PublicTemporalEvidenceService()
    later_known = service.record_from_observation(observation(2, "NEGATED", -2))
    earlier_known = service.record_from_observation(observation(1, "ASSERTED", -5))
    fallback = service.record_from_observation(observation(3, "ASSERTED", None))
    series = service.build_series((fallback, later_known, earlier_known))
    assert [item.candidate_id for item in series.records] == ["C-1", "C-2", "C-3"]
    assert series.record_count == 3 and series.asserted_count == 2 and series.negated_count == 1
    assert series.warnings == ("One or more records lack publication/filing time and use known-at time.",)

    with TemporaryDirectory() as directory:
        repository = PublicTemporalEvidenceRepository(Path(directory) / "temporal.jsonl")
        assert repository.add(earlier_known) == earlier_known
        repository.add(later_known); repository.add(fallback)
        assert repository.all() == (earlier_known, later_known, fallback)
        try:
            repository.add(earlier_known)
        except ValueError as exc:
            assert "already exists" in str(exc)
        else:
            raise AssertionError("duplicate Temporal Evidence accepted")

    legacy = Observation("Legacy", "No fact lineage", "Archive", "General", "Alpha", 50, now)
    try:
        service.record_from_observation(legacy)
    except ValueError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("legacy Observation entered reviewed-fact Temporal Evidence")

    print("PUBLIC TEMPORAL EVIDENCE: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
