"""Write the passive universal sector-catalyst coverage map."""
import json
from pathlib import Path
from modules.external_intelligence.sector_catalyst_coverage import build_sector_catalyst_coverage

ROOT=Path(__file__).resolve().parents[1]
def main():
    result=build_sector_catalyst_coverage(); path=ROOT/'data/company_intelligence/sector_catalyst_coverage.json'
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"Sector catalyst coverage written: {result['sectorCount']} sectors | {result['indicatorCount']} indicators")
if __name__=='__main__': main()
