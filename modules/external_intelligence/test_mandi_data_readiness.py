from datetime import date

from modules.external_intelligence.mandi_data_readiness import MandiDataSourceStatus,assess_mandi_data_readiness


def main():
    current=date(2026,8,31)
    ogd=MandiDataSourceStatus("INDIA_OGD",date(2026,8,29),True,False,True,False,True,True,True,False)
    held=assess_mandi_data_readiness(ogd,as_of=current)
    assert held.status=="RESEARCH_HOLD" and not held.price_ready and not held.arrival_ready
    assert "authorized programmatic access or governed manual export" in held.missing_controls
    captured=MandiDataSourceStatus("INDIA_OGD",date(2026,8,29),True,True,True,False,True,True,True,True)
    price_only=assess_mandi_data_readiness(captured,as_of=current)
    assert price_only.status=="PRICE_ONLY_READY" and price_only.price_ready and not price_only.supply_tightness_ready
    complete=MandiDataSourceStatus("AGMARKNET",date(2026,8,29),True,True,True,True,True,True,True,True)
    ready=assess_mandi_data_readiness(complete,as_of=current)
    assert ready.status=="PRICE_AND_ARRIVAL_READY" and ready.supply_tightness_ready and len(ready.blocked_claims)==6
    print("MANDI DATA READINESS: ALL TESTS PASSED")


if __name__=="__main__": main()
