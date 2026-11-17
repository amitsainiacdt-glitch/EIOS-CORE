"""Dated live-source research fixture for BRAVO v4.8 pilot, 9 Nov 2026.

Source links are discovery provenance only, NOT independent verification of all
filing claims or enough for ADD. No invented valuation is fed to the ADD gate.
"""
import unittest
from datetime import date
from modules.discovery.bravo_v48_pilot import DiscoveryLead, DiscoveryLane, discover

D=DiscoveryLane
LEADS=(
 DiscoveryLead("TINNARUBR",D.OPERATING_REPAIR,"2026-10-22",("https://financialfilings.com/filings/tinna-rubber-and-infrastructure-limited/earnings-release/2026/74466070/",),"Earlier growth/valuation reset","Tyre-processing volumes and end-market demand","Q2 revenue +31% and PAT +45%".split("|"),("NSE 22 Oct exchange filing summary",),next_trigger="Q3 FY27 utilisation and cash flow"),
 DiscoveryLead("SOMANYCERA",D.OPERATING_REPAIR,"2026-11-04",("https://nsearchives.nseindia.com/corporate/ixbrl/INTEGRATED_FILING_INDAS_209802_04112026193834_iXBRL_WEB.html",),"Underutilised tiles/JV margins","Better product mix and JV recovery",("Higher quarterly operating margins","JV profitability"),next_trigger="Q3 FY27 cash conversion"),
 DiscoveryLead("KSHINTL",D.OPERATING_REPAIR,"2026-11-04",("https://kshinternational.com/investor-relations/integrated-filing-financial-with-rpt/financial-results-with-rpt_september-30-2026/",),"Lower utilisation in expanded assets","Exports and specialised wire production",("Exports increased","Capacity approved"),next_trigger="Supa commissioning, FY27 cash"),
 DiscoveryLead("KEI",D.DISTRESSED_QUALITY,"2026-10-26",("https://tradebrains.in/premium/kei-industries-35-below-its-52-week-high-after-q2-results-disappoint-is-the-correction-a-buying-opportunity-or-a-warning-sign-12741182",),"Margin weakness and price correction","Sanand ramp with strong domestic demand",("Sanand expansion",),adjusted_drawdown_percent=32.4,next_trigger="Verify primary quarterly filing and FY28 margin"),
 DiscoveryLead("BORORENEW",D.DISTRESSED_QUALITY,"2026-11-04",("https://bazaarwatch.com/announcement/282946/borosil-renewables-ltd-transcript-of-analysts-investors-conference-call",),"Furnace maintenance and fuel price squeeze","Higher output plus restored surcharge",("October production recovery","Surcharge restoration"),adjusted_drawdown_percent=41,next_trigger="Q3 invoicing and funding"),
 DiscoveryLead("GANESHBE",D.BALANCE_SHEET_REPAIR,"2026-09-29",("https://www.bazaarwatch.com/announcement/158316/ganesh-benzoplast-limited-outcome-of-board-meeting",),"Conglomerate valuation with uncertain asset realisation","Proposed terminal disposal to release capital",("Signed disposal agreement",),next_trigger="Shareholder vote, completion proceeds"),
 DiscoveryLead("SAATVIKGL",D.OPERATING_REPAIR,"2026-11-05",("https://www.saatvikgroup.com/newsroom/press-release/saatvik-green-energy-reports-77-sequential-revenue-growth-in-q2-fy27-commences-commercial-production-at-odisha-facility",),"Compression in module margin and utilisation","Odisha capacity and domestic-order conversion",("Odisha commercial production","SECI awarded order"),next_trigger="Q3 debt, utilisation and cash"),
 DiscoveryLead("SWARAJENG",D.OPERATING_REPAIR,"2026-10-12",("https://financialfilings.com/filings/swaraj-engines-ltd/interim-quarterly-report/2026/69140361/",),"Share price correction despite sales growth","Engine dispatch growth",("Engine volumes +20%",),next_trigger="Q3 volume and customer concentration"),
 DiscoveryLead("PIIND",D.DISTRESSED_QUALITY,"2026-11-04",("https://www.nseindia.com/get-quote/equity/PIIND/PI-Industries-Limited",),"Export agrochemical pricing collapse","New molecules and domestic biologicals",("Commercialised molecules","Domestic growth"),adjusted_drawdown_percent=54,familiar_registry_name=True,next_trigger="Q3 export price and margins"),
 DiscoveryLead("FINCABLES",D.OPERATING_REPAIR,"2026-11-07",("https://strota.in/quarterly-results",),"Previously subdued conversion","Cable sales and capacity leverage",("Q2 revenue +65%",),familiar_registry_name=True,next_trigger="H1 cash conversion reconciliation"),
)

class ActualResearchFixture(unittest.TestCase):
    def test_three_lanes_and_fresh_first(self):
        r=discover(LEADS,date(2026,11,9))
        self.assertEqual(r.screened,10)
        self.assertEqual(len(r.investigated),10)
        self.assertEqual(len(r.missing_lanes),0)
        self.assertEqual(r.novel_leads,8)
        self.assertFalse(r.investigated[0].familiar_registry_name)
        self.assertIsNone(r.false_positives)
        self.assertIsNone(r.missed_opportunities)

if __name__=="__main__":
 unittest.main()
