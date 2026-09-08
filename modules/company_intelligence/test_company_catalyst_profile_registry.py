import tempfile,unittest
from dataclasses import replace
from pathlib import Path
from modules.company_intelligence.company_catalyst_profile_registry import CompanyCatalystProfile,CompanyCatalystProfileRegistry,build_company_catalyst_onboarding

class CompanyCatalystProfileRegistryTests(unittest.TestCase):
    def profile(self):return CompanyCatalystProfile('TEST','Test IT',('IT_SERVICES',),('DIGITAL_ENGINEERING_PROVIDER',),('SOURCE-1',),'2026-09-08','REGISTERED_UNVERIFIED','Exposure unverified.')
    def test_routes_sector_and_archetype_but_does_not_claim_active_coverage(self):
        registry=CompanyCatalystProfileRegistry((self.profile(),));registry.collector_readiness={'TEST':{}}
        company=build_company_catalyst_onboarding(registry)['companies'][0]
        self.assertEqual(['IT_DEAL_CONVERSION_AND_HIRING'],[x['indicatorId'] for x in company['indicators']]);self.assertFalse(company['activeCoverageClaim'])
    def test_invalid_and_duplicate_profiles_fail(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):CompanyCatalystProfileRegistry((self.profile(),self.profile()))
        with self.assertRaisesRegex(ValueError,'exposure status'):CompanyCatalystProfileRegistry((replace(self.profile(),exposure_status='READY'),))
    def test_project_profiles_preserve_partial_and_unverified_boundary(self):
        path=Path(__file__).resolve().parents[2]/'data/company_intelligence/company_catalyst_profiles.json'
        result=build_company_catalyst_onboarding(CompanyCatalystProfileRegistry.load(path)); companies={x['ticker']:x for x in result['companies']}
        self.assertEqual(3,result['companyCount']);self.assertGreaterEqual(companies['COROMANDEL']['connectedIndicatorCount'],2)
        self.assertFalse(any(x['activeCoverageClaim'] for x in companies.values()))

if __name__=='__main__':unittest.main()
