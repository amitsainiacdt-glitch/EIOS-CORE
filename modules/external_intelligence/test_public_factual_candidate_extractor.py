"""Offline tests for deterministic, source-grounded factual candidates."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_factual_candidate_extractor import PublicFactualCandidateExtractor
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def main():
    with TemporaryDirectory() as directory:
        now = datetime(2026, 8, 29, 15, tzinfo=timezone.utc)
        text = (
            "May " + ("background " * 70) +
            "Alpha Engineering Limited received an order worth INR 125 crore from Metro Rail Corporation on 28 August 2026. "
            "The company may expand capacity at its Pune facility by December 2027. "
            "It did not receive regulatory approval for the proposed product. "
            "Ordinary background information contains no event language."
        )
        body = text.encode()
        root = Path(directory)
        registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("NSE", "NSE", ("nseindia.com",)),))
        receipt = PublicSourceAcquisitionLedger(root / "a.jsonl").record(
            acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="EARLY_FACT",
            source_url="https://www.nseindia.com/announcement/1", access_classification="PUBLIC", status="RETRIEVED",
            requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
            document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="Acquirer",
        )
        acquisition = TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url), receipt, RetrievedContent(receipt.source_url, 200, text, "text/plain", {}), body)
        extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(root / "e.jsonl"), clock=lambda: now + timedelta(seconds=1)).extract(acquisition, extraction_id="E1", recorder="Extractor")
        admission = PublicObservationAdmissionGate(registry).preview(acquisition=acquisition, extraction=extraction, observations=(), title="Filing", entity="Alpha Engineering Limited", category="EXCHANGE_FILING", confidence=80)
        preview = PublicFactualCandidateExtractor().extract(acquisition=acquisition, extraction=extraction, admission=admission, subject_entity="Alpha Engineering Limited")
        event_types = [item.event_type for item in preview.candidates]
        assert event_types == ["ORDER_CONTRACT", "CAPACITY_CHANGE", "REGULATORY_APPROVAL"], event_types
        order, capacity, approval = preview.candidates
        assert order.statement_posture == "ASSERTED" and order.explicit_amounts == ("INR 125 crore",)
        assert order.explicit_dates == ("28 August 2026",)
        assert "Alpha Engineering Limited" in order.mentioned_entities
        assert capacity.statement_posture == "UNCERTAIN"
        assert approval.statement_posture == "NEGATED"
        assert PublicFactualCandidateExtractor.UNCERTAIN.search("Meeting May 20 to 22, 2026") is None
        for item in preview.candidates:
            assert text[item.passage_start:item.passage_end] == item.source_passage
            assert item.document_hash == receipt.document_hash

        vocabulary_examples = {
            "WEATHER_ANOMALY": "Monsoon rainfall was deficient by 18 percent.",
            "HYDROLOGY": "Reservoir live storage decreased below normal by 20 percent.",
            "CROP_PROGRESS": "Sown area decreased by 12 percent.",
            "SATELLITE_CROP_CONDITION": "NDVI crop condition anomaly indicated stress.",
            "FERTILIZER_MARKET": "DAP availability and fertilizer sales decreased.",
            "FOOD_STOCK_POLICY": "Buffer stock released 2 million tonnes.",
            "AGRI_PRICE_SUPPLY_CHAIN": "Mandi price increased after a supply disruption.",
            "RURAL_DEMAND": "Tractor sales decreased as rural demand declined.",
            "GLOBAL_INPUT_COST": "Natural gas price increased after supply disruption.",
        }
        import re
        for event_type, example in vocabulary_examples.items():
            assert any(re.search(pattern, example, re.IGNORECASE | re.DOTALL) for pattern in PublicFactualCandidateExtractor.EVENT_PATTERNS[event_type]), event_type
        assert any(re.search(pattern, "Subdued rainfall activity is likely to continue.", re.IGNORECASE | re.DOTALL) for pattern in PublicFactualCandidateExtractor.EVENT_PATTERNS["WEATHER_ANOMALY"])
        assert not any(re.search(pattern, "Apply fertilizer to rice after rainfall.", re.IGNORECASE | re.DOTALL) for pattern in PublicFactualCandidateExtractor.EVENT_PATTERNS["FERTILIZER_MARKET"])

        quiet_text = "This document provides general institutional background and contact information only."
        quiet_body = quiet_text.encode()
        quiet_receipt = PublicSourceAcquisitionLedger(root / "a2.jsonl").record(
            acquisition_id="A2", cycle_id="C1", job_id="J2", research_intent="EARLY_FACT",
            source_url="https://www.nseindia.com/about", access_classification="PUBLIC", status="RETRIEVED",
            requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
            document_hash=sha256(quiet_body).hexdigest(), bytes_received=len(quiet_body), recorder="Acquirer",
        )
        quiet_acquisition = TrustedPublicAcquisitionResult(registry.resolve(quiet_receipt.source_url), quiet_receipt, RetrievedContent(quiet_receipt.source_url, 200, quiet_text, "text/plain", {}), quiet_body)
        quiet_extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(root / "e2.jsonl"), clock=lambda: now + timedelta(seconds=1)).extract(quiet_acquisition, extraction_id="E2", recorder="Extractor")
        quiet_admission = PublicObservationAdmissionGate(registry).preview(acquisition=quiet_acquisition, extraction=quiet_extraction, observations=(), title="About", entity="NSE", category="PUBLIC_PAGE", confidence=50)
        quiet = PublicFactualCandidateExtractor().extract(acquisition=quiet_acquisition, extraction=quiet_extraction, admission=quiet_admission, subject_entity="NSE")
        assert quiet.candidate_count == 0 and quiet.warnings

    print("PUBLIC FACTUAL CANDIDATE EXTRACTOR: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
