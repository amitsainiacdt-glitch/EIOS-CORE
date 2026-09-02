"""Read-only provenance, quality, completeness, and duplication admission gate."""

from __future__ import annotations

from hashlib import sha256

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionStatus
from modules.external_intelligence.public_observation_admission_preview import PublicObservationAdmissionDecision, PublicObservationAdmissionPreview
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.source_quality_service import SourceQualityService
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionResult
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry
from modules.observation.observation import Observation


class PublicObservationAdmissionGate:
    """Produces a decision only. It never creates or persists an Observation."""

    def __init__(self, registry, *, minimum_characters=50, allowed_quality_tiers=("TIER_1",)):
        if not isinstance(registry, TrustedPublicSourceRegistry):
            raise ValueError("registry must be a TrustedPublicSourceRegistry")
        if isinstance(minimum_characters, bool) or not isinstance(minimum_characters, int) or minimum_characters <= 0:
            raise ValueError("minimum_characters must be a positive integer")
        self.registry = registry
        self.minimum_characters = minimum_characters
        self.allowed_quality_tiers = tuple(allowed_quality_tiers)

    def preview(self, *, acquisition, extraction, observations=(), title, entity, category, confidence):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        if not isinstance(extraction, TrustedPublicDocumentExtractionResult):
            raise ValueError("extraction must be a TrustedPublicDocumentExtractionResult")
        if not all(isinstance(item, Observation) for item in observations):
            raise ValueError("observations must contain Observation values")
        title, entity, category = (self._text(value, name) for value, name in ((title, "title"), (entity, "entity"), (category, "category")))
        confidence = self._confidence(confidence)
        acquired, extracted = acquisition.receipt, extraction.receipt
        reasons = []

        if acquired.status != PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None:
            reasons.append("ACQUISITION_NOT_RETRIEVED")
        if acquired.access_classification != PublicSourceAcquisitionLedger.PUBLIC:
            reasons.append("NON_PUBLIC_SOURCE")
        try:
            source = self.registry.resolve(acquired.source_url)
        except (TypeError, ValueError):
            source = None
            reasons.append("SOURCE_NOT_TRUSTED")
        entity_domain = source.domains[0] if source and source.source_type == "COMPANY_PRIMARY" else None
        quality = SourceQualityService().classify(acquired.source_url, entity_domain=entity_domain)
        if quality.quality_tier not in self.allowed_quality_tiers:
            reasons.append("SOURCE_QUALITY_INSUFFICIENT")

        fingerprint = PublicSourceAcquisitionLedger.receipt_fingerprint(acquired)
        if extracted.acquisition_id != acquired.acquisition_id or extracted.acquisition_fingerprint != fingerprint or extracted.document_hash != acquired.document_hash:
            reasons.append("EXTRACTION_ACQUISITION_MISMATCH")
        text = extraction.extracted_text
        if extracted.status == PublicDocumentExtractionStatus.FAILED or text is None:
            reasons.append("EXTRACTION_FAILED")
        elif sha256(text.encode("utf-8")).hexdigest() != extracted.extracted_content_fingerprint:
            reasons.append("EXTRACTED_CONTENT_MISMATCH")
        if extracted.status == PublicDocumentExtractionStatus.PARTIAL:
            reasons.append("EXTRACTION_PARTIAL")
        if not isinstance(text, str) or len(text.strip()) < self.minimum_characters:
            reasons.append("CONTENT_INSUFFICIENT")

        duplicates = tuple(
            index for index, observation in enumerate(observations)
            if observation.provenance is not None and (
                (acquired.document_hash and observation.provenance.document_hash == acquired.document_hash)
                or (extracted.extracted_content_fingerprint and observation.provenance.content_fingerprint == extracted.extracted_content_fingerprint)
            )
        )
        if duplicates:
            reasons.append("DUPLICATE_EXISTING_OBSERVATION")

        reject_codes = {"ACQUISITION_NOT_RETRIEVED", "NON_PUBLIC_SOURCE", "SOURCE_NOT_TRUSTED", "EXTRACTION_ACQUISITION_MISMATCH", "EXTRACTION_FAILED", "EXTRACTED_CONTENT_MISMATCH", "DUPLICATE_EXISTING_OBSERVATION"}
        decision = PublicObservationAdmissionDecision.ADMIT
        if reject_codes.intersection(reasons):
            decision = PublicObservationAdmissionDecision.REJECT
        elif reasons:
            decision = PublicObservationAdmissionDecision.DEFER
        return PublicObservationAdmissionPreview(
            decision, tuple(dict.fromkeys(reasons)), acquired.acquisition_id, extracted.extraction_id,
            source.source_id if source else None, quality.quality_tier, acquired.document_hash,
            extracted.extracted_content_fingerprint, extracted.character_count, duplicates,
            title, entity, category, confidence,
        )

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @staticmethod
    def _confidence(value):
        if isinstance(value, bool):
            raise ValueError("confidence must be between 0 and 100")
        try:
            value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("confidence must be between 0 and 100") from exc
        if not 0 <= value <= 100:
            raise ValueError("confidence must be between 0 and 100")
        return value


__all__ = ["PublicObservationAdmissionGate"]
