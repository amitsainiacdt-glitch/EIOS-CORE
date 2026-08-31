"""Fail-closed readiness gate for official mandi price and arrival data."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MandiDataSourceStatus:
    source_id: str
    catalog_updated_on: date | None
    public_report_route: bool
    programmatic_access_authorized: bool
    price_fields_verified: bool
    arrival_quantity_field_verified: bool
    geography_fields_verified: bool
    commodity_field_verified: bool
    reporting_date_field_verified: bool
    source_bytes_hash_bound: bool


@dataclass(frozen=True)
class MandiDataReadiness:
    price_ready: bool
    arrival_ready: bool
    supply_tightness_ready: bool
    status: str
    missing_controls: tuple[str, ...]
    blocked_claims: tuple[str, ...]


def assess_mandi_data_readiness(source: MandiDataSourceStatus, *, as_of: date, max_catalog_age_days=45):
    if source.source_id not in ("AGMARKNET", "INDIA_OGD"):
        raise ValueError("mandi data requires an approved AGMARKNET or India OGD authority")
    missing=[]
    if source.catalog_updated_on is None or (as_of-source.catalog_updated_on).days<0 or (as_of-source.catalog_updated_on).days>max_catalog_age_days:
        missing.append("current official catalog metadata")
    if not source.public_report_route: missing.append("sanctioned public report route")
    if not source.programmatic_access_authorized: missing.append("authorized programmatic access or governed manual export")
    if not source.source_bytes_hash_bound: missing.append("hash-bound source payload")
    if not source.commodity_field_verified: missing.append("commodity field")
    if not source.geography_fields_verified: missing.append("state, district, and market fields")
    if not source.reporting_date_field_verified: missing.append("reporting-date field")
    common=not missing
    price_ready=common and source.price_fields_verified
    arrival_ready=common and source.arrival_quantity_field_verified
    if not source.price_fields_verified: missing.append("minimum, maximum, and modal price fields")
    if not source.arrival_quantity_field_verified: missing.append("arrival quantity and unit fields")
    tightness=price_ready and arrival_ready
    status="PRICE_AND_ARRIVAL_READY" if tightness else "PRICE_ONLY_READY" if price_ready else "RESEARCH_HOLD"
    return MandiDataReadiness(price_ready,arrival_ready,tightness,status,tuple(dict.fromkeys(missing)),(
        "rising mandi price proves falling physical supply",
        "lower reported arrivals prove lower crop production",
        "one market represents a state or India",
        "price and arrival co-movement was caused by weather",
        "mandi data proves a listed company's earnings impact",
        "a trading or investment conclusion",
    ))


__all__=["MandiDataSourceStatus","MandiDataReadiness","assess_mandi_data_readiness"]
