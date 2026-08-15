"""
EIOS
Everest Investment Operating System

External API Configuration
==========================

Purpose
-------
Provides a controlled configuration boundary for external
API credentials.

Design Principles
-----------------
- API keys are never hardcoded.
- Secrets come from environment variables.
- Configuration remains passive.
- No network calls.
- No provider-specific search logic.
- No investment analysis.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalAPIConfig:
    """
    Immutable configuration for an external API provider.
    """

    brave_api_key: str = ""

    @classmethod
    def from_environment(cls) -> "ExternalAPIConfig":
        """
        Load external API configuration from environment
        variables.

        Expected variable:

            BRAVE_SEARCH_API_KEY
        """

        return cls(
            brave_api_key=os.environ.get(
                "BRAVE_SEARCH_API_KEY",
                "",
            ).strip()
        )

    @property
    def brave_configured(self) -> bool:
        """
        Return whether the Brave Search API key is configured.
        """

        return bool(
            self.brave_api_key
        )


__all__ = [
    "ExternalAPIConfig",
]