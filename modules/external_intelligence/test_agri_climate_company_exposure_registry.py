"""Offline tests for public company agriculture-climate exposure mapping."""

from dataclasses import replace
from datetime import datetime, timezone

from modules.external_intelligence.agri_climate_company_exposure import AgriClimateCompanyExposure
from modules.external_intelligence.agri_climate_company_exposure_registry import AgriClimateCompanyExposureRegistry


def main():
    exposure = AgriClimateCompanyExposure(
        1, "EXP-1", "Example Fertilizers Limited", "FERTILIZER_PRODUCER", ("RICE", "COTTON"),
        ("MH", "TG"), (), ("UREA", "DAP"), ("FARMER", "DEALER"), "MIXED", None,
        ("NSE-ANNUAL-REPORT", "FERT-STATE-SALES"), datetime(2026, 8, 30, tzinfo=timezone.utc), True,
        "Public disclosures do not quantify crop-level revenue exposure.",
    )
    registry = AgriClimateCompanyExposureRegistry((exposure,))
    assert registry.for_entity("example fertilizers limited")[0].product_ids == ("UREA", "DAP")
    assert registry.for_entity("Unknown Limited") == ()
    for invalid, message in (
        (replace(exposure, exposure_id="NONPUBLIC", public_information_only=False), "public information"),
        (replace(exposure, exposure_id="NO-SOURCE", public_source_ids=()), "source"),
        (replace(exposure, exposure_id="BAD-PCT", disclosed_revenue_exposure_pct=101), "between 0 and 100"),
    ):
        try: registry.register(invalid)
        except ValueError as exc: assert message in str(exc)
        else: raise AssertionError("invalid company exposure accepted")
    print("AGRI-CLIMATE COMPANY EXPOSURE REGISTRY: ALL TESTS PASSED")


if __name__ == "__main__": main()
