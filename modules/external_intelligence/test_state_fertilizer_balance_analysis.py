from modules.external_intelligence.public_state_fertilizer_record import PublicStateFertilizerPreview,PublicStateFertilizerRecord
from modules.external_intelligence.state_fertilizer_balance_analysis import StateFertilizerBalanceAnalysisService


def _record(state,scope,product,requirement,availability):
    sales=min(availability,requirement)/2; closing=availability-sales
    return PublicStateFertilizerRecord(state+product,state,scope,product,"P","LMT",requirement,availability,sales,closing,state,"A","a"*64,"https://example.test")


def test_national_comfort_does_not_hide_state_product_shortfall():
    products=("UREA","DAP","MOP","NPKS")
    records=[_record("All India","ALL_INDIA",p,10,20) for p in products]
    records += [_record("Alpha","STATE",p,10,9 if p=="DAP" else 20) for p in products]
    result=StateFertilizerBalanceAnalysisService().assess(PublicStateFertilizerPreview("A","E","P",tuple(records)))
    assert result.national_availability_above_requirement and result.state_count==1
    assert len(result.state_requirement_gaps)==1 and result.state_requirement_gaps[0].product=="DAP"
    assert not result.creates_observation
