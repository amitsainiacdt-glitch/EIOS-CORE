"""Offline tests for passive sector causal-indicator knowledge."""

from dataclasses import replace

from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry


def main():
    registry = SectorCausalIndicatorRegistry.initial_library()
    indicator_ids = {item.indicator_id for item in registry.all()}
    assert {
        "INDUSTRIAL_ORDER_CONVERSION", "LENDER_EARLY_CREDIT_STRESS",
        "CHEMICAL_SPREAD_RECOVERY", "BUILDING_MATERIAL_UTILISATION",
    }.issubset(indicator_ids)
    assert len(indicator_ids) == 29
    assert registry.validate_dependencies()
    fertilizer = registry.get("RAINFALL_FERTILIZER_RESPONSE_CURVE")
    assert "FERTILIZER_APPLICATION_TIMING" in fertilizer.required_upstream_indicator_ids
    assert "AGRICULTURAL_DROUGHT_COMPOSITE" in registry.missing_dependencies(("RAINFALL_FERTILIZER_RESPONSE_CURVE",))
    complete_fertilizer_chain = (
        "AGRICULTURAL_DROUGHT_COMPOSITE", "CROP_STAGE_WATER_STRESS", "IRRIGATION_DROUGHT_SHIELD",
        "FERTILIZER_APPLICATION_TIMING", "NUTRIENT_MIX_SUBSTITUTION", "RAINFALL_FERTILIZER_RESPONSE_CURVE",
    )
    assert registry.missing_dependencies(complete_fertilizer_chain) == ()
    industrial = registry.get("INDUSTRIAL_ORDER_CONVERSION")
    assert industrial.lead_time_quarters_min == 1 and industrial.lead_time_quarters_max == 4
    assert industrial.minimum_independence_groups == 2
    assert registry.applicable(sector_id="INDUSTRIALS", event_type="ORDER_CONTRACT") == (industrial,)
    assert registry.applicable(sector_id="BANKING", event_type="ORDER_CONTRACT") == ()
    assert registry.get("IT_DEAL_CONVERSION_AND_HIRING").minimum_persistent_observations == 2
    assert registry.get("PHARMA_REGULATORY_PIPELINE").lead_time_quarters_max == 6
    assert registry.get("RENEWABLE_AWARD_TO_COD").minimum_independence_groups == 2
    assert registry.get("DEFENCE_ORDER_EXECUTION_CASH").kill_tests
    assert registry.applicable(sector_id="TELECOM", event_type="TARIFF_CHANGE")
    try:
        registry.register(replace(industrial, indicator_id="BAD", lead_time_quarters_min=5, lead_time_quarters_max=2))
    except ValueError as exc:
        assert "lead-time" in str(exc)
    else:
        raise AssertionError("invalid lead-time definition accepted")
    try:
        registry.get("UNKNOWN")
    except ValueError as exc:
        assert "not registered" in str(exc)
    else:
        raise AssertionError("unknown indicator accepted")
    rainfall = registry.applicable(sector_id="FERTILIZERS", event_type="WEATHER_ANOMALY")
    assert {item.indicator_id for item in rainfall} >= {"AGRICULTURAL_DROUGHT_COMPOSITE", "RAINFALL_FERTILIZER_RESPONSE_CURVE"}
    print("SECTOR CAUSAL INDICATOR REGISTRY: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
