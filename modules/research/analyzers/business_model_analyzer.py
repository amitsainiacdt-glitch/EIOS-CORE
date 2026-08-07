"""
===============================================================================
EIOS
Business Model Analyzer

Purpose:
    Analyze and understand the company's business model.

Responsibilities:
    - What does the company do?
    - How does it make money?
    - Who are its customers?
    - What products/services are offered?
    - How are revenues generated?

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import dataclass, field

from .base_analyzer import BaseAnalyzer


@dataclass
class BusinessModelAnalysis:
    """
    Stores the output of the Business Model Analyzer.
    """

    business_model: str = ""

    revenue_model: str = ""

    primary_products: list[str] = field(default_factory=list)

    primary_customers: list[str] = field(default_factory=list)

    distribution_channels: list[str] = field(default_factory=list)

    recurring_revenue: bool = False

    asset_light: bool = False

    capital_intensive: bool = False

    notes: list[str] = field(default_factory=list)

    confidence: float = 0.0


class BusinessModelAnalyzer(BaseAnalyzer):
    """
    Understands how a company creates value.
    """

    def analyze(self, company):
        """
        Analyze the company's business model.

        Parameters
        ----------
        company
            Company research object.

        Returns
        -------
        BusinessModelAnalysis
        """

        analysis = BusinessModelAnalysis()

        # ------------------------------------------------------------------
        # Actual analysis logic will be implemented in future releases
        # using:
        #   - Annual Reports
        #   - Conference Calls
        #   - Investor Presentations
        #   - Financial Statements
        #   - AI Reasoning
        # ------------------------------------------------------------------

        return analysis

