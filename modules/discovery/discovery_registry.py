"""
===============================================================================
EIOS
Everest Investment Operating System

Discovery Registry

Purpose:
    Registers all Discovery Office filters.

Architecture:
    - Single source of truth for Discovery filters.
    - Discovery Engine loads filters from here.
    - New filters require registration only.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.discovery.filters.quality_filter import QualityFilter


class DiscoveryRegistry:
    """
    Registry of Discovery Office filters.
    """

    @staticmethod
    def get_filters():

        return [

            QualityFilter(),

        ]