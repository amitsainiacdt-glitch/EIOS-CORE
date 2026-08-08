"""
EIOS
Everest Investment Operating System

Opportunity Signal Registry

Purpose:
Maintains the canonical collection of Opportunity Intelligence
signals.

Architecture:

Signal Sources
      ↓
Signal
      ↓
SignalRegistry
      ↓
Validation / Catalyst / Opportunity Engines

Design Principles:
- Registry only manages signals.
- No scoring.
- No business calculations.
- No persistence.
- No company-specific logic.
- Duplicate signal IDs are rejected.
"""

from typing import List, Optional

from .signal_model import (
    Signal,
    SignalDomain,
    SignalStage,
)


class SignalRegistry:
    """
    Central in-memory registry for Opportunity Signals.
    """

    def __init__(self):
        self._signals = {}

    # ==========================================================
    # ADD
    # ==========================================================

    def add(self, signal: Signal) -> None:
        """
        Add a signal to the registry.

        Signal IDs must be unique.
        """

        if not signal.signal_id:
            raise ValueError(
                "Signal must have a signal_id."
            )

        if signal.signal_id in self._signals:
            raise ValueError(
                f"Signal already exists: "
                f"{signal.signal_id}"
            )

        self._signals[signal.signal_id] = signal

    # ==========================================================
    # GET
    # ==========================================================

    def get(
        self,
        signal_id: str,
    ) -> Optional[Signal]:
        """
        Retrieve a signal by ID.
        """

        return self._signals.get(signal_id)

    # ==========================================================
    # ALL
    # ==========================================================

    def get_all(self) -> List[Signal]:
        """
        Return all registered signals.
        """

        return list(
            self._signals.values()
        )

    # ==========================================================
    # DOMAIN
    # ==========================================================

    def by_domain(
        self,
        domain: SignalDomain,
    ) -> List[Signal]:
        """
        Return signals belonging to a domain.
        """

        return [
            signal
            for signal in self._signals.values()
            if signal.domain == domain
        ]

    # ==========================================================
    # COMPANY
    # ==========================================================

    def by_company(
        self,
        company: str,
    ) -> List[Signal]:
        """
        Return signals associated with a company.
        """

        return [
            signal
            for signal in self._signals.values()
            if company in signal.companies
        ]

    # ==========================================================
    # SECTOR
    # ==========================================================

    def by_sector(
        self,
        sector: str,
    ) -> List[Signal]:
        """
        Return signals associated with a sector.
        """

        return [
            signal
            for signal in self._signals.values()
            if sector in signal.sectors
        ]

    # ==========================================================
    # STAGE
    # ==========================================================

    def by_stage(
        self,
        stage: SignalStage,
    ) -> List[Signal]:
        """
        Return signals at a particular maturity stage.
        """

        return [
            signal
            for signal in self._signals.values()
            if signal.stage == stage
        ]

    # ==========================================================
    # COUNT
    # ==========================================================

    def count(self) -> int:
        """
        Return total number of registered signals.
        """

        return len(self._signals)

    # ==========================================================
    # EXISTS
    # ==========================================================

    def exists(
        self,
        signal_id: str,
    ) -> bool:
        """
        Determine whether a signal exists.
        """

        return signal_id in self._signals

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self) -> None:
        """
        Clear the in-memory registry.

        Persistence is deliberately outside this class.
        """

        self._signals.clear()