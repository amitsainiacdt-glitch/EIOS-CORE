"""
EIOS
Everest Investment Operating System

HTTP External Retriever
=======================

Purpose
-------
Provides a controlled HTTP retrieval boundary for externally
hosted information.

Architecture

Internet / HTTP Source
        ↓
HTTPExternalRetriever
        ↓
RetrievedContent
        ↓
ExternalObservationAdapter
        ↓
Observation

Design Principles
-----------------
- Retrieval only.
- No investment analysis.
- No Signal creation.
- No Evidence creation.
- No Catalyst analysis.
- No valuation.
- No opportunity scoring.
- No persistence.
- Explicit timeout.
- Explicit status validation.
- Deterministic error handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import requests


@dataclass(frozen=True)
class RetrievedContent:
    """
    Immutable result of an HTTP retrieval.
    """

    url: str

    status_code: int

    content: str

    content_type: str

    headers: Dict[str, str]


class HTTPExternalRetriever:
    """
    Controlled HTTP retrieval client.

    This class retrieves external content only.
    """

    DEFAULT_TIMEOUT = 15.0

    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:

        if timeout <= 0:
            raise ValueError(
                "timeout must be greater than zero"
            )

        self.timeout = float(timeout)

    # ======================================================
    # RETRIEVE
    # ======================================================

    def retrieve(
        self,
        url: str,
    ) -> RetrievedContent:
        """
        Retrieve content from an HTTP/HTTPS URL.

        Raises:
            ValueError
                for invalid URLs.

            requests.RequestException
                for transport failures.

            requests.HTTPError
                for HTTP error responses.
        """

        if not isinstance(
            url,
            str,
        ):
            raise ValueError(
                "url must be a string"
            )

        normalized_url = url.strip()

        if not normalized_url:
            raise ValueError(
                "url must not be empty"
            )

        if not (
            normalized_url.startswith(
                "http://"
            )
            or normalized_url.startswith(
                "https://"
            )
        ):
            raise ValueError(
                "url must use http:// or https://"
            )

        response = requests.get(
            normalized_url,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return RetrievedContent(
            url=normalized_url,
            status_code=response.status_code,
            content=response.text,
            content_type=(
                response.headers.get(
                    "Content-Type",
                    "",
                )
            ),
            headers=dict(
                response.headers
            ),
        )


__all__ = [
    "RetrievedContent",
    "HTTPExternalRetriever",
]