"""
Module: Company Registry

Purpose:
Maintains the registry of all Company objects inside EIOS.

Architecture Layer:
Knowledge

Author:
EIOS Project

Version:
0.1.0
"""

from .company import Company


class CompanyRegistry:
    """Stores and manages all companies known to EIOS."""

    def __init__(self):
        self._companies = {}

    def add_company(self, company: Company):
        """Add a company to the registry."""
        self._companies[company.ticker] = company

    def get_company(self, ticker: str):
        """Retrieve a company by ticker."""
        return self._companies.get(ticker)

    def list_companies(self):
        """Return all registered companies."""
        return list(self._companies.values())

    def count(self):
        """Return the number of registered companies."""
        return len(self._companies)