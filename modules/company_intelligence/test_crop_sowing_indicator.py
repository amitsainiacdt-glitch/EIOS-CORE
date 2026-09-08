import unittest
from modules.company_intelligence.crop_sowing_indicator import crop_sowing_indicator_candidate,crop_mix_summary
from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview,PublicCropAreaRecord

RULE={'id':'india-crop-sowing-area','unit':'percent change','favourable_direction':'UP','source_domain':'www.pib.gov.in'}
def preview(rows=None):
    rows=rows or (PublicCropAreaRecord('a','Rice','2026-09-04','LAKH_HECTARE',412,421.82,438.19,-16.37,'1 | Rice | 412.00 | 421.82 | 438.19 | -16.37','A','a'*64,'https://www.pib.gov.in/release'),
                  PublicCropAreaRecord('b','Grand Total','2026-09-04','LAKH_HECTARE',1104.46,1086.31,1104,-17.69,'Grand Total | 1104.46 | 1086.31 | 1104.00 | -17.69','A','a'*64,'https://www.pib.gov.in/release'))
    return PublicCropAreaPreview('A','E','2026-09-04',tuple(rows))

class CropSowingIndicatorTests(unittest.TestCase):
    def test_converts_total_area_to_reconciled_yoy_percent(self):
        result=crop_sowing_indicator_candidate(preview(),ticker='COROMANDEL',rule=RULE)
        self.assertEqual('-1.60',result['value']); self.assertIn('Grand Total',result['evidence_passage'])
    def test_rejects_missing_total_and_wrong_domain(self):
        with self.assertRaisesRegex(ValueError,'one Grand Total'): crop_sowing_indicator_candidate(preview(preview().records[:1]),ticker='X',rule=RULE)
        bad={**RULE,'source_domain':'agriwelfare.gov.in'}
        with self.assertRaisesRegex(ValueError,'authority domain'): crop_sowing_indicator_candidate(preview(),ticker='X',rule=bad)
    def test_mix_summary_is_non_causal(self):
        result=crop_mix_summary(preview()); self.assertFalse(result['causes_rainfall']); self.assertFalse(result['changes_verdict'])

if __name__=='__main__': unittest.main()
