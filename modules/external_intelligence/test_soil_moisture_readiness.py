from modules.external_intelligence.soil_moisture_readiness import (
    SoilMoistureReadinessService,
    SoilMoistureResearchInput,
)


def test_catalogue_availability_is_discovery_only():
    result = SoilMoistureReadinessService().assess(SoilMoistureResearchInput(
        source_id="NRSC",
        product_name="Surface Soil Moisture - 2 Day",
        latest_period="25-Aug-2026",
    ))
    assert result.usable_for_source_discovery
    assert not result.usable_for_weather_corroboration
    assert not result.usable_for_crop_stress
    assert result.decision == "RESEARCH_HOLD"
    assert "DATASET_NOT_GUARDED_AND_PARSED" in result.reason_codes
    assert "SOIL_MOISTURE_ANOMALY_MISSING" in result.reason_codes
    assert not result.creates_observation


def test_absolute_measurements_without_baseline_cannot_claim_anomaly():
    result = SoilMoistureReadinessService().assess(SoilMoistureResearchInput(
        source_id="NRSC", product_name="Surface Soil Moisture - 2 Day",
        latest_period="25-Aug-2026", dataset_acquisition_id="A1",
        dataset_document_hash="a" * 64, structured_record_count=100,
    ))
    assert not result.usable_for_weather_corroboration
    assert "SOIL_MOISTURE_BASELINE_MISSING" in result.reason_codes


def test_anomaly_without_crop_mapping_and_corroboration_remains_hold():
    result = SoilMoistureReadinessService().assess(SoilMoistureResearchInput(
        source_id="NRSC", product_name="Surface Soil Moisture - 2 Day",
        latest_period="25-Aug-2026", dataset_acquisition_id="A1",
        dataset_document_hash="a" * 64, structured_record_count=100,
        has_valid_baseline=True, has_computed_anomaly=True,
    ))
    assert result.usable_for_weather_corroboration
    assert not result.usable_for_crop_stress
    assert "CROP_STAGE_GEOGRAPHY_MAP_MISSING" in result.reason_codes
    assert "INDEPENDENT_CROP_STRESS_CORROBORATION_MISSING" in result.reason_codes


def test_complete_chain_only_reaches_crop_stress_review():
    result = SoilMoistureReadinessService().assess(SoilMoistureResearchInput(
        source_id="NRSC", product_name="Surface Soil Moisture - 2 Day",
        latest_period="25-Aug-2026", dataset_acquisition_id="A1",
        dataset_document_hash="a" * 64, structured_record_count=100,
        has_valid_baseline=True, has_computed_anomaly=True,
        has_crop_stage_geography_map=True, has_independent_corroboration=True,
    ))
    assert result.decision == "READY_FOR_CROP_STRESS_REVIEW"
    assert result.usable_for_crop_stress
    assert result.reason_codes == ()
    assert not result.creates_observation
