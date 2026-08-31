"""Fail-closed readiness checks for soil-moisture use in agriculture research."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SoilMoistureResearchInput:
    source_id: str
    product_name: str
    latest_period: str | None = None
    dataset_acquisition_id: str | None = None
    dataset_document_hash: str | None = None
    structured_record_count: int = 0
    has_valid_baseline: bool = False
    has_computed_anomaly: bool = False
    has_crop_stage_geography_map: bool = False
    has_independent_corroboration: bool = False


@dataclass(frozen=True)
class SoilMoistureReadinessPreview:
    decision: str
    reason_codes: tuple[str, ...]
    usable_for_source_discovery: bool
    usable_for_weather_corroboration: bool
    usable_for_crop_stress: bool
    creates_observation: bool = False
    requires_human_review: bool = True


class SoilMoistureReadinessService:
    """Separates catalogue discovery, measured data, anomaly, and crop impact."""

    def assess(self, item: SoilMoistureResearchInput) -> SoilMoistureReadinessPreview:
        if not isinstance(item, SoilMoistureResearchInput):
            raise ValueError("soil-moisture readiness requires SoilMoistureResearchInput")

        reasons = []
        if item.source_id != "NRSC":
            reasons.append("UNTRUSTED_SOIL_MOISTURE_AUTHORITY")
        if not item.latest_period:
            reasons.append("LATEST_PERIOD_UNVERIFIED")

        has_dataset = bool(
            item.dataset_acquisition_id
            and item.dataset_document_hash
            and item.structured_record_count > 0
        )
        if not has_dataset:
            reasons.append("DATASET_NOT_GUARDED_AND_PARSED")
        if not item.has_valid_baseline:
            reasons.append("SOIL_MOISTURE_BASELINE_MISSING")
        if not item.has_computed_anomaly:
            reasons.append("SOIL_MOISTURE_ANOMALY_MISSING")
        if not item.has_crop_stage_geography_map:
            reasons.append("CROP_STAGE_GEOGRAPHY_MAP_MISSING")
        if not item.has_independent_corroboration:
            reasons.append("INDEPENDENT_CROP_STRESS_CORROBORATION_MISSING")

        discovery = item.source_id == "NRSC" and bool(item.product_name) and bool(item.latest_period)
        weather = discovery and has_dataset and item.has_valid_baseline and item.has_computed_anomaly
        crop_stress = weather and item.has_crop_stage_geography_map and item.has_independent_corroboration
        return SoilMoistureReadinessPreview(
            decision="READY_FOR_CROP_STRESS_REVIEW" if crop_stress else "RESEARCH_HOLD",
            reason_codes=tuple(reasons),
            usable_for_source_discovery=discovery,
            usable_for_weather_corroboration=weather,
            usable_for_crop_stress=crop_stress,
        )


__all__ = [
    "SoilMoistureResearchInput",
    "SoilMoistureReadinessPreview",
    "SoilMoistureReadinessService",
]
