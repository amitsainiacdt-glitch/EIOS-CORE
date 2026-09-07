"""Governed contract for alternate delivery of a blocked official document."""

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol
from urllib.parse import urlsplit

from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


@dataclass(frozen=True)
class OfficialDocumentDeliveryProvenance:
    provider_id: str
    delivery_url: str
    requested_official_url: str


class OfficialDocumentFallbackProvider(Protocol):
    def acquire_after_failure(self, primary_result, **acquisition_request): ...


@dataclass(frozen=True)
class FallbackAcquisitionResult(TrustedPublicAcquisitionResult):
    delivery_provenance: OfficialDocumentDeliveryProvenance


def validate_fallback_delivery(result, *, requested_url: str):
    """Fail closed unless alternate delivery retains an auditable source chain."""
    if result is None or result.document_bytes is None or result.retrieved_content is None:
        raise ValueError("fallback provider returned no document")
    provenance = getattr(result, "delivery_provenance", None)
    if not isinstance(provenance, OfficialDocumentDeliveryProvenance):
        raise ValueError("fallback delivery provenance is required")
    if not provenance.provider_id.strip():
        raise ValueError("fallback provider identity is required")
    if provenance.requested_official_url != requested_url:
        raise ValueError("fallback delivery changed the requested official URL")
    scheme = urlsplit(provenance.delivery_url).scheme.casefold()
    local_inbox = provenance.provider_id in {
        "EIOS_GOVERNED_LOCAL_INBOX", "EIOS_CORROBORATED_BROWSER_CAPTURE",
    } and scheme == "eios-local"
    if scheme != "https" and not local_inbox:
        raise ValueError("fallback delivery must use HTTPS or the governed local inbox")
    receipt = result.receipt
    if receipt.requested_url != requested_url:
        raise ValueError("fallback receipt does not preserve the official URL")
    if sha256(result.document_bytes).hexdigest() != receipt.document_hash:
        raise ValueError("fallback bytes do not match the acquisition receipt")
    if len(result.document_bytes) != receipt.bytes_received:
        raise ValueError("fallback byte count does not match the acquisition receipt")
    return result


class ChainedOfficialDocumentFallback:
    def __init__(self, *providers):
        self.providers = tuple(providers)

    def acquire_after_failure(self, primary_result, **request):
        for provider in self.providers:
            result = provider.acquire_after_failure(primary_result, **request)
            if result is not None:
                return result
        return None


__all__ = ["ChainedOfficialDocumentFallback", "FallbackAcquisitionResult", "OfficialDocumentDeliveryProvenance", "OfficialDocumentFallbackProvider", "validate_fallback_delivery"]
