"""Target-specific agriculture-climate research plan and coverage state."""

from dataclasses import dataclass
from enum import Enum


class AgriClimateResearchTarget(str, Enum):
    FERTILIZER_EARNINGS = "FERTILIZER_EARNINGS"
    FOOD_COMPANY_EARNINGS = "FOOD_COMPANY_EARNINGS"
    FOOD_STOCK_AND_PRICE = "FOOD_STOCK_AND_PRICE"
    RURAL_DEMAND_AND_CREDIT = "RURAL_DEMAND_AND_CREDIT"


@dataclass(frozen=True)
class AgriClimateResearchPlan:
    schema_version: int
    plan_id: str
    target: AgriClimateResearchTarget
    entity: str
    season: str
    crop_ids: tuple[str, ...]
    geography_ids: tuple[str, ...]
    required_indicator_ids: tuple[str, ...]
    required_source_ids: tuple[str, ...]
    company_exposure_required: bool


@dataclass(frozen=True)
class AgriClimateResearchCoveragePreview:
    plan_id: str
    ready_for_mandatory_meta: bool
    covered_indicator_ids: tuple[str, ...]
    missing_indicator_ids: tuple[str, ...]
    covered_source_ids: tuple[str, ...]
    missing_source_ids: tuple[str, ...]
    company_exposure_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    non_authority_statement: str


__all__ = ["AgriClimateResearchCoveragePreview", "AgriClimateResearchPlan", "AgriClimateResearchTarget"]
