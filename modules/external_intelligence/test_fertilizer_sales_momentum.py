from modules.external_intelligence.fertilizer_sales_momentum import FertilizerSalesMomentumService
from modules.external_intelligence.public_fertilizer_sales_comparison import PublicFertilizerSalesComparison, PublicFertilizerSalesComparisonPreview


def test_aggregate_decline_does_not_infer_product_weather_or_company():
    item=PublicFertilizerSalesComparison("C","CURRENT","PRIOR",151.74,157.05,-3.38,"passage",0,7,"A","a"*64,"https://example.test")
    result=FertilizerSalesMomentumService().assess(PublicFertilizerSalesComparisonPreview("A","E",item))
    assert result.aggregate_direction=="AGGREGATE_CONSUMPTION_DOWN_YOY"
    assert result.product_momentum_assessment==result.weather_attribution_assessment==result.company_impact_assessment=="RESEARCH_HOLD"
    assert "PRODUCT_LEVEL_COMPARABLE_SALES_MISSING" in result.reason_codes
    assert "WEATHER_TO_FERTILIZER_CAUSAL_ATTRIBUTION_MISSING" in result.reason_codes and not result.creates_observation
