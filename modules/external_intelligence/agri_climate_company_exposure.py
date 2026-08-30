"""Public, dated company exposure needed for agriculture-climate transmission."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class IrrigationDependency(str, Enum):
    LOW = "LOW"
    MIXED = "MIXED"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AgriClimateCompanyExposure:
    schema_version: int
    exposure_id: str
    entity: str
    company_archetype: str
    crop_ids: tuple[str, ...]
    state_ids: tuple[str, ...]
    district_ids: tuple[str, ...]
    product_ids: tuple[str, ...]
    customer_types: tuple[str, ...]
    irrigation_dependency: IrrigationDependency
    disclosed_revenue_exposure_pct: float | None
    public_source_ids: tuple[str, ...]
    as_of: datetime
    public_information_only: bool
    uncertainty_statement: str


__all__ = ["AgriClimateCompanyExposure", "IrrigationDependency"]
