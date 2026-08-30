"""Offline tests for the trusted public-source registry and guarded adapter."""

from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


class Response:
    def __init__(self, status_code, *, body=b"", headers=None):
        self.status_code = status_code
        self.content = body
        self.text = body.decode("utf-8", errors="replace")
        self.headers = headers or {}
        self.encoding = "utf-8"


class Transport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, url, *, timeout, allow_redirects):
        self.calls.append((url, timeout, allow_redirects))
        return self.responses.pop(0)


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        definition = TrustedPublicSourceDefinition(
            "TEST_EXCHANGE", "Test Public Exchange",
            ("exchange.example.com", "static.exchange.example.com"),
            allowed_path_prefixes=("/public/",),
        )
        registry = TrustedPublicSourceRegistry((definition,))
        ledger = PublicSourceAcquisitionLedger(root / "acquisitions.jsonl")
        now = datetime(2026, 8, 29, 10, tzinfo=timezone.utc)
        resolver = lambda host: ("93.184.216.34",)

        transport = Transport([Response(200, body=b"public filing", headers={"Content-Type": "application/pdf"})])
        adapter = TrustedPublicAcquisitionAdapter(
            registry, ledger, transport=transport, address_resolver=resolver,
            clock=lambda: now,
        )
        result = adapter.acquire(
            acquisition_id="ACQ-LIVE-1", cycle_id="cycle-1", job_id="exchange-job",
            research_intent="PUBLIC_ANNOUNCEMENTS",
            url="https://exchange.example.com/public/filing.pdf",
            recorder="Trusted Adapter", requested_at=now,
            source_document_id="ANN-1",
        )
        assert result.receipt.status.value == "RETRIEVED"
        assert result.retrieved_content.content == "public filing"
        assert result.receipt.requested_url == result.receipt.source_url
        assert transport.calls[0][2] is False

        redirect_transport = Transport([
            Response(302, headers={"Location": "https://static.exchange.example.com/public/filing-2.pdf"}),
            Response(200, body=b"redirected public filing", headers={"Content-Type": "application/pdf"}),
        ])
        redirected = TrustedPublicAcquisitionAdapter(
            registry, ledger, transport=redirect_transport,
            address_resolver=resolver, clock=lambda: now,
        ).acquire(
            acquisition_id="ACQ-LIVE-2", cycle_id="cycle-1", job_id="exchange-job",
            research_intent="PUBLIC_ANNOUNCEMENTS",
            url="https://exchange.example.com/public/redirect",
            recorder="Trusted Adapter", requested_at=now,
        )
        assert redirected.receipt.status.value == "RETRIEVED"
        assert redirected.receipt.requested_url != redirected.receipt.source_url
        assert redirected.receipt.source_url.startswith("https://static.exchange.example.com/")

        blocked_transport = Transport([])
        blocked_adapter = TrustedPublicAcquisitionAdapter(
            registry, ledger, transport=blocked_transport,
            address_resolver=resolver, clock=lambda: now,
        )
        try:
            blocked_adapter.acquire(
                acquisition_id="BLOCKED", cycle_id="cycle-1", job_id="job",
                research_intent="TEST", url="https://unknown.example.com/public/a",
                recorder="Adapter", requested_at=now,
            )
        except ValueError as exc:
            assert "approved" in str(exc)
        else:
            raise AssertionError("unregistered domain accepted")
        assert not blocked_transport.calls

        private_result = TrustedPublicAcquisitionAdapter(
            registry, ledger, transport=Transport([]),
            address_resolver=lambda host: ("127.0.0.1",), clock=lambda: now,
        ).acquire(
            acquisition_id="ACQ-PRIVATE-DNS", cycle_id="cycle-1", job_id="job",
            research_intent="TEST", url="https://exchange.example.com/public/a",
            recorder="Adapter", requested_at=now,
        )
        assert private_result.receipt.status.value == "FAILED"
        assert "non-public network" in private_result.receipt.error_message

        untrusted_redirect = TrustedPublicAcquisitionAdapter(
            registry, ledger,
            transport=Transport([Response(302, headers={"Location": "https://evil.example.net/a"})]),
            address_resolver=resolver, clock=lambda: now,
        ).acquire(
            acquisition_id="ACQ-BAD-REDIRECT", cycle_id="cycle-1", job_id="job",
            research_intent="TEST", url="https://exchange.example.com/public/a",
            recorder="Adapter", requested_at=now,
        )
        assert untrusted_redirect.receipt.status.value == "FAILED"
        assert "approved" in untrusted_redirect.receipt.error_message

        http_failure = TrustedPublicAcquisitionAdapter(
            registry, ledger, transport=Transport([Response(503)]),
            address_resolver=resolver, clock=lambda: now,
        ).acquire(
            acquisition_id="ACQ-HTTP-FAIL", cycle_id="cycle-1", job_id="job",
            research_intent="TEST", url="https://exchange.example.com/public/a",
            recorder="Adapter", requested_at=now,
        )
        assert http_failure.receipt.status.value == "FAILED"
        assert http_failure.receipt.http_status == 503

        india = TrustedPublicSourceRegistry.india_primary_sources()
        assert india.resolve("https://www.nseindia.com/corporates/announcements").source_id == "NSE"
        source_ids = {item.source_id for item in india.all()}
        assert {"NSE", "BSE", "SEBI", "RBI", "IMD", "NRSC", "ISRO", "AGRI_MINISTRY", "CWC", "CGWB", "FERTILIZERS_DEPARTMENT", "FOOD_DISTRIBUTION_DEPARTMENT", "AGMARKNET", "DGFT"}.issubset(source_ids)
        assert india.resolve("https://mausam.imd.gov.in/responsive/agromet.php").source_id == "IMD"
        assert india.resolve("https://www.fert.nic.in/publication").source_id == "FERTILIZERS_DEPARTMENT"
        assert india.resolve("https://dfpd.gov.in/allocation-of-food-grains/en").source_id == "FOOD_DISTRIBUTION_DEPARTMENT"

        assert len(ledger.read_all()) == 5

    print("TRUSTED PUBLIC ACQUISITION ADAPTER: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
