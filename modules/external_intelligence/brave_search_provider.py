"""
EIOS
Everest Investment Operating System

Brave Search Provider
=====================

Purpose
-------
Concrete implementation of the provider-neutral SearchProvider
contract using the Brave Search API.

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
- Provides explicit provider error diagnostics.
"""

from __future__ import annotations

import requests

from modules.external_intelligence.api_config import (
    ExternalAPIConfig,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)


class BraveSearchProvider(SearchProvider):
    """
    Brave Search API implementation of SearchProvider.
    """

    BASE_URL = (
        "https://api.search.brave.com/"
        "res/v1/web/search"
    )

    DEFAULT_TIMEOUT = 15.0

    def __init__(
        self,
        config: ExternalAPIConfig | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:

        if timeout <= 0:
            raise ValueError(
                "timeout must be greater than zero"
            )

        self.config = (
            config
            if config is not None
            else ExternalAPIConfig.from_environment()
        )

        self.timeout = float(timeout)

    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:
        """
        Execute a Brave web search and normalize results.

        Raises:
            ValueError
                When query is invalid.

            RuntimeError
                When the API key is missing or the provider
                returns an HTTP error.

            requests.RequestException
                For network/transport failures.

            ValueError
                When the provider returns invalid JSON.
        """

        if query is None:
            raise ValueError(
                "query must not be None"
            )

        if not isinstance(
            query,
            ExternalResearchQuery,
        ):
            raise ValueError(
                "query must be an ExternalResearchQuery"
            )

        if not query.query.strip():
            raise ValueError(
                "query.query must not be empty"
            )

        if not self.config.brave_configured:
            raise RuntimeError(
                "BRAVE_SEARCH_API_KEY is not configured"
            )

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": (
                self.config.brave_api_key
            ),
        }

        response = requests.get(
            self.BASE_URL,
            params={
                "q": query.query,
            },
            headers=headers,
            timeout=self.timeout,
        )

        # ==================================================
        # PROVIDER ERROR DIAGNOSTICS
        # ==================================================

        if not response.ok:
            body = response.text.strip()

            raise RuntimeError(
                "Brave Search API error "
                f"{response.status_code}: "
                f"{body}"
            )

        # ==================================================
        # JSON RESPONSE
        # ==================================================

        try:
            payload = response.json()

        except ValueError as exc:

            raise RuntimeError(
                "Brave Search API returned "
                "invalid JSON"
            ) from exc

        # ==================================================
        # RESULT EXTRACTION
        # ==================================================

        results: list[
            ExternalSearchResult
        ] = []

        web_section = payload.get(
            "web",
            {},
        )

        if not isinstance(
            web_section,
            dict,
        ):
            return results

        web_results = web_section.get(
            "results",
            [],
        )

        if not isinstance(
            web_results,
            list,
        ):
            return results

        for item in web_results:

            if not isinstance(
                item,
                dict,
            ):
                continue

            title = str(
                item.get(
                    "title",
                    "",
                )
            ).strip()

            url = str(
                item.get(
                    "url",
                    "",
                )
            ).strip()

            snippet = str(
                item.get(
                    "description",
                    "",
                )
            ).strip()

            if not url:
                continue

            results.append(
                ExternalSearchResult(
                    title=title,
                    url=url,
                    snippet=snippet,
                    source="Brave Search",
                )
            )

        return results


__all__ = [
    "BraveSearchProvider",
]