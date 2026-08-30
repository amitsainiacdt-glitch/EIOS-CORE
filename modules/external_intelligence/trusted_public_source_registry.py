"""Source-neutral allowlist for confirmed public institutional sources."""

from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True)
class TrustedPublicSourceDefinition:
    source_id: str
    name: str
    domains: tuple[str, ...]
    allowed_path_prefixes: tuple[str, ...] = ("/",)
    source_type: str = "REGULATORY"
    enabled: bool = True
    public_information_only: bool = True


class TrustedPublicSourceRegistry:
    def __init__(self, definitions=()):
        self._definitions = {}
        for definition in definitions:
            self.register(definition)

    def register(self, definition):
        if not isinstance(definition, TrustedPublicSourceDefinition):
            raise ValueError("definition must be a TrustedPublicSourceDefinition")
        source_id = self._text(definition.source_id, "source_id")
        if source_id in self._definitions:
            raise ValueError("source_id is already registered")
        domains = tuple(self._domain(value) for value in definition.domains)
        if not domains or len(set(domains)) != len(domains):
            raise ValueError("domains must be non-empty and unique")
        prefixes = tuple(self._path(value) for value in definition.allowed_path_prefixes)
        if not prefixes:
            raise ValueError("allowed_path_prefixes must not be empty")
        if not definition.public_information_only:
            raise ValueError("trusted registry accepts public-information sources only")
        self._definitions[source_id] = TrustedPublicSourceDefinition(
            source_id, self._text(definition.name, "name"), domains, prefixes,
            self._text(definition.source_type, "source_type"), bool(definition.enabled), True,
        )

    def resolve(self, url):
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must not be empty")
        parts = urlsplit(url.strip())
        if parts.scheme.casefold() != "https":
            raise ValueError("trusted public sources require HTTPS")
        if parts.username or parts.password:
            raise ValueError("trusted public source URL cannot contain credentials")
        if parts.port not in (None, 443):
            raise ValueError("trusted public source URL cannot use a non-HTTPS port")
        host = self._domain(parts.hostname or "")
        path = parts.path or "/"
        matches = []
        for definition in self._definitions.values():
            if not definition.enabled:
                continue
            if any(host == domain or host.endswith("." + domain) for domain in definition.domains):
                if any(path.startswith(prefix) for prefix in definition.allowed_path_prefixes):
                    matches.append(definition)
        if len(matches) != 1:
            raise ValueError("URL is not uniquely approved by the trusted public-source registry")
        return matches[0]

    def all(self):
        return tuple(self._definitions[key] for key in sorted(self._definitions))

    @classmethod
    def india_primary_sources(cls):
        return cls((
            TrustedPublicSourceDefinition("NSE", "National Stock Exchange of India", ("nseindia.com",)),
            TrustedPublicSourceDefinition("BSE", "BSE India", ("bseindia.com",)),
            TrustedPublicSourceDefinition("SEBI", "Securities and Exchange Board of India", ("sebi.gov.in",)),
            TrustedPublicSourceDefinition("RBI", "Reserve Bank of India", ("rbi.org.in",)),
            TrustedPublicSourceDefinition("IMD", "India Meteorological Department", ("imd.gov.in",), source_type="WEATHER_AUTHORITY"),
            TrustedPublicSourceDefinition("NRSC", "National Remote Sensing Centre", ("nrsc.gov.in",), source_type="EARTH_OBSERVATION_AUTHORITY"),
            TrustedPublicSourceDefinition("ISRO", "Indian Space Research Organisation", ("isro.gov.in",), source_type="EARTH_OBSERVATION_AUTHORITY"),
            TrustedPublicSourceDefinition("AGRI_MINISTRY", "Ministry of Agriculture and Farmers Welfare", ("agriwelfare.gov.in",), source_type="AGRICULTURE_AUTHORITY"),
            TrustedPublicSourceDefinition("CWC", "Central Water Commission", ("cwc.gov.in",), source_type="HYDROLOGY_AUTHORITY"),
            TrustedPublicSourceDefinition("CGWB", "Central Ground Water Board", ("cgwb.gov.in",), source_type="HYDROLOGY_AUTHORITY"),
            TrustedPublicSourceDefinition("FERTILIZERS_DEPARTMENT", "Department of Fertilizers", ("fert.nic.in",), source_type="FERTILIZER_AUTHORITY"),
            TrustedPublicSourceDefinition("FOOD_DISTRIBUTION_DEPARTMENT", "Department of Food and Public Distribution", ("dfpd.gov.in",), source_type="FOOD_STOCK_AUTHORITY"),
            TrustedPublicSourceDefinition("AGMARKNET", "Agricultural Marketing Information Network", ("agmarknet.gov.in",), source_type="AGRICULTURE_MARKET_DATA"),
            TrustedPublicSourceDefinition("DGFT", "Directorate General of Foreign Trade", ("dgft.gov.in",), source_type="TRADE_POLICY_AUTHORITY"),
        ))

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _domain(cls, value):
        domain = cls._text(value, "domain").casefold().rstrip(".")
        if "/" in domain or ":" in domain:
            raise ValueError("domain must contain only a host name")
        return domain

    @classmethod
    def _path(cls, value):
        path = cls._text(value, "allowed_path_prefix")
        if not path.startswith("/"):
            raise ValueError("allowed_path_prefix must begin with /")
        return path


__all__ = ["TrustedPublicSourceDefinition", "TrustedPublicSourceRegistry"]
