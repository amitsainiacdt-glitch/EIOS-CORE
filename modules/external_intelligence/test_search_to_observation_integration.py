"""
EIOS
Everest Investment Operating System

Search → HTTP → Observation Integration Test
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
)

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
)

from modules.external_intelligence.research_query import (
    ExternalResearchQuery,
)

from modules.external_intelligence.research_search_engine import (
    ExternalResearchSearchEngine,
)

from modules.external_intelligence.search_provider import (
    SearchProvider,
)

from modules.external_intelligence.search_result import (
    ExternalSearchResult,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)
from modules.observation.observation_persistence import ObservationPersistence


class MockSearchProvider(SearchProvider):

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [
            ExternalSearchResult(
                title="Example Research Result",
                url="https://example.com",
                snippet=(
                    "Synthetic search result "
                    "for integration testing."
                ),
                source="Mock Provider",
            )
        ]


def main() -> None:

    query = ExternalResearchQuery(
        company="Test Company",
        ticker="TEST",
        question=(
            "Is the identified demand trend "
            "supported by external evidence?"
        ),
        query=(
            '"Test Company" "TEST" '
            '"demand trend external evidence"'
        ),
        intent="DEMAND_VALIDATION",
    )

    provider = MockSearchProvider()

    search_engine = (
        ExternalResearchSearchEngine(
            provider
        )
    )

    retriever = HTTPExternalRetriever()

    temp_dir = TemporaryDirectory()
    observation_engine = ObservationEngine(
        persistence=ObservationPersistence(
            Path(temp_dir.name) / "observations.json"
        )
    )

    adapter = ExternalObservationAdapter(
        observation_engine
    )

    # ======================================================
    # SEARCH
    # ======================================================

    results = search_engine.search(
        query
    )

    assert len(results) == 1

    result = results[0]

    assert (
        result.url
        == "https://example.com"
    )

    print(
        "Search Result Creation         : PASS"
    )

    # ======================================================
    # RETRIEVE
    # ======================================================

    retrieved = retriever.retrieve(
        result.url
    )

    assert (
        retrieved.status_code
        == 200
    )

    assert retrieved.content

    print(
        "Search Result → HTTP            : PASS"
    )

    # ======================================================
    # OBSERVATION
    # ======================================================

    observation = adapter.ingest(
        title=result.title,
        description=retrieved.content,
        source=result.url,
        category="External Web",
        entity="Test Company",
        confidence=70.0,
    )

    assert observation is not None

    print(
        "HTTP → Observation              : PASS"
    )

    # ======================================================
    # SOURCE PRESERVATION
    # ======================================================

    assert (
        observation.source
        == result.url
    )

    assert (
        observation.title
        == result.title
    )

    print(
        "Source Preservation             : PASS"
    )

    # ======================================================
    # REGISTRY
    # ======================================================

    assert (
        observation_engine.registry.count()
        == 1
    )

    assert (
        observation_engine.registry.latest()
        is observation
    )

    print(
        "Observation Registry            : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        observation,
        "evidence_score",
    )

    assert not hasattr(
        observation,
        "opportunity_score",
    )

    assert not hasattr(
        observation,
        "valuation",
    )

    print(
        "Analytical Boundary             : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS SEARCH → HTTP → "
        "OBSERVATION : PASS"
    )


if __name__ == "__main__":
    main()
