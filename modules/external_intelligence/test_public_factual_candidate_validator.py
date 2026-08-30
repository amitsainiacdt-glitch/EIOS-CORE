"""Offline validation tests for factual candidates."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_factual_candidate_extractor import PublicFactualCandidateExtractor
from modules.external_intelligence.public_factual_candidate_validator import PublicFactualCandidateValidator
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        now = datetime(2026, 8, 29, 16, tzinfo=timezone.utc)
        text = (
            "Alpha Engineering Limited received an order worth INR 125 crore on 28 August 2026. "
            "The company may expand capacity at its Pune facility. "
            "Alpha Engineering Limited did not receive regulatory approval for Product Z."
        )
        body = text.encode()
        registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("NSE", "NSE", ("nseindia.com",)),))
        receipt = PublicSourceAcquisitionLedger(root / "a.jsonl").record(
            acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="FACT_VALIDATION",
            source_url="https://www.nseindia.com/announcement/1", access_classification="PUBLIC", status="RETRIEVED",
            requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
            document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="Acquirer",
        )
        acquisition = TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url), receipt, RetrievedContent(receipt.source_url, 200, text, "text/plain", {}), body)
        extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(root / "e.jsonl"), clock=lambda: now + timedelta(seconds=1)).extract(acquisition, extraction_id="E1", recorder="Extractor")
        admission = PublicObservationAdmissionGate(registry).preview(acquisition=acquisition, extraction=extraction, observations=(), title="Filing", entity="Alpha Engineering Limited", category="EXCHANGE_FILING", confidence=80)
        candidates = PublicFactualCandidateExtractor().extract(acquisition=acquisition, extraction=extraction, admission=admission, subject_entity="Alpha Engineering Limited").candidates
        validator = PublicFactualCandidateValidator()
        order, capacity, approval = [validator.validate(candidate=item, acquisition=acquisition, extraction=extraction) for item in candidates]
        assert order.validated and order.reason_codes == ()
        assert capacity.decision.value == "DEFER" and "SUBJECT_NOT_IN_PASSAGE" in capacity.reason_codes
        assert "UNCERTAIN_STATEMENT_REQUIRES_CORROBORATION" in capacity.reason_codes
        assert approval.validated and approval.statement_posture == "NEGATED"

        altered = replace(candidates[0], source_passage=candidates[0].source_passage + " altered")
        rejected = validator.validate(candidate=altered, acquisition=acquisition, extraction=extraction)
        assert rejected.decision.value == "REJECT" and "SOURCE_PASSAGE_MISMATCH" in rejected.reason_codes

        authority_source = TrustedPublicSourceDefinition("CWC", "CWC", ("cwc.gov.in",), source_type="HYDROLOGY_AUTHORITY")
        hydro_acquisitions = PublicSourceAcquisitionLedger(root / "hydro-a.jsonl")
        hydro_candidate = replace(
            candidates[0], event_type="HYDROLOGY", subject_entity="INDIA AGRICULTURE",
            source_passage="Reservoir live storage was 82.070 BCM, 127.01 percent of normal storage.",
            passage_start=0, passage_end=76, matched_triggers=("Reservoir live storage was 82.070 BCM, 127.01 percent of normal storage",),
        )
        hydro_text = hydro_candidate.source_passage
        hydro_body = hydro_text.encode()
        hydro_receipt = hydro_acquisitions.record(
            acquisition_id="A-HYDRO", cycle_id="C1", job_id="J-HYDRO", research_intent="FACT_VALIDATION",
            source_url="https://cwc.gov.in/public/bulletin", status="RETRIEVED", requested_at=now, completed_at=now,
            http_status=200, content_type="text/plain", document_hash=sha256(hydro_body).hexdigest(), bytes_received=len(hydro_body), recorder="Acquirer",
        )
        hydro_acquisition = TrustedPublicAcquisitionResult(authority_source, hydro_receipt, RetrievedContent(hydro_receipt.source_url, 200, hydro_text, "text/plain", {}), hydro_body)
        hydro_extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(root / "hydro-e.jsonl"), clock=lambda: now + timedelta(seconds=1)).extract(hydro_acquisition, extraction_id="E-HYDRO", recorder="Extractor")
        hydro_candidate = replace(
            hydro_candidate, document_hash=hydro_receipt.document_hash,
            extracted_content_fingerprint=hydro_extraction.receipt.extracted_content_fingerprint,
            acquisition_id="A-HYDRO", extraction_id="E-HYDRO",
        )
        hydro_candidate = replace(hydro_candidate, candidate_id=sha256(f"{hydro_candidate.document_hash}\n0\n{len(hydro_text)}\nHYDROLOGY".encode()).hexdigest(), passage_end=len(hydro_text))
        assert validator.validate(candidate=hydro_candidate, acquisition=hydro_acquisition, extraction=hydro_extraction).validated

    print("PUBLIC FACTUAL CANDIDATE VALIDATOR: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
