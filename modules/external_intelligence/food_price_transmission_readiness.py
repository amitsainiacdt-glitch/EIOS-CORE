"""Conservative interpretation gate for public food-price comparisons."""

from dataclasses import dataclass
from datetime import date, datetime

from modules.external_intelligence.public_food_price_comparison_record import PublicFoodPriceComparisonRecord


@dataclass(frozen=True)
class FoodPriceTransmissionAssessment:
    ready_for_meta: bool
    freshness_days: int
    direction: str
    permitted_claim: str
    blocked_claims: tuple[str,...]


def assess_food_price_transmission(record: PublicFoodPriceComparisonRecord, as_of: date, max_age_days=7):
    report=datetime.strptime(record.reporting_date.replace("-","/"),"%d/%m/%Y").date()
    age=(as_of-report).days
    if age<0: raise ValueError("reporting date is after assessment date")
    yearly=record.year_change_percent
    direction="UNAVAILABLE" if yearly is None else ("RISING" if yearly>0 else "FALLING" if yearly<0 else "FLAT")
    ready=age<=max_age_days and yearly is not None
    claim=f"Official {record.market_level.lower()} {record.commodity} price is {yearly:+.2f}% versus one year earlier." if ready else "The price record is stale or lacks a comparable annual value."
    return FoodPriceTransmissionAssessment(ready,age,direction,claim,("weather or crop-area data caused the price move","the national average proves state-level prices or arrivals","the price move proves processor margin or company earnings impact","a trading or investment conclusion"))


__all__=["FoodPriceTransmissionAssessment","assess_food_price_transmission"]
