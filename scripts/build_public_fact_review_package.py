"""Build one guarded, non-committing human-review package from a public document."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_factual_candidate_extractor import PublicFactualCandidateExtractor
from modules.external_intelligence.public_factual_candidate_validator import PublicFactualCandidateValidator
from modules.external_intelligence.public_factual_observation_review_package_builder import PublicFactualObservationReviewPackageBuilder
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry
from modules.observation.observation_persistence import ObservationPersistence


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Build a human-review package without committing Observations.")
    for name in ("package-id", "acquisition-id", "extraction-id", "cycle-id", "job-id", "research-intent", "url", "title", "entity", "category", "confidence", "acquisition-ledger-path", "extraction-ledger-path", "observation-path", "output-path", "recorder"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--include-event-type", action="append", required=True)
    args = parser.parse_args(argv)
    registry = TrustedPublicSourceRegistry.india_primary_sources()
    acquisition = TrustedPublicAcquisitionAdapter(registry, PublicSourceAcquisitionLedger(args.acquisition_ledger_path)).acquire(
        acquisition_id=args.acquisition_id, cycle_id=args.cycle_id, job_id=args.job_id,
        research_intent=args.research_intent, url=args.url, recorder=args.recorder,
        requested_at=datetime.now(timezone.utc),
    )
    if acquisition.retrieved_content is None:
        print(f"Acquisition blocked: {acquisition.receipt.error_message}")
        return 1
    extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(args.extraction_ledger_path)).extract(
        acquisition, extraction_id=args.extraction_id, recorder=args.recorder,
    )
    if extraction.extracted_text is None:
        print(f"Extraction blocked: {extraction.receipt.error_message}")
        return 1
    admission = PublicObservationAdmissionGate(registry).preview(
        acquisition=acquisition, extraction=extraction,
        observations=tuple(ObservationPersistence(args.observation_path).load()),
        title=args.title, entity=args.entity, category=args.category, confidence=args.confidence,
    )
    if not admission.admissible:
        print("Admission blocked: " + ", ".join(admission.reason_codes))
        return 1
    candidates = PublicFactualCandidateExtractor().extract(
        acquisition=acquisition, extraction=extraction, admission=admission, subject_entity=args.entity,
    )
    validator = PublicFactualCandidateValidator()
    validations = tuple(validator.validate(candidate=item, acquisition=acquisition, extraction=extraction) for item in candidates.candidates)
    builder = PublicFactualObservationReviewPackageBuilder()
    package = builder.build(
        package_id=args.package_id, candidate_preview=candidates, validations=validations,
        acquisition=acquisition, extraction=extraction, included_event_types=tuple(args.include_event_type),
    )
    output = Path(args.output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(builder.to_payload(package), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Review proposals: {len(package.proposals)}")
    print(f"Deferred for corroboration: {len(package.deferred_candidates)}")
    print(f"Excluded candidates: {len(package.excluded_candidate_ids)}")
    print(f"Package status: {package.package_status}")
    print(f"Package fingerprint: {package.package_fingerprint}")
    print(f"Review package: {output}")
    print("No Observation, Evidence, Meta conclusion, Signal, recommendation, or trade was created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
