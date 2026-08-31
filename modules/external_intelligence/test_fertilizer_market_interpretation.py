from modules.external_intelligence.fertilizer_market_interpretation import FertilizerMarketInterpretationService
from modules.external_intelligence.public_fertilizer_market_record import PublicFertilizerMarketPreview, PublicFertilizerMarketRecord


def _record(product,requirement,availability,sales,stock):
    return PublicFertilizerMarketRecord(product,product,"P","LMT",requirement,availability,sales,stock,product,"A","a"*64,"https://example.test")


def test_supply_comfort_does_not_infer_sales_or_company_impact():
    preview=PublicFertilizerMarketPreview("A","E","P",(
        _record("UREA",109.4,163.78,94.78,69.01),_record("DAP",31.57,39.54,22.82,16.72),
        _record("MOP",10.06,13.81,5.2,8.63),_record("NPKS",48.48,84.57,39.36,45.21)))
    result=FertilizerMarketInterpretationService().assess(preview)
    assert result.national_supply_assessment=="NATIONAL_AVAILABILITY_ABOVE_REQUIREMENT"
    assert result.sales_momentum_assessment=="RESEARCH_HOLD" and result.company_impact_assessment=="RESEARCH_HOLD"
    assert next(item for item in result.balances if item.product=="UREA").availability_to_requirement_percent==149.71
    assert "COMPARABLE_PRIOR_PERIOD_SALES_MISSING" in result.reason_codes and not result.creates_observation


def test_any_availability_shortfall_is_not_hidden_by_other_products():
    preview=PublicFertilizerMarketPreview("A","E","P",(
        _record("UREA",10,9,5,4),_record("DAP",10,20,5,15),_record("MOP",10,20,5,15),_record("NPKS",10,20,5,15)))
    assert FertilizerMarketInterpretationService().assess(preview).national_supply_assessment=="POTENTIAL_SUPPLY_SHORTFALL"
