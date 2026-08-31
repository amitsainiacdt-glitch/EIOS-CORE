"""Deterministic passage detection; no event validation or investment analysis."""

from __future__ import annotations

import re
from hashlib import sha256

from modules.external_intelligence.public_factual_candidate import PublicFactualCandidate, PublicFactualCandidatePreview
from modules.external_intelligence.public_observation_admission_preview import PublicObservationAdmissionPreview
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionResult


class PublicFactualCandidateExtractor:
    MAX_PASSAGE_CHARACTERS = 600
    EVENT_PATTERNS = {
        "ORDER_CONTRACT": (r"\b(?:awarded|received|secured|won)\b.{0,80}\b(?:order|contract|purchase order)\b", r"\border book\b", r"\bletter of award\b"),
        "TENDER": (r"\b(?:tender|request for proposal|request for quotation|expression of interest)\b", r"\b(?:bid|bids) invited\b"),
        "REGULATORY_APPROVAL": (r"\b(?:approval|licen[cs]e|clearance|registration|authorisation|authorization)\b.{0,80}\b(?:granted|received|approved|issued)\b", r"\b(?:receive|received|obtain|obtained|secure|secured|deny|denied|reject|rejected)\b.{0,80}\b(?:approval|licen[cs]e|clearance|registration|authorisation|authorization)\b", r"\b(?:approved|authorised|authorized) by\b"),
        "CAPACITY_CHANGE": (r"\b(?:capacity|plant|facility|production line)\b.{0,100}\b(?:expand|expansion|commissioned|commissioning|debottleneck|shutdown|closed|closure)\w*\b", r"\b(?:expand|expansion|commissioned|commissioning|debottleneck|shutdown|closed|closure)\w*\b.{0,100}\b(?:capacity|plant|facility|production line)\b"),
        "POLICY_REGULATION": (r"\b(?:policy|regulation|rule|tariff|duty|subsidy|guideline|circular)\b.{0,100}\b(?:issued|revised|introduced|amended|withdrawn|effective|notified)\b",),
        "SUPPLIER_CUSTOMER": (r"\b(?:supplier|customer|client|vendor|distributor)\b.{0,100}\b(?:added|appointed|selected|terminated|onboarded|agreement|contract)\b",),
        "EXECUTION_UPDATE": (r"\b(?:order|contract|project)\b.{0,100}\b(?:executed|execution|completed|delayed|cancelled|canceled)\b",),
        "WEATHER_ANOMALY": (r"\b(?:rainfall|monsoon|precipitation)\b.{0,100}\b(?:deficit|deficient|below normal|above normal|excess|delayed|subdued)\b", r"\b(?:deficit|deficient|below normal|above normal|excess|delayed|subdued)\b.{0,100}\b(?:rainfall|monsoon|precipitation)\b", r"\b(?:dry spell|drought|standardized precipitation index|SPI)\b"),
        "HYDROLOGY": (r"\b(?:reservoir|groundwater|soil moisture|stream flow|canal storage|live storage)\b.{0,100}\b(?:declined|decreased|increased|deficit|below|above|percent|normal)\b",),
        "CROP_PROGRESS": (r"\b(?:sowing|sown area|acreage|crop condition|production estimate|yield estimate|market arrivals)\b.{0,100}\b(?:increased|decreased|delayed|ahead|behind|revised|lakh|million|percent)\b",),
        "SATELLITE_CROP_CONDITION": (r"\b(?:NDVI|NDWI|VCI|VHI|vegetation health|satellite.{0,30}crop|remote sensing.{0,30}crop)\b.{0,120}\b(?:anomaly|decline|stress|improved|deteriorated|normal)\b",),
        "FERTILIZER_MARKET": (r"\b(?:urea|DAP|NPK|MOP|potash|fertili[sz]er)\b.{0,120}\b(?:sales|requirement|availability|inventory|allocation|shortage|subsidy)\b",),
        "FOOD_STOCK_POLICY": (r"\b(?:buffer stock|foodgrain stock|central pool|procurement|open market sale|OMSS|stock limit|export ban|import duty)\b.{0,120}\b(?:released|increased|decreased|imposed|revised|procured|available|million|lakh)\b",),
        "AGRI_PRICE_SUPPLY_CHAIN": (r"\b(?:mandi price|farm gate|wholesale price|retail price|market arrival|cold storage|crop wastage)\b.{0,120}\b(?:increased|decreased|margin|spread|disruption|shortage)\b",),
        "RURAL_DEMAND": (r"\b(?:rural demand|tractor sales|two-wheeler sales|rural FMCG|farm income|agricultural credit|microfinance delinquency)\b.{0,120}\b(?:increased|decreased|growth|decline|stress|recovery)\b",),
        "GLOBAL_INPUT_COST": (r"\b(?:natural gas|ammonia|phosphate|phosphoric acid|potash|freight|fertili[sz]er import)\b.{0,120}\b(?:price|cost|supply|shipment|disruption|increased|decreased)\b",),
    }
    AMOUNT = re.compile(r"(?i)(?:₹|INR|Rs\.?|USD|US\$|\$|EUR|€)\s*[\d,]+(?:\.\d+)?\s*(?:crore|cr|lakh|million|billion|mn|bn)?|\b[\d,]+(?:\.\d+)?\s*(?:crore|lakh|million|billion)\b")
    DATE = re.compile(r"(?i)\b(?:\d{1,2}[-/](?:\d{1,2}|[A-Za-z]{3,9})[-/]\d{2,4}|\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4})\b")
    COMPANY = re.compile(r"\b[A-Z][A-Za-z&.'-]*(?:\s+[A-Z][A-Za-z&.'-]*){0,5}\s+(?:Limited|Ltd\.?|Corporation|Corp\.?|Industries|Bank)\b")
    SENTENCE = re.compile(r"\S(?:.*?)(?:[.!?]+(?=\s|$)|$)", re.DOTALL)
    NEGATED = re.compile(r"(?i)\b(?:not|no|never|denied|rejected|cancelled|canceled|failed to|did not|has not|have not)\b")
    UNCERTAIN = re.compile(r"(?i)\b(?:(?:may(?!\s+(?:\d{1,2}|20\d{2})\b))|might|could|likely|forecast|forecasted|proposed|expected|plans? to|intends? to|subject to)\b")

    def extract(self, *, acquisition, extraction, admission, subject_entity):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        if not isinstance(extraction, TrustedPublicDocumentExtractionResult):
            raise ValueError("extraction must be a TrustedPublicDocumentExtractionResult")
        if not isinstance(admission, PublicObservationAdmissionPreview) or not admission.admissible:
            raise ValueError("candidate extraction requires an ADMIT preview")
        subject_entity = self._text(subject_entity, "subject_entity")
        acquired, extracted = acquisition.receipt, extraction.receipt
        if admission.acquisition_id != acquired.acquisition_id or admission.extraction_id != extracted.extraction_id:
            raise ValueError("admission does not bind to the supplied acquisition and extraction")
        if admission.document_hash != acquired.document_hash or admission.extracted_content_fingerprint != extracted.extracted_content_fingerprint:
            raise ValueError("admission fingerprints do not match the supplied document")
        text = extraction.extracted_text
        if not isinstance(text, str) or not text:
            raise ValueError("admitted extraction must contain text")

        candidates = []
        for sentence in self.SENTENCE.finditer(text):
            sentence_passage = sentence.group(0).strip()
            if not sentence_passage:
                continue
            leading = len(sentence.group(0)) - len(sentence.group(0).lstrip())
            sentence_start = sentence.start() + leading
            sentence_end = sentence_start + len(sentence_passage)
            for event_type, patterns in self.EVENT_PATTERNS.items():
                matches = tuple(match for pattern in patterns if (match := re.search(pattern, sentence_passage, re.IGNORECASE | re.DOTALL)))
                if not matches:
                    continue
                start, end, passage = self._bounded_passage(
                    text, sentence_start, sentence_end,
                    sentence_start + matches[0].start(), sentence_start + matches[0].end(),
                )
                triggers = tuple(match.group(0) for match in matches)
                posture = "NEGATED" if self.NEGATED.search(passage) else ("UNCERTAIN" if self.UNCERTAIN.search(passage) else "ASSERTED")
                mentioned = list(dict.fromkeys(self.COMPANY.findall(passage)))
                if subject_entity.casefold() in passage.casefold() and subject_entity not in mentioned:
                    mentioned.insert(0, subject_entity)
                identity = f"{acquired.document_hash}\n{start}\n{end}\n{event_type}"
                candidates.append(PublicFactualCandidate(
                    1, sha256(identity.encode("utf-8")).hexdigest(), event_type, posture,
                    subject_entity, tuple(mentioned), tuple(self.AMOUNT.findall(passage)),
                    tuple(self.DATE.findall(passage)), passage, start, end, triggers,
                    acquired.acquisition_id, extracted.extraction_id, acquired.source_url,
                    acquired.document_hash, extracted.extracted_content_fingerprint,
                    extracted.extraction_method,
                ))
        candidates.sort(key=lambda item: (item.passage_start, item.event_type, item.candidate_id))
        warnings = () if candidates else ("No configured factual-event trigger was found; this is not negative evidence.",)
        return PublicFactualCandidatePreview(acquired.acquisition_id, extracted.extraction_id, len(candidates), tuple(candidates), warnings)

    @classmethod
    def _bounded_passage(cls, text, sentence_start, sentence_end, trigger_start, trigger_end):
        if sentence_end - sentence_start <= cls.MAX_PASSAGE_CHARACTERS:
            return sentence_start, sentence_end, text[sentence_start:sentence_end]
        allowance = cls.MAX_PASSAGE_CHARACTERS - (trigger_end - trigger_start)
        start = max(sentence_start, trigger_start - allowance // 2)
        end = min(sentence_end, start + cls.MAX_PASSAGE_CHARACTERS)
        start = max(sentence_start, end - cls.MAX_PASSAGE_CHARACTERS)
        if start > sentence_start:
            space = text.find(" ", start, trigger_start)
            if space >= 0:
                start = space + 1
        if end < sentence_end:
            space = text.rfind(" ", trigger_end, end)
            if space >= 0:
                end = space
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        return start, end, text[start:end]

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["PublicFactualCandidateExtractor"]
