"""
===============================================================================
Module: ownership_registry.py

Purpose:
    Central registry for ownership history.

Responsibilities:
    - Store ownership history
    - Retrieve ownership history
    - Retrieve latest ownership
    - Validate duplicates
    - Support Ownership Intelligence Engine

Author:
    EIOS (Everest Investment Operating System)
===============================================================================
"""

from typing import Dict, List, Optional

from .ownership_models import OwnershipQuarter


class OwnershipRegistry:
    """
    Central repository for company ownership history.
    """

    def __init__(self):
        self._registry: Dict[str, List[OwnershipQuarter]] = {}

    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------

    def register(
        self,
        company: str,
        ownership: OwnershipQuarter,
    ) -> None:
        """
        Register one ownership record.
        """

        if company not in self._registry:
            self._registry[company] = []

        # Avoid duplicate quarter entries
        for existing in self._registry[company]:

            if (
                existing.financial_year == ownership.financial_year
                and existing.quarter == ownership.quarter
            ):
                raise ValueError(
                    f"Ownership already exists for "
                    f"{company} "
                    f"{ownership.financial_year} "
                    f"{ownership.quarter}"
                )

        self._registry[company].append(ownership)

    # -------------------------------------------------------------------------
    # Retrieval
    # -------------------------------------------------------------------------

    def get_history(
        self,
        company: str,
    ) -> List[OwnershipQuarter]:
        """
        Return full ownership history.
        """

        return self._registry.get(company, [])

    def get_latest(
        self,
        company: str,
    ) -> Optional[OwnershipQuarter]:
        """
        Return latest ownership record.
        """

        history = self.get_history(company)

        if not history:
            return None

        return history[-1]

    def get_quarter(
        self,
        company: str,
        financial_year: str,
        quarter: str,
    ) -> Optional[OwnershipQuarter]:
        """
        Retrieve one specific quarter.
        """

        history = self.get_history(company)

        for record in history:

            if (
                record.financial_year == financial_year
                and record.quarter == quarter
            ):
                return record

        return None

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def exists(
        self,
        company: str,
        financial_year: str,
        quarter: str,
    ) -> bool:
        """
        Check whether quarter exists.
        """

        return (
            self.get_quarter(
                company,
                financial_year,
                quarter,
            )
            is not None
        )

    def validate(
        self,
        company: str,
    ) -> bool:
        """
        Basic validation.
        """

        history = self.get_history(company)

        return len(history) > 0

    # -------------------------------------------------------------------------
    # Utilities
    # -------------------------------------------------------------------------

    def companies(self) -> List[str]:
        """
        Return all registered companies.
        """

        return list(self._registry.keys())

    def remove(
        self,
        company: str,
        financial_year: str,
        quarter: str,
    ) -> bool:
        """
        Remove one ownership record.
        """

        history = self.get_history(company)

        for record in history:

            if (
                record.financial_year == financial_year
                and record.quarter == quarter
            ):
                history.remove(record)
                return True

        return False

    def clear(self) -> None:
        """
        Clear registry.
        """

        self._registry.clear()