"""Offline tests for target-driven agriculture-climate research coverage."""

from datetime import datetime, timezone

from modules.external_intelligence.agri_climate_company_exposure import AgriClimateCompanyExposure
from modules.external_intelligence.agri_climate_company_exposure_registry import AgriClimateCompanyExposureRegistry
from modules.external_intelligence.agri_climate_research_planner import AgriClimateResearchPlanner
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry


def main():
    exposure = AgriClimateCompanyExposure(
        1, "EXP-FERT-1", "Example Fertilizers Limited", "FERTILIZER_PRODUCER", ("RICE",), ("MH",), (),
        ("UREA", "DAP"), ("FARMER", "DEALER"), "MIXED", None, ("PUBLIC-REPORT",),
        datetime(2026, 8, 30, tzinfo=timezone.utc), True, "Crop revenue split is not disclosed.",
    )
    planner = AgriClimateResearchPlanner(SectorCausalIndicatorRegistry.initial_library(), AgriClimateCompanyExposureRegistry((exposure,)))
    fertilizer = planner.plan(plan_id="PLAN-FERT", target="FERTILIZER_EARNINGS", entity="Example Fertilizers Limited", season="KHARIF-2026", crop_ids=("RICE",), geography_ids=("MH",))
    assert "AGRICULTURAL_DROUGHT_COMPOSITE" in fertilizer.required_indicator_ids
    assert "RAINFALL_FERTILIZER_RESPONSE_CURVE" in fertilizer.required_indicator_ids
    assert {"IMD", "NRSC", "CWC", "CGWB", "FERTILIZERS_DEPARTMENT", "DGFT", "FOOD_DISTRIBUTION_DEPARTMENT"}.issubset(set(fertilizer.required_source_ids))
    rainfall_only = planner.coverage(fertilizer, covered_indicator_ids=("AGRICULTURAL_DROUGHT_COMPOSITE",), covered_source_ids=("IMD",))
    assert not rainfall_only.ready_for_mandatory_meta
    assert "AGRI_CLIMATE_INDICATOR_COVERAGE_INCOMPLETE" in rainfall_only.reason_codes
    complete = planner.coverage(fertilizer, covered_indicator_ids=fertilizer.required_indicator_ids, covered_source_ids=fertilizer.required_source_ids)
    assert complete.ready_for_mandatory_meta and complete.company_exposure_ids == ("EXP-FERT-1",)

    food = planner.plan(plan_id="PLAN-FOOD", target="FOOD_STOCK_AND_PRICE", entity="INDIA", season="KHARIF-2026", crop_ids=("RICE", "PULSES"), geography_ids=("INDIA",))
    assert not food.company_exposure_required
    assert planner.coverage(food, covered_indicator_ids=food.required_indicator_ids, covered_source_ids=food.required_source_ids).ready_for_mandatory_meta

    rural = planner.plan(plan_id="PLAN-RURAL", target="RURAL_DEMAND_AND_CREDIT", entity="Unknown Rural Lender", season="KHARIF-2026", crop_ids=("MIXED",), geography_ids=("INDIA",))
    rural_coverage = planner.coverage(rural, covered_indicator_ids=rural.required_indicator_ids, covered_source_ids=rural.required_source_ids)
    assert not rural_coverage.ready_for_mandatory_meta
    assert rural_coverage.reason_codes == ("AGRI_CLIMATE_COMPANY_EXPOSURE_MISSING",)
    print("AGRI-CLIMATE RESEARCH PLANNER: ALL TESTS PASSED")


if __name__ == "__main__": main()
