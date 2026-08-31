"""Freshness-aware use of public foodgrain buffers in policy-risk research."""

from dataclasses import dataclass
from datetime import date,datetime
from modules.external_intelligence.public_foodgrain_buffer_record import PublicFoodgrainBufferPreview


@dataclass(frozen=True)
class FoodgrainBufferReadinessPreview:
    reporting_date: str
    historical_buffer_assessment: str
    current_buffer_assessment: str
    food_price_pressure_assessment: str
    reason_codes: tuple[str,...]
    creates_observation: bool = False
    requires_human_review: bool = True


class FoodgrainBufferReadinessService:
    def assess(self,preview,*,as_of_date,maximum_age_days=31):
        if not isinstance(preview,PublicFoodgrainBufferPreview): raise ValueError("foodgrain readiness requires PublicFoodgrainBufferPreview")
        if not isinstance(as_of_date,date): raise ValueError("as_of_date must be a date")
        if {item.grain for item in preview.records}!={"WHEAT","RICE"}: raise ValueError("wheat and rice records are required")
        dates={item.reporting_date for item in preview.records}
        if len(dates)!=1: raise ValueError("foodgrain records must share one reporting date")
        reporting=datetime.strptime(next(iter(dates)),"%d %B %Y").date(); age=(as_of_date-reporting).days
        if age<0: raise ValueError("foodgrain reporting date is in the future")
        above=all(item.stock_lmt>item.buffer_norm_lmt for item in preview.records)
        stale=age>maximum_age_days; reasons=[]
        if stale: reasons.append("CURRENT_FOODGRAIN_STOCK_UPDATE_MISSING")
        reasons.append("MARKET_PRICE_TRANSMISSION_NOT_ESTABLISHED")
        return FoodgrainBufferReadinessPreview(next(iter(dates)),"HISTORICAL_BUFFER_ABOVE_NORM" if above else "HISTORICAL_BUFFER_NOT_UNIFORMLY_ABOVE_NORM","RESEARCH_HOLD" if stale else "READY_FOR_CURRENT_BUFFER_REVIEW","RESEARCH_HOLD",tuple(reasons))


__all__=["FoodgrainBufferReadinessPreview","FoodgrainBufferReadinessService"]
