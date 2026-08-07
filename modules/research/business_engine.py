"""
EIOS
Business Engine

Purpose:
Orchestrates all Business Analyzers and produces a consolidated
BusinessAnalysisResult.

Author:
EIOS
"""

from .business_analysis_result import BusinessAnalysisResult

from .analyzers.business_model_analyzer import BusinessModelAnalyzer
from .analyzers.revenue_analyzer import RevenueAnalyzer
from .analyzers.tam_analyzer import TAMAnalyzer
from .analyzers.moat_analyzer import MoatAnalyzer
from .analyzers.pricing_power_analyzer import PricingPowerAnalyzer
from .analyzers.customer_analyzer import CustomerAnalyzer
from .analyzers.scalability_analyzer import ScalabilityAnalyzer
from .analyzers.capital_intensity_analyzer import CapitalIntensityAnalyzer
from .analyzers.swot_analyzer import SWOTAnalyzer


class BusinessEngine:
    """
    Executes all business analyzers and consolidates their output.
    """

    def __init__(self):

        self.business_model_analyzer = BusinessModelAnalyzer()
        self.revenue_analyzer = RevenueAnalyzer()
        self.tam_analyzer = TAMAnalyzer()
        self.moat_analyzer = MoatAnalyzer()
        self.pricing_power_analyzer = PricingPowerAnalyzer()
        self.customer_analyzer = CustomerAnalyzer()
        self.scalability_analyzer = ScalabilityAnalyzer()
        self.capital_intensity_analyzer = CapitalIntensityAnalyzer()
        self.swot_analyzer = SWOTAnalyzer()

    def analyze(self, company):
        """
        Analyze the business.

        Parameters
        ----------
        company
            Company research object.

        Returns
        -------
        BusinessAnalysisResult
        """

        result = BusinessAnalysisResult()

        # -------------------------------------------------------------
        # Run all analyzers
        # -------------------------------------------------------------

        business = self.business_model_analyzer.analyze(company)
        revenue = self.revenue_analyzer.analyze(company)
        tam = self.tam_analyzer.analyze(company)
        moat = self.moat_analyzer.analyze(company)
        customer = self.customer_analyzer.analyze(company)
        pricing = self.pricing_power_analyzer.analyze(company)
        scalability = self.scalability_analyzer.analyze(company)
        capital = self.capital_intensity_analyzer.analyze(company)
        swot = self.swot_analyzer.analyze(company)

        # -------------------------------------------------------------
        # Consolidate Business Model
        # -------------------------------------------------------------

        result.business_model = business.business_model
        result.revenue_model = business.revenue_model

        # -------------------------------------------------------------
        # Market Opportunity
        # -------------------------------------------------------------

        result.tam = tam.total_addressable_market
        result.sam = tam.serviceable_available_market
        result.som = tam.serviceable_obtainable_market

        # -------------------------------------------------------------
        # Competitive Advantage
        # -------------------------------------------------------------

        result.moat = moat.moat_strength
        result.pricing_power = pricing.pricing_strength
        result.customer_stickiness = customer.customer_stickiness
        result.switching_costs = customer.switching_cost

        # -------------------------------------------------------------
        # Scalability
        # -------------------------------------------------------------

        result.scalability = scalability.scalability
        result.reinvestment_runway = tam.growth_runway
        result.capital_intensity = capital.capital_intensity

        # -------------------------------------------------------------
        # SWOT
        # -------------------------------------------------------------

        result.strengths = swot.strengths
        result.weaknesses = swot.weaknesses
        result.opportunities = swot.opportunities
        result.threats = swot.threats

        # -------------------------------------------------------------
        # Confidence
        # -------------------------------------------------------------

        result.confidence = (
            business.confidence
            + revenue.confidence
            + tam.confidence
            + moat.confidence
            + pricing.confidence
            + customer.confidence
            + scalability.confidence
            + capital.confidence
            + swot.confidence
        ) / 9

        return result