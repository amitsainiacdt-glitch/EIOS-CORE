from modules.external_intelligence.sector_catalyst_coverage import build_sector_catalyst_coverage

def main():
    result=build_sector_catalyst_coverage(); sectors={item['sectorId']:item for item in result['sectors']}
    assert result['indicatorCount']==29 and result['sectorCount']>=20
    for sector in ('BANKING','FERTILIZERS','IT_SERVICES','PHARMACEUTICALS','POWER_UTILITIES','METALS','TELECOM','REAL_ESTATE','DEFENCE'):
        assert sector in sectors and sectors[sector]['indicatorCount']>=1
    for sector in sectors.values():
        for item in sector['indicators']:
            assert item['earningsChannels'] and item['preferredPrimarySourceTypes'] and item['killTests']
            assert item['minimumIndependentGroups']>=2 and item['minimumPersistentObservations']>=2
    assert result['createsCatalyst'] is False and result['changesVerdict'] is False
    print('SECTOR CATALYST COVERAGE: ALL TESTS PASSED')

if __name__=='__main__': main()
