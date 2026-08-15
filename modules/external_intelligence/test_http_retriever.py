"""
EIOS
Everest Investment Operating System

HTTP External Retriever Test
============================

Validates the HTTP retrieval boundary only.

The test does not create Observations, Signals,
Evidence, Catalysts, or Opportunity conclusions.
"""

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
    RetrievedContent,
)


def main() -> None:

    # ======================================================
    # RETRIEVER EXISTS
    # ======================================================

    retriever = HTTPExternalRetriever()

    assert retriever is not None

    print(
        "HTTP Retriever Exists          : PASS"
    )

    # ======================================================
    # INVALID URL PROTECTION
    # ======================================================

    try:
        retriever.retrieve("")
        raise AssertionError(
            "Empty URL was accepted"
        )
    except ValueError:
        pass

    try:
        retriever.retrieve(
            "ftp://example.com"
        )
        raise AssertionError(
            "Unsupported protocol was accepted"
        )
    except ValueError:
        pass

    print(
        "Invalid URL Protection         : PASS"
    )

    # ======================================================
    # PUBLIC HTTP RETRIEVAL
    # ======================================================

    result = retriever.retrieve(
        "https://example.com"
    )

    assert isinstance(
        result,
        RetrievedContent,
    )

    print(
        "HTTP Retrieval                 : PASS"
    )

    # ======================================================
    # STATUS
    # ======================================================

    assert (
        result.status_code
        == 200
    )

    print(
        "HTTP Status Validation         : PASS"
    )

    # ======================================================
    # URL PRESERVATION
    # ======================================================

    assert (
        result.url
        == "https://example.com"
    )

    print(
        "URL Preservation               : PASS"
    )

    # ======================================================
    # CONTENT
    # ======================================================

    assert isinstance(
        result.content,
        str,
    )

    assert len(
        result.content
    ) > 0

    print(
        "Content Retrieval              : PASS"
    )

    # ======================================================
    # CONTENT TYPE
    # ======================================================

    assert isinstance(
        result.content_type,
        str,
    )

    print(
        "Content Type Capture           : PASS"
    )

    # ======================================================
    # HEADERS
    # ======================================================

    assert isinstance(
        result.headers,
        dict,
    )

    print(
        "Header Capture                 : PASS"
    )

    # ======================================================
    # TIMEOUT PROTECTION
    # ======================================================

    try:
        HTTPExternalRetriever(
            timeout=0
        )

        raise AssertionError(
            "Zero timeout was accepted"
        )

    except ValueError:
        pass

    print(
        "Timeout Protection             : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        result,
        "signal_score",
    )

    assert not hasattr(
        result,
        "valuation",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    print(
        "No Analytical Fabrication      : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS HTTP EXTERNAL RETRIEVER : PASS"
    )


if __name__ == "__main__":
    main()