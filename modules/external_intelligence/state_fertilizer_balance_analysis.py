"""Geographic fertilizer balance analysis that preserves state/national scope."""

from dataclasses import dataclass
from modules.external_intelligence.public_state_fertilizer_record import PublicStateFertilizerPreview


@dataclass(frozen=True)
class StateFertilizerRequirementGap:
    state: str
    product: str
    requirement_lmt: float
    availability_lmt: float
    availability_gap_lmt: float
    closing_stock_lmt: float


@dataclass(frozen=True)
class StateFertilizerBalancePreview:
    period_label: str
    state_count: int
    national_product_count: int
    state_requirement_gaps: tuple[StateFertilizerRequirementGap,...]
    national_availability_above_requirement: bool
    creates_observation: bool = False
    requires_human_review: bool = True


class StateFertilizerBalanceAnalysisService:
    def assess(self,preview):
        if not isinstance(preview,PublicStateFertilizerPreview): raise ValueError("state fertilizer analysis requires PublicStateFertilizerPreview")
        state_records=[item for item in preview.records if item.geography_scope=="STATE"]
        national=[item for item in preview.records if item.geography_scope=="ALL_INDIA"]
        if len(national)!=4 or {item.product for item in national}!={"UREA","DAP","MOP","NPKS"}: raise ValueError("exactly four All India product records are required")
        states={item.state for item in state_records}
        if any(sum(item.state==state for item in state_records)!=4 for state in states): raise ValueError("each state requires four product records")
        gaps=tuple(sorted((StateFertilizerRequirementGap(item.state,item.product,item.requirement,item.availability,round(item.availability-item.requirement,2),item.closing_stock) for item in state_records if item.availability+0.005<item.requirement),key=lambda item:(item.state,item.product)))
        return StateFertilizerBalancePreview(preview.period_label,len(states),len(national),gaps,all(item.availability>=item.requirement for item in national))


__all__=["StateFertilizerRequirementGap","StateFertilizerBalancePreview","StateFertilizerBalanceAnalysisService"]
