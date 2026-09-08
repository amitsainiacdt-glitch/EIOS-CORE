"""Build company-specific catalyst selection and connector-gap status."""
import json
from pathlib import Path
from modules.company_intelligence.company_catalyst_profile_registry import CompanyCatalystProfileRegistry,build_company_catalyst_onboarding
ROOT=Path(__file__).resolve().parents[1]
def main():
    source=ROOT/'data/company_intelligence/company_catalyst_profiles.json'; output=ROOT/'data/company_intelligence/company_catalyst_onboarding.json'
    result=build_company_catalyst_onboarding(CompanyCatalystProfileRegistry.load(source));output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"Company catalyst onboarding written: {result['companyCount']} companies")
if __name__=='__main__':main()
