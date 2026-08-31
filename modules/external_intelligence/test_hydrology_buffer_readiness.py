from datetime import date

from modules.external_intelligence.hydrology_buffer_readiness import HydrologyBufferInput, HydrologyBufferReadinessService


def test_stale_official_layer_cannot_be_current_hydrology():
    result = HydrologyBufferReadinessService().assess(HydrologyBufferInput(
        source_id="NWIC", reporting_date=date(2022, 8, 31), acquisition_id="A", document_hash="a" * 64,
        structured_record_count=100, has_normal_comparison=True, has_prior_year_comparison=True,
    ), as_of_date=date(2026, 8, 31))
    assert result.decision == "RESEARCH_HOLD" and not result.usable_as_current_hydrology
    assert "HYDROLOGY_DATA_STALE" in result.reason_codes


def test_current_national_storage_without_crop_basin_map_is_not_irrigation_shield():
    result = HydrologyBufferReadinessService().assess(HydrologyBufferInput(
        source_id="CWC", reporting_date=date(2026, 8, 27), acquisition_id="A", document_hash="a" * 64,
        structured_record_count=166, has_normal_comparison=True, has_prior_year_comparison=True,
    ), as_of_date=date(2026, 8, 31))
    assert result.usable_as_current_hydrology and not result.usable_as_irrigation_buffer
    assert "CROP_BASIN_GEOGRAPHY_MAP_MISSING" in result.reason_codes


def test_complete_current_chain_only_reaches_review():
    result = HydrologyBufferReadinessService().assess(HydrologyBufferInput(
        source_id="CWC", reporting_date=date(2026, 8, 27), acquisition_id="A", document_hash="a" * 64,
        structured_record_count=166, has_normal_comparison=True, has_prior_year_comparison=True,
        has_crop_basin_geography_map=True,
    ), as_of_date=date(2026, 8, 31))
    assert result.decision == "READY_FOR_IRRIGATION_BUFFER_REVIEW"
    assert result.usable_as_irrigation_buffer and not result.creates_observation
