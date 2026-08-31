"""Non-investment interpretation of structured fertilizer market balances."""

from dataclasses import dataclass

from modules.external_intelligence.public_fertilizer_market_record import PublicFertilizerMarketPreview


@dataclass(frozen=True)
class FertilizerProductBalance:
    product: str
    availability_to_requirement_percent: float
    sales_to_requirement_percent: float
    closing_stock_lmt: float
    supply_shortfall: bool


@dataclass(frozen=True)
class FertilizerMarketInterpretationPreview:
    period_label: str
    balances: tuple[FertilizerProductBalance, ...]
    national_supply_assessment: str
    sales_momentum_assessment: str
    company_impact_assessment: str
    reason_codes: tuple[str, ...]
    creates_observation: bool = False
    requires_human_review: bool = True


class FertilizerMarketInterpretationService:
    def assess(self, preview, *, has_comparable_prior_period=False, has_governed_company_exposure=False):
        if not isinstance(preview, PublicFertilizerMarketPreview): raise ValueError("fertilizer interpretation requires PublicFertilizerMarketPreview")
        if {item.product for item in preview.records}!={"UREA","DAP","MOP","NPKS"}: raise ValueError("complete major-product set is required")
        balances=[]
        for item in sorted(preview.records,key=lambda value:value.product):
            if item.requirement<=0: raise ValueError("fertilizer requirement must be positive")
            balances.append(FertilizerProductBalance(item.product,round(100*item.availability/item.requirement,2),round(100*item.dbt_sales/item.requirement,2),item.closing_stock,item.availability<item.requirement))
        shortfall=any(item.supply_shortfall for item in balances)
        reasons=[]
        if not has_comparable_prior_period: reasons.append("COMPARABLE_PRIOR_PERIOD_SALES_MISSING")
        if not has_governed_company_exposure: reasons.append("GOVERNED_COMPANY_EXPOSURE_MISSING")
        return FertilizerMarketInterpretationPreview(
            preview.period_label,tuple(balances),"POTENTIAL_SUPPLY_SHORTFALL" if shortfall else "NATIONAL_AVAILABILITY_ABOVE_REQUIREMENT",
            "RESEARCH_HOLD" if not has_comparable_prior_period else "READY_FOR_SALES_MOMENTUM_REVIEW",
            "RESEARCH_HOLD" if not has_governed_company_exposure else "READY_FOR_COMPANY_EXPOSURE_REVIEW",
            tuple(reasons),
        )


__all__=["FertilizerProductBalance","FertilizerMarketInterpretationPreview","FertilizerMarketInterpretationService"]
