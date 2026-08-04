"""
===============================================================================
EIOS
Everest Investment Operating System

Universe Builder

Purpose:
    Builds the investment universe for the Discovery Office.

Architecture:
    - Produces DiscoveryCandidate objects.
    - Does not perform scoring.
    - Does not perform filtering.
    - Simply constructs the research universe.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.discovery.discovery_candidate import DiscoveryCandidate


class UniverseBuilder:
    """
    Builds the investment universe.
    """

    def build(self):
        """
        Returns a list of DiscoveryCandidate objects.

        Temporary implementation for Sprint 9.
        """

        return [
            DiscoveryCandidate(
                company_name="Genus Power",
                ticker="GENUSPOWER",
                sector="Capital Goods",
                industry="Smart Metering",
            ),
            DiscoveryCandidate(
                company_name="PI Industries",
                ticker="PIIND",
                sector="Chemicals",
                industry="Agro Chemicals",
            ),
            DiscoveryCandidate(
                company_name="Shilchar Technologies",
                ticker="SHILCHAR",
                sector="Electrical Equipment",
                industry="Transformers",
            ),
        ]