"""
Module: Company

Purpose:
Defines the Company object, the Digital Twin of a real-world business
inside the Everest Investment Operating System (EIOS).

Architecture Layer:
Knowledge

Author:
EIOS Project

Version:
0.2.0
"""


class Company:
    """
    Digital Twin of a company.
    Every module in EIOS revolves around this object.
    """

    def __init__(
        self,
        name: str,
        ticker: str,
        sector: str,
        industry: str
    ):

        # --------------------------------------------------
        # Identity
        # --------------------------------------------------
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.industry = industry

        # --------------------------------------------------
        # Knowledge
        # --------------------------------------------------
        self.master_dossier = None
        self.intelligence = None

        # --------------------------------------------------
        # Evidence
        # --------------------------------------------------
        self.evidence = []

        # --------------------------------------------------
        # Events
        # --------------------------------------------------
        self.events = []

        # --------------------------------------------------
        # Decisions
        # --------------------------------------------------
        self.decisions = []

        # --------------------------------------------------
        # Learning
        # --------------------------------------------------
        self.learning_history = []

    def summary(self):

        return {
            "Name": self.name,
            "Ticker": self.ticker,
            "Sector": self.sector,
            "Industry": self.industry,
            "Evidence": len(self.evidence),
            "Events": len(self.events),
            "Decisions": len(self.decisions),
            "Learning": len(self.learning_history),
        }

    def __str__(self):

        return f"{self.name} ({self.ticker})"