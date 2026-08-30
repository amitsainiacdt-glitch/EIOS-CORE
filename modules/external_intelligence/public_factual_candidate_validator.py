"""Fail-closed validation of factual candidates before Observation admission."""

from __future__ import annotations

import re
from hashlib import sha256

from modules.external_intelligence.public_factual_candidate import PublicFactualCandidate
from modules.external_intelligence.public_factual_candidate_validation import PublicFactualCandidateValidation, PublicFactualCandidateValidationDecision
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionResult


class PublicFactualCandidateValidator:
    MECHANICS = {
        "ORDER_CONTRACT": re.compile(r"(?i)\b(?:order|contract|purchase order|letter of award|order book)\b"),
        "TENDER": re.compile(r"(?i)\b(?:tender|request for proposal|request for quotation|expression of interest|bids? invited)\b"),
        "REGULATORY_APPROVAL": re.compile(r"(?i)\b(?:approval|licen[cs]e|clearance|registration|authorisation|authorization|approved)\b"),
        "CAPACITY_CHANGE": re.compile(r"(?i)\b(?:capacity|plant|facility|production line)\b.*\b(?:expand\w*|commission\w*|debottleneck\w*|shutdown|closed|closure)\b|\b(?:expand\w*|commission\w*|debottleneck\w*|shutdown|closed|closure)\b.*\b(?:capacity|plant|facility|production line)\b"),
        "POLICY_REGULATION": re.compile(r"(?i)\b(?:policy|regulation|rule|tariff|duty|subsidy|guideline|circular)\b.*\b(?:issued|revised|introduced|amended|withdrawn|effective|notified)\b"),
        "SUPPLIER_CUSTOMER": re.compile(r"(?i)\b(?:supplier|customer|client|vendor|distributor)\b.*\b(?:added|appointed|selected|terminated|onboarded|agreement|contract)\b"),
        "EXECUTION_UPDATE": re.compile(r"(?i)\b(?:order|contract|project)\b.*\b(?:executed|execution|completed|delayed|cancelled|canceled)\b"),
        "WEATHER_ANOMALY": re.compile(r"(?i)\b(?:rainfall|monsoon|precipitation|dry spell|drought|SPI)\b"),
        "HYDROLOGY": re.compile(r"(?i)\b(?:reservoir|live storage|groundwater|soil moisture|stream flow|canal)\b.*\b(?:BCM|percent|normal|capacity|declin\w*|increas\w*|deficit|above|below)\b"),
        "CROP_PROGRESS": re.compile(r"(?i)\b(?:sowing|sown area|acreage|crop condition|production estimate|yield estimate|market arrivals)\b"),
        "SATELLITE_CROP_CONDITION": re.compile(r"(?i)\b(?:NDVI|NDWI|VCI|VHI|vegetation health|satellite|remote sensing)\b.*\b(?:crop|soil moisture|vegetation|stress|anomaly)\b"),
        "FERTILIZER_MARKET": re.compile(r"(?i)\b(?:urea|DAP|NPK|MOP|potash|fertili[sz]er)\b.*\b(?:sales|requirement|availability|inventory|allocation|application|shortage|subsidy)\b"),
        "FOOD_STOCK_POLICY": re.compile(r"(?i)\b(?:buffer stock|foodgrain stock|central pool|procurement|open market sale|OMSS|stock limit|export ban|import duty)\b"),
        "AGRI_PRICE_SUPPLY_CHAIN": re.compile(r"(?i)\b(?:mandi|farm gate|wholesale|retail|market arrival|cold storage|wastage)\b.*\b(?:price|margin|spread|disruption|shortage)\b"),
        "RURAL_DEMAND": re.compile(r"(?i)\b(?:rural demand|tractor sales|two-wheeler sales|rural FMCG|farm income|agricultural credit|microfinance)\b"),
        "GLOBAL_INPUT_COST": re.compile(r"(?i)\b(?:natural gas|ammonia|phosphate|phosphoric acid|potash|freight|fertili[sz]er import)\b.*\b(?:price|cost|supply|shipment|disruption)\b"),
    }
    AUTHORITY_SCOPED_EVENT_TYPES = frozenset(MECHANICS) - {"ORDER_CONTRACT", "TENDER", "REGULATORY_APPROVAL", "CAPACITY_CHANGE", "SUPPLIER_CUSTOMER", "EXECUTION_UPDATE"}
    AUTHORITY_SOURCE_TYPES = frozenset({"WEATHER_AUTHORITY", "EARTH_OBSERVATION_AUTHORITY", "AGRICULTURE_AUTHORITY", "HYDROLOGY_AUTHORITY", "FERTILIZER_AUTHORITY", "FOOD_STOCK_AUTHORITY", "AGRICULTURE_MARKET_DATA", "TRADE_POLICY_AUTHORITY"})

    def validate(self, *, candidate, acquisition, extraction):
        if not isinstance(candidate, PublicFactualCandidate):
            raise ValueError("candidate must be a PublicFactualCandidate")
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        if not isinstance(extraction, TrustedPublicDocumentExtractionResult):
            raise ValueError("extraction must be a TrustedPublicDocumentExtractionResult")
        reasons = []
        text = extraction.extracted_text
        acquired, extracted = acquisition.receipt, extraction.receipt
        if candidate.acquisition_id != acquired.acquisition_id or candidate.extraction_id != extracted.extraction_id:
            reasons.append("CANDIDATE_LINEAGE_MISMATCH")
        if candidate.document_hash != acquired.document_hash or candidate.extracted_content_fingerprint != extracted.extracted_content_fingerprint:
            reasons.append("CANDIDATE_FINGERPRINT_MISMATCH")
        passage_valid = (
            isinstance(text, str) and 0 <= candidate.passage_start < candidate.passage_end <= len(text)
            and text[candidate.passage_start:candidate.passage_end] == candidate.source_passage
        )
        if not passage_valid:
            reasons.append("SOURCE_PASSAGE_MISMATCH")
        expected_id = sha256(f"{candidate.document_hash}\n{candidate.passage_start}\n{candidate.passage_end}\n{candidate.event_type}".encode("utf-8")).hexdigest()
        if candidate.candidate_id != expected_id:
            reasons.append("CANDIDATE_ID_MISMATCH")

        authority_scope = (
            candidate.subject_entity.casefold() in {"india", "india agriculture"}
            and candidate.event_type in self.AUTHORITY_SCOPED_EVENT_TYPES
            and acquisition.source.source_type in self.AUTHORITY_SOURCE_TYPES
        )
        subject_grounded = candidate.subject_entity.casefold() in candidate.source_passage.casefold() or authority_scope
        if not subject_grounded:
            reasons.append("SUBJECT_NOT_IN_PASSAGE")
        mechanics = self.MECHANICS.get(candidate.event_type)
        mechanics_grounded = bool(mechanics and mechanics.search(candidate.source_passage))
        if not mechanics_grounded:
            reasons.append("EVENT_MECHANICS_INSUFFICIENT")
        if not candidate.matched_triggers or not all(trigger.casefold() in candidate.source_passage.casefold() for trigger in candidate.matched_triggers):
            reasons.append("TRIGGER_NOT_IN_PASSAGE")
        if candidate.statement_posture == "UNCERTAIN":
            reasons.append("UNCERTAIN_STATEMENT_REQUIRES_CORROBORATION")

        rejection = {"CANDIDATE_LINEAGE_MISMATCH", "CANDIDATE_FINGERPRINT_MISMATCH", "SOURCE_PASSAGE_MISMATCH", "CANDIDATE_ID_MISMATCH", "TRIGGER_NOT_IN_PASSAGE"}
        decision = PublicFactualCandidateValidationDecision.VALIDATED
        if rejection.intersection(reasons):
            decision = PublicFactualCandidateValidationDecision.REJECT
        elif reasons:
            decision = PublicFactualCandidateValidationDecision.DEFER
        return PublicFactualCandidateValidation(
            candidate.candidate_id, decision, tuple(dict.fromkeys(reasons)), candidate.event_type,
            candidate.statement_posture, subject_grounded, mechanics_grounded,
            decision == PublicFactualCandidateValidationDecision.DEFER,
            candidate.source_passage, candidate.document_hash, candidate.extracted_content_fingerprint,
        )


__all__ = ["PublicFactualCandidateValidator"]
