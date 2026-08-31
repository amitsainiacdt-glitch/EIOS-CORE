"""Fail-closed readiness for using reservoir data as an irrigation buffer."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HydrologyBufferInput:
    source_id: str
    reporting_date: date | None = None
    acquisition_id: str | None = None
    document_hash: str | None = None
    structured_record_count: int = 0
    has_normal_comparison: bool = False
    has_prior_year_comparison: bool = False
    has_crop_basin_geography_map: bool = False


@dataclass(frozen=True)
class HydrologyBufferReadinessPreview:
    decision: str
    reason_codes: tuple[str, ...]
    usable_as_current_hydrology: bool
    usable_as_irrigation_buffer: bool
    creates_observation: bool = False
    requires_human_review: bool = True


class HydrologyBufferReadinessService:
    AUTHORITY_IDS = {"CWC", "NWIC"}

    def assess(self, item, *, as_of_date, maximum_age_days=10):
        if not isinstance(item, HydrologyBufferInput): raise ValueError("hydrology readiness requires HydrologyBufferInput")
        if not isinstance(as_of_date, date): raise ValueError("as_of_date must be a date")
        if isinstance(maximum_age_days, bool) or not isinstance(maximum_age_days, int) or maximum_age_days < 0:
            raise ValueError("maximum_age_days must be a non-negative integer")
        reasons = []
        if item.source_id not in self.AUTHORITY_IDS: reasons.append("UNTRUSTED_HYDROLOGY_AUTHORITY")
        if item.reporting_date is None: reasons.append("HYDROLOGY_REPORTING_DATE_MISSING")
        elif item.reporting_date > as_of_date: reasons.append("HYDROLOGY_REPORTING_DATE_IN_FUTURE")
        elif (as_of_date - item.reporting_date).days > maximum_age_days: reasons.append("HYDROLOGY_DATA_STALE")
        has_dataset = bool(item.acquisition_id and item.document_hash and item.structured_record_count > 0)
        if not has_dataset: reasons.append("HYDROLOGY_DATASET_NOT_GUARDED_AND_PARSED")
        if not item.has_normal_comparison: reasons.append("NORMAL_STORAGE_COMPARISON_MISSING")
        if not item.has_prior_year_comparison: reasons.append("PRIOR_YEAR_STORAGE_COMPARISON_MISSING")
        if not item.has_crop_basin_geography_map: reasons.append("CROP_BASIN_GEOGRAPHY_MAP_MISSING")
        current = item.source_id in self.AUTHORITY_IDS and item.reporting_date is not None and not any(
            code in reasons for code in ("HYDROLOGY_REPORTING_DATE_IN_FUTURE", "HYDROLOGY_DATA_STALE")
        ) and has_dataset and item.has_normal_comparison and item.has_prior_year_comparison
        buffer_ready = current and item.has_crop_basin_geography_map
        return HydrologyBufferReadinessPreview(
            "READY_FOR_IRRIGATION_BUFFER_REVIEW" if buffer_ready else "RESEARCH_HOLD",
            tuple(reasons), current, buffer_ready,
        )


__all__ = ["HydrologyBufferInput", "HydrologyBufferReadinessPreview", "HydrologyBufferReadinessService"]
