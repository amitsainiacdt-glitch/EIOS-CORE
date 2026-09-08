import tempfile
import unittest
from datetime import datetime,timezone
from pathlib import Path
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger,extract_primary_indicator,attach_indicator_record_state
from modules.observation.observation import Observation,ObservationProvenance


RULE={'id':'acid','indicator':'Acid price','family':'COMMODITY_INPUT','unit':'USD per tonne','favourable_direction':'DOWN',
      'source_requirement':'Issuer','source_domain':'issuer.example.com','cadence':'Quarterly','unit_aliases':['USD/t'],
      'match_terms':['phosphoric acid'],'improvement_meaning':'lower is helpful','deterioration_meaning':'higher is adverse'}


def observation(text='On 2026-06-30 phosphoric acid settled at 1700 USD/t for the reported quarter.'):
    return Observation('Official update',text,'https://issuer.example.com/q1','Primary Indicator Candidate','TEST',70,datetime.now(),
        ObservationProvenance(job_id='TEST-PRIMARY-INDICATOR-ACID',research_intent='PRIMARY_INDICATOR_MONITORING',
            source_domain='issuer.example.com',source_quality_tier='TIER_1',content_fingerprint='a'*64))


class PrimaryIndicatorLedgerTests(unittest.TestCase):
    def test_extracts_one_bound_value(self):
        result=extract_primary_indicator(observation(),RULE,ticker='TEST')
        self.assertEqual('READY_TO_RECORD',result['status']); self.assertEqual('1700',result['candidate']['value'])

    def test_ambiguous_values_are_held(self):
        result=extract_primary_indicator(observation('On 2026-06-30 phosphoric acid was 1700 USD/t, previously 1360 USD/t.'),RULE,ticker='TEST')
        self.assertEqual('HELD_VALUE_AMBIGUOUS',result['status'])

    def test_unique_header_date_is_used_when_other_document_dates_are_irrelevant(self):
        text=('PRESS RELEASE Date: 14.04.2026 ' + ('background context ' * 35) +
              'phosphoric acid settled at 1700 USD/t for the reported quarter. ' +
              ('historical discussion ' * 20) + 'Archived update 2025-01-01.')
        result=extract_primary_indicator(observation(text),RULE,ticker='TEST')
        self.assertEqual('READY_TO_RECORD',result['status'])
        self.assertEqual('2026-04-14',result['candidate']['reporting_date'])
        self.assertEqual('DOCUMENT_HEADER',result['dateBasis'])

    def test_two_dates_inside_indicator_passage_remain_held(self):
        result=extract_primary_indicator(observation(
            'Between 2026-06-30 and 2026-07-01 phosphoric acid settled at 1700 USD/t.'),RULE,ticker='TEST')
        self.assertEqual('HELD_REPORTING_DATE_AMBIGUOUS',result['status'])

    def test_forecast_percentage_cannot_enter_realized_deficit_history(self):
        rainfall={**RULE,'id':'rain','unit':'percent below long-period average','unit_aliases':['%'],
                  'source_domain':'issuer.example.com','match_terms':['All India','rainfall deficit'],
                  'match_term_groups':[['All India','country as a whole'],['seasonal rainfall','rainfall deficit']],
                  'accepted_postures':['REALIZED'],'accepted_measurements':['DIRECT_DEFICIT']}
        item=observation('PRESS RELEASE Date: 14.04.2026 The forecast says seasonal rainfall over the country as a whole is likely to be 92% of LPA with a model error of ± 5%.')
        item.provenance=ObservationProvenance(job_id='TEST-PRIMARY-INDICATOR-RAIN',research_intent='PRIMARY_INDICATOR_MONITORING',
            source_domain='issuer.example.com',source_quality_tier='TIER_1',content_fingerprint='a'*64)
        result=extract_primary_indicator(item,rainfall,ticker='TEST')
        self.assertEqual('HELD_MEASUREMENT_POSTURE_MISMATCH',result['status'])
        self.assertEqual(['FORECAST'],result['detectedPostures'])

    def test_realized_direct_deficit_is_eligible(self):
        rainfall={**RULE,'id':'rain','unit':'percent below long-period average','unit_aliases':['%'],
                  'match_terms':['All India','rainfall deficit'],
                  'accepted_postures':['REALIZED'],'accepted_measurements':['DIRECT_DEFICIT']}
        item=observation('On 2026-09-07 the observed All India seasonal rainfall deficit was 8% below LPA.')
        item.provenance=ObservationProvenance(job_id='TEST-PRIMARY-INDICATOR-RAIN',research_intent='PRIMARY_INDICATOR_MONITORING',
            source_domain='issuer.example.com',source_quality_tier='TIER_1',content_fingerprint='a'*64)
        result=extract_primary_indicator(item,rainfall,ticker='TEST')
        self.assertEqual('READY_TO_RECORD',result['status'])
        self.assertEqual('8',result['candidate']['value'])

    def test_ledger_compares_like_rule_and_never_changes_verdict(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger=PrimaryIndicatorLedger(Path(folder)/'records.jsonl')
            first=extract_primary_indicator(observation(),RULE,ticker='TEST')['candidate']; ledger.record(first,recorded_at=datetime.now(timezone.utc))
            second={**first,'reporting_date':'2026-09-30','value':'1500','content_fingerprint':'b'*64}; ledger.record(second,recorded_at=datetime.now(timezone.utc))
            alert=ledger.latest_alert(RULE)
        self.assertEqual('FAVOURABLE_DIRECTION',alert['status']); self.assertFalse(alert['changes_verdict'])

    def test_empty_ledger_reports_connected_without_inventing_value(self):
        with tempfile.TemporaryDirectory() as folder:
            display=attach_indicator_record_state({'rules':[RULE]},PrimaryIndicatorLedger(Path(folder)/'records.jsonl'))
        self.assertEqual('CONNECTED_AWAITING_FIRST_RECORD',display['recordStatus'])
        self.assertIsNone(display['rules'][0]['latest_value'])


if __name__=='__main__': unittest.main()
