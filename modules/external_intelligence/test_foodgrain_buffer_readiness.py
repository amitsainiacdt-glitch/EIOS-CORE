from datetime import date
from modules.external_intelligence.foodgrain_buffer_readiness import FoodgrainBufferReadinessService
from modules.external_intelligence.public_foodgrain_buffer_record import PublicFoodgrainBufferPreview,PublicFoodgrainBufferRecord


def test_strong_old_buffer_is_baseline_not_current_price_conclusion():
    records=(PublicFoodgrainBufferRecord("W","WHEAT","28 MAY 2026","1 JULY",513,275.8,186,None,"p","A","a"*64,"https://example.test"),PublicFoodgrainBufferRecord("R","RICE","28 MAY 2026","1 JULY",397,135.4,293.21,298,"p","A","a"*64,"https://example.test"))
    result=FoodgrainBufferReadinessService().assess(PublicFoodgrainBufferPreview("A","E",records),as_of_date=date(2026,8,31))
    assert result.historical_buffer_assessment=="HISTORICAL_BUFFER_ABOVE_NORM"
    assert result.current_buffer_assessment==result.food_price_pressure_assessment=="RESEARCH_HOLD"
    assert "CURRENT_FOODGRAIN_STOCK_UPDATE_MISSING" in result.reason_codes and not result.creates_observation
