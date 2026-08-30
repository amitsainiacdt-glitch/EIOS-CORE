"""Guarded HTTP acquisition from explicitly trusted public sources."""

from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from urllib.parse import urljoin, urlsplit

import requests

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionReceipt
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


@dataclass(frozen=True)
class TrustedPublicAcquisitionResult:
    source: TrustedPublicSourceDefinition
    receipt: PublicSourceAcquisitionReceipt
    retrieved_content: RetrievedContent | None
    document_bytes: bytes | None


class TrustedPublicAcquisitionAdapter:
    REDIRECT_STATUSES = {301, 302, 303, 307, 308}

    def __init__(self, registry, ledger, *, transport=requests.get, address_resolver=None, clock=None, timeout=15.0, max_redirects=5):
        if not isinstance(registry, TrustedPublicSourceRegistry): raise ValueError("registry must be a TrustedPublicSourceRegistry")
        if not isinstance(ledger, PublicSourceAcquisitionLedger): raise ValueError("ledger must be a PublicSourceAcquisitionLedger")
        if timeout <= 0: raise ValueError("timeout must be positive")
        if isinstance(max_redirects, bool) or not isinstance(max_redirects, int) or max_redirects < 0: raise ValueError("max_redirects must be a non-negative integer")
        self.registry, self.ledger = registry, ledger
        self.transport = transport
        self.address_resolver = address_resolver or self._resolve_addresses
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.timeout, self.max_redirects = float(timeout), max_redirects

    def acquire(self, *, acquisition_id, cycle_id, job_id, research_intent, url, recorder, requested_at=None, source_document_id=None):
        requested_at = requested_at or self.clock()
        source = self.registry.resolve(url)
        current_url = url.strip()
        try:
            self._validate_network_target(url)
            response = None
            for redirect_count in range(self.max_redirects + 1):
                response = self.transport(current_url, timeout=self.timeout, allow_redirects=False)
                status = self._status(response)
                if status not in self.REDIRECT_STATUSES:
                    break
                if redirect_count >= self.max_redirects:
                    raise ValueError("redirect limit exceeded")
                location = self._header(response, "Location")
                if not location:
                    raise ValueError("redirect response has no Location header")
                next_url = urljoin(current_url, location)
                redirected_source = self.registry.resolve(next_url)
                if redirected_source.source_id != source.source_id:
                    raise ValueError("redirect leaves the approved public source")
                self._validate_network_target(next_url)
                current_url = next_url
            status = self._status(response)
            if status >= 400:
                return self._failure(
                    source, acquisition_id, cycle_id, job_id, research_intent,
                    url, current_url, recorder, requested_at, status,
                    f"HTTP_{status}", f"Public source returned HTTP {status}.",
                )
            if status in self.REDIRECT_STATUSES:
                raise ValueError("unresolved redirect response")
            body = self._body(response)
            if not body:
                raise ValueError("public source returned an empty document")
            completed_at = self.clock()
            content_type = self._header(response, "Content-Type") or ""
            document_hash = sha256(body).hexdigest()
            receipt = self.ledger.record(
                acquisition_id=acquisition_id, cycle_id=cycle_id, job_id=job_id,
                research_intent=research_intent, requested_url=url, source_url=current_url,
                access_classification="PUBLIC", status="RETRIEVED", requested_at=requested_at,
                completed_at=completed_at, http_status=status, content_type=content_type,
                source_document_id=source_document_id, document_hash=document_hash,
                bytes_received=len(body), recorder=recorder,
            )
            encoding = getattr(response, "encoding", None) or "utf-8"
            text = getattr(response, "text", None)
            if not isinstance(text, str):
                text = body.decode(encoding, errors="replace")
            return TrustedPublicAcquisitionResult(
                source,
                receipt,
                RetrievedContent(current_url, status, text, content_type, dict(getattr(response, "headers", {}) or {})),
                body,
            )
        except Exception as exc:
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            return self._failure(
                source, acquisition_id, cycle_id, job_id, research_intent,
                url, current_url, recorder, requested_at, None,
                type(exc).__name__.upper(), str(exc) or type(exc).__name__,
            )

    def _failure(self, source, acquisition_id, cycle_id, job_id, research_intent, requested_url, final_url, recorder, requested_at, http_status, error_code, error_message):
        receipt = self.ledger.record(
            acquisition_id=acquisition_id, cycle_id=cycle_id, job_id=job_id,
            research_intent=research_intent, requested_url=requested_url,
            source_url=final_url, access_classification="PUBLIC", status="FAILED",
            requested_at=requested_at, completed_at=self.clock(), http_status=http_status,
            bytes_received=0, error_code=error_code, error_message=error_message,
            recorder=recorder,
        )
        return TrustedPublicAcquisitionResult(source, receipt, None, None)

    def _validate_network_target(self, url):
        host = urlsplit(url).hostname or ""
        addresses = tuple(self.address_resolver(host))
        if not addresses:
            raise ValueError("trusted public-source domain did not resolve")
        for address in addresses:
            parsed = ipaddress.ip_address(address)
            if not parsed.is_global:
                raise ValueError("trusted public-source domain resolved to a non-public network address")

    @staticmethod
    def _resolve_addresses(host):
        return tuple(sorted({item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)}))

    @staticmethod
    def _status(response):
        status = getattr(response, "status_code", None)
        if isinstance(status, bool) or not isinstance(status, int) or not 100 <= status <= 599:
            raise ValueError("transport returned an invalid HTTP status")
        return status

    @staticmethod
    def _header(response, name):
        headers = getattr(response, "headers", {}) or {}
        for key, value in headers.items():
            if str(key).casefold() == name.casefold():
                return str(value)
        return ""

    @staticmethod
    def _body(response):
        body = getattr(response, "content", None)
        if isinstance(body, bytes): return body
        if isinstance(body, str): return body.encode("utf-8")
        text = getattr(response, "text", None)
        if isinstance(text, str): return text.encode("utf-8")
        raise ValueError("transport returned no byte or text content")


__all__ = ["TrustedPublicAcquisitionAdapter", "TrustedPublicAcquisitionResult"]
