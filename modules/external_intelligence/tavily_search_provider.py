"""
EIOS
Everest Investment Operating System

Tavily Search Provider
======================

Purpose
-------
Concrete implementation of the provider-neutral SearchProvider
contract using the Tavily Search API.

Design Principles
-----------------
- Implements SearchProvider only.
- Uses ExternalResearchQuery as input.
- Returns ExternalSearchResult objects.
- Does not create Observations.
- Does not create Evidence.
- Does not create Signals.
- Does not perform investment analysis.
- API key comes only from environment configuration.
"""

from __future__ import annotations

import os

import requests

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class TavilySearchProvider(SearchProvider):
    """
    Tavily Search API implementation of SearchProvider.
    """

    BASE_URL = (
        "https://api.tavily.com/search"
    )

    DEFAULT_TIMEOUT = 15.0

    API_KEY_ENVIRONMENT_VARIABLE = (
        "TAVILY_API_KEY"
    )

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:

        if timeout <= 0:
            raise ValueError(
                "timeout must be greater than zero"
            )

        self.api_key = (
            api_key
            if api_key is not None
            else os.getenv(
                self.API_KEY_ENVIRONMENT_VARIABLE,
                "",
            ).strip()
        )

        self.timeout = float(timeout)

    # ======================================================
    # CONFIGURATION
    # ======================================================

    @property
    def configured(self) -> bool:
        """
        Return whether a Tavily API key is configured.
        """

        return bool(
            self.api_key
        )

    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:
        """
        Execute a Tavily web search and normalize results.
        """

        if query is None:
            raise ValueError(
                "query must not be None"
            )

        if not self.configured:
            raise RuntimeError(
                "TAVILY_API_KEY is not configured"
            )

        payload = {
            "api_key": self.api_key,
            "query": query.query,
            "search_depth": "basic",
            "include_answer": False,
            "include_raw_content": False,
            "max_results": 5,
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            timeout=self.timeout,
        )

        if not response.ok:
            raise RuntimeError(
                "Tavily Search API error "
                f"{response.status_code}: "
                f"{response.text}"
            )

        response_payload = response.json()

        results = []

        for item in response_payload.get(
            "results",
            [],
        ):

            title = str(
                item.get(
                    "title",
                    "",
                )
            )

            url = str(
                item.get(
                    "url",
                    "",
                )
            )

            snippet = str(
                item.get(
                    "content",
                    "",
                )
            )

            if not url:
                continue

            results.append(
                ExternalSearchResult(
                    title=title,
                    url=url,
                    snippet=snippet,
                    source="Tavily Search",
                )
            )

        return results


__all__ = [
    "TavilySearchProvider",
]