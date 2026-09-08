import tempfile,unittest
from datetime import datetime,timezone
from pathlib import Path
from types import SimpleNamespace
from modules.company_intelligence.automatic_crop_sowing_monitor import crop_area_urls_from_research,run_automatic_crop_sowing_monitor

class AutomaticCropSowingMonitorTests(unittest.TestCase):
    def test_extracts_only_exact_official_urls_from_matching_job(self):
        def selected(url): return SimpleNamespace(result=SimpleNamespace(url=url))
        job='COROMANDEL-PRIMARY-INDICATOR-INDIA-CROP-SOWING-AREA'
        results=[SimpleNamespace(job_id=job,selected_sources=[selected('https://www.pib.gov.in/PressReleasePage.aspx?PRID=1'),selected('https://pib.gov.in/PressReleasePage.aspx?PRID=2'),selected('https://www.pib.gov.in.evil.example/x?PRID=3')])]
        self.assertEqual(('https://www.pib.gov.in/PressReleasePage.aspx?PRID=1',),crop_area_urls_from_research(results))
    def test_missing_discovery_is_held_and_cannot_change_decisions(self):
        with tempfile.TemporaryDirectory() as folder:
            result=run_automatic_crop_sowing_monitor(Path(folder),candidate_urls=(),now=datetime(2026,9,8,tzinfo=timezone.utc))
            self.assertEqual('NO_SOURCE_DISCOVERED',result['status']); self.assertFalse(result['causes_rainfall']); self.assertFalse(result['changes_verdict'])

if __name__=='__main__': unittest.main()
