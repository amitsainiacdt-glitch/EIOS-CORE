"""
EIOS
Everest Investment Operating System

Brave Search Provider Test
"""

from modules.external_intelligence.api_config import (
    ExternalAPIConfig,
)

from modules.external_intelligence.brave_search_provider import (
    BraveSearchProvider,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)


def main() -> None:

    query = ExternalResearchQuery(
        company="Test Company",
        ticker="TEST",
        question=(
            "Is industrial demand accelerating?"
        ),
        query=(
            '"Test Company" "TEST" '
            '"industrial demand accelerating"'
        ),
        intent="DEMAND_VALIDATION",
    )

    # ======================================================
    # PROVIDER
    # ======================================================

    provider = BraveSearchProvider(
        config=ExternalAPIConfig(
            brave_api_key=""
        )
    )

    assert isinstance(
        provider,
        SearchProvider,
    )

    print(
        "Brave Provider Contract       : PASS"
    )

    # ======================================================
    # MISSING KEY PROTECTION
    # ======================================================

    try:

        provider.search(
            query
        )

        raise AssertionError(
            "Search executed without API key"
        )

    except RuntimeError as exc:

        assert (
            "BRAVE_SEARCH_API_KEY"
            in str(exc)
        )

    print(
        "Missing API Key Protection    : PASS"
    )

    # ======================================================
    # NONE QUERY PROTECTION
    # ======================================================

    configured_provider = BraveSearchProvider(
        config=ExternalAPIConfig(
            brave_api_key="TEST-KEY"
        )
    )

    try:

        configured_provider.search(
            None
        )

        raise AssertionError(
            "None query was accepted"
        )

    except ValueError:
        pass

    print(
        "None Query Protection         : PASS"
    )

    # ======================================================
    # TIMEOUT PROTECTION
    # ======================================================

    try:

        BraveSearchProvider(
            config=ExternalAPIConfig(
                brave_api_key="TEST-KEY"
            ),
            timeout=0,
        )

        raise AssertionError(
            "Invalid timeout was accepted"
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
        query,
        "confidence",
    )

    assert not hasattr(
        query,
        "evidence_score",
    )

    assert not hasattr(
        query,
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
        "EIOS BRAVE SEARCH PROVIDER : PASS"
    )


if __name__ == "__main__":
    main()