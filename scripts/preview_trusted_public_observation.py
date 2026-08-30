"""Run a live public intake canary and stop at the read-only admission decision."""

import argparse
import sys
from datetime import datetime, timezone

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_factual_candidate_extractor import PublicFactualCandidateExtractor
from modules.external_intelligence.public_factual_candidate_validator import PublicFactualCandidateValidator
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry
from modules.observation.observation_persistence import ObservationPersistence


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Preview one trusted public document without committing an Observation.")
    for name in ("acquisition-id", "extraction-id", "cycle-id", "job-id", "research-intent", "url", "title", "entity", "category", "confidence", "acquisition-ledger-path", "extraction-ledger-path", "observation-path", "recorder"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args(argv)
    registry = TrustedPublicSourceRegistry.india_primary_sources()
    acquisition = TrustedPublicAcquisitionAdapter(registry, PublicSourceAcquisitionLedger(args.acquisition_ledger_path)).acquire(
        acquisition_id=args.acquisition_id, cycle_id=args.cycle_id, job_id=args.job_id,
        research_intent=args.research_intent, url=args.url, recorder=args.recorder,
        requested_at=datetime.now(timezone.utc),
    )
    print(f"Acquisition: {acquisition.receipt.status.value}")
    if acquisition.retrieved_content is None:
        print(f"Decision: REJECT ({acquisition.receipt.error_code})")
        return 1
    extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(args.extraction_ledger_path)).extract(
        acquisition, extraction_id=args.extraction_id, recorder=args.recorder
    )
    print(f"Extraction: {extraction.receipt.status.value} ({extraction.receipt.character_count} characters)")
    preview = PublicObservationAdmissionGate(registry).preview(
        acquisition=acquisition, extraction=extraction,
        observations=tuple(ObservationPersistence(args.observation_path).load()),
        title=args.title, entity=args.entity, category=args.category, confidence=args.confidence,
    )
    print(f"Decision: {preview.decision.value}")
    print("Reasons: " + (", ".join(preview.reason_codes) if preview.reason_codes else "none"))
    print(f"Existing duplicates: {len(preview.duplicate_observation_indexes)}")
    if preview.admissible:
        factual = PublicFactualCandidateExtractor().extract(
            acquisition=acquisition, extraction=extraction, admission=preview,
            subject_entity=args.entity,
        )
        print(f"Factual candidates: {factual.candidate_count}")
        validator = PublicFactualCandidateValidator()
        for candidate in factual.candidates[:10]:
            validation = validator.validate(candidate=candidate, acquisition=acquisition, extraction=extraction)
            reasons = ",".join(validation.reason_codes) if validation.reason_codes else "none"
            print(f"- {candidate.event_type} [{candidate.statement_posture}] {validation.decision.value} ({reasons}): {candidate.source_passage[:180]}")
        if factual.candidate_count > 10:
            print(f"- {factual.candidate_count - 10} additional candidates omitted from display")
        for warning in factual.warnings:
            print(f"Candidate warning: {warning}")
    print("Preview only. No Observation, Evidence, Signal, Catalyst, Opportunity, or Meta conclusion was created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
