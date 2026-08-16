"""
EIOS
Everest Investment Operating System

Tavily Search Provider Tests
============================

Validates the provider-neutral SearchProvider contract
without making any live network requests.
"""

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.external_intelligence.tavily_search_provider import (
    TavilySearchProvider,
)


# ==========================================================
# TEST HELPERS
# ==========================================================


class FakeResponse:
    """Deterministic fake Tavily response."""

    ok = True
    status_code = 200
    text = "OK"

    def json(self):
        return {
            "results": [
                {
                    "title": "Test Result One",
                    "url": "https://example.com/one",
                    "content": "Test content one.",
                },
                {
                    "title": "Test Result Two",
                    "url": "https://example.com/two",
                    "content": "Test content two.",
                },
            ]
        }


class FakeRequests:
    """Deterministic requests replacement."""

    def __init__(self):
        self.called = False
        self.url = None
        self.json_payload = None
        self.timeout = None

    def post(
        self,
        url,
        json,
        timeout,
    ):
        self.called = True
        self.url = url
        self.json_payload = json
        self.timeout = timeout

        return FakeResponse()


# ==========================================================
# TESTS
# ==========================================================


def main() -> None:

    # ======================================================
    # PROVIDER CONTRACT
    # ======================================================

    provider = TavilySearchProvider(
        api_key="TEST-KEY"
    )

    assert isinstance(
        provider,
        SearchProvider,
    )

    print(
        "Tavily Provider Contract       : PASS"
    )

    # ======================================================
    # CONFIGURATION
    # ======================================================

    assert provider.configured is True

    print(
        "API Key Configuration           : PASS"
    )

    # ======================================================
    # NONE QUERY PROTECTION
    # ======================================================

    try:
        provider.search(None)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "None query must raise ValueError"
        )

    print(
        "None Query Protection           : PASS"
    )

    # ======================================================
    # MISSING API KEY PROTECTION
    # ======================================================

    unconfigured = TavilySearchProvider(
        api_key=""
    )

    try:
        unconfigured.search(
            ExternalResearchQuery(
                company="Tata Motors",
                ticker="TATAMOTORS",
                question="Test question",
                query="Tata Motors test",
                intent="TEST",
            )
        )
    except RuntimeError as exc:

        assert (
            "TAVILY_API_KEY"
            in str(exc)
        )

    else:

        raise AssertionError(
            "Missing API key must raise RuntimeError"
        )

    print(
        "Missing API Key Protection      : PASS"
    )

    # ======================================================
    # TIMEOUT VALIDATION
    # ======================================================

    try:
        TavilySearchProvider(
            api_key="TEST-KEY",
            timeout=0,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Invalid timeout must raise ValueError"
        )

    print(
        "Timeout Protection              : PASS"
    )

    # ======================================================
    # NETWORK MOCK
    # ======================================================

    fake_requests = FakeRequests()

    import modules.external_intelligence.tavily_search_provider as module

    original_requests = module.requests

    module.requests = fake_requests

    try:

        query = ExternalResearchQuery(
            company="Tata Motors",
            ticker="TATAMOTORS",
            question=(
                "What are the latest "
                "demand developments?"
            ),
            query=(
                "Tata Motors latest "
                "demand developments"
            ),
            intent="DEMAND_RESEARCH",
        )

        results = provider.search(
            query
        )

    finally:

        module.requests = original_requests

    # ======================================================
    # REQUEST EXECUTION
    # ======================================================

    assert fake_requests.called is True

    assert (
        fake_requests.url
        == TavilySearchProvider.BASE_URL
    )

    assert (
        fake_requests.timeout
        == provider.timeout
    )

    print(
        "Search Execution                : PASS"
    )

    # ======================================================
    # REQUEST PRESERVATION
    # ======================================================

    assert (
        fake_requests.json_payload["query"]
        == query.query
    )

    assert (
        fake_requests.json_payload["api_key"]
        == "TEST-KEY"
    )

    print(
        "Query Preservation              : PASS"
    )

    # ======================================================
    # RESULT TYPE
    # ======================================================

    assert len(results) == 2

    assert all(
        isinstance(
            result,
            ExternalSearchResult,
        )
        for result in results
    )

    print(
        "Search Result Type              : PASS"
    )

    # ======================================================
    # RESULT PRESERVATION
    # ======================================================

    assert (
        results[0].title
        == "Test Result One"
    )

    assert (
        results[0].url
        == "https://example.com/one"
    )

    assert (
        results[0].snippet
        == "Test content one."
    )

    assert (
        results[0].source
        == "Tavily Search"
    )

    print(
        "Result Preservation             : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        results[0],
        "score",
    )

    assert not hasattr(
        results[0],
        "recommendation",
    )

    assert not hasattr(
        results[0],
        "opportunity_score",
    )

    print(
        "No Analytical Fabrication       : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS TAVILY SEARCH PROVIDER : PASS"
    )


if __name__ == "__main__":
    main()