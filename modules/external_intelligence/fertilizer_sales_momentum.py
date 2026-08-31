"""Bounded interpretation of comparable aggregate fertilizer consumption."""

from dataclasses import dataclass

from modules.external_intelligence.public_fertilizer_sales_comparison import PublicFertilizerSalesComparisonPreview


@dataclass(frozen=True)
class FertilizerSalesMomentumPreview:
    aggregate_direction: str
    year_over_year_percent: float
    product_momentum_assessment: str
    weather_attribution_assessment: str
    company_impact_assessment: str
    reason_codes: tuple[str, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


class FertilizerSalesMomentumService:
    def assess(self, preview, *, has_product_comparison=False, has_causal_attribution=False, has_governed_company_exposure=False):
        if not isinstance(preview,PublicFertilizerSalesComparisonPreview): raise ValueError("sales momentum requires a fertilizer comparison preview")
        value=preview.comparison.year_over_year_percent
        direction="AGGREGATE_CONSUMPTION_UP_YOY" if value>0 else "AGGREGATE_CONSUMPTION_DOWN_YOY" if value<0 else "AGGREGATE_CONSUMPTION_FLAT_YOY"
        reasons=[]
        if not has_product_comparison: reasons.append("PRODUCT_LEVEL_COMPARABLE_SALES_MISSING")
        if not has_causal_attribution: reasons.append("WEATHER_TO_FERTILIZER_CAUSAL_ATTRIBUTION_MISSING")
        if not has_governed_company_exposure: reasons.append("GOVERNED_COMPANY_EXPOSURE_MISSING")
        return FertilizerSalesMomentumPreview(
            direction,value,"READY_FOR_PRODUCT_MOMENTUM_REVIEW" if has_product_comparison else "RESEARCH_HOLD",
            "READY_FOR_CAUSAL_REVIEW" if has_causal_attribution else "RESEARCH_HOLD",
            "READY_FOR_COMPANY_EXPOSURE_REVIEW" if has_governed_company_exposure else "RESEARCH_HOLD",tuple(reasons))


__all__=["FertilizerSalesMomentumPreview","FertilizerSalesMomentumService"]
