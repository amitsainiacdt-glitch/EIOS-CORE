"""
EIOS
Everest Investment Operating System

External Research Quality Integration Test
===========================================

Verifies the boundary:

External Research
        ↓
Source Assessment
        ↓
Research Quality Gate
        ↓
Observation

Tests:

1. Accepted research becomes Observation.
2. Rejected research does not become Observation.
3. Provenance is preserved.
4. Duplicate protection remains active.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
)

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
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

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.observation.observation_persistence import (
    ObservationPersistence,
)

from modules.observation.observation_registry import (
    ObservationRegistry,
)


# ==========================================================
# MOCK SEARCH PROVIDER
# ==========================================================


class MockSearchProvider(SearchProvider):
    """
    Deterministic search provider.
    """

    def search(
        self,
        query: ExternalResearchQuery,
    ) -> list[ExternalSearchResult]:

        return [
            ExternalSearchResult(
                title="Synthetic Research",
                url="https://example.com/research",
                snippet="Synthetic research result.",
                source="Mock Provider",
            )
        ]


# ==========================================================
# MOCK HTTP RETRIEVER
# ==========================================================


class MockHTTPRetriever:
    """
    Deterministic HTTP retrieval boundary.
    """

    def __init__(
        self,
        content: str,
    ) -> None:

        self.content = content
        self.received_urls: list[str] = []

    def retrieve(
        self,
        url: str,
    ) -> RetrievedContent:

        self.received_urls.append(
            url
        )

        return RetrievedContent(
            url=url,
            status_code=200,
            content=self.content,
            content_type="text/html",
            headers={
                "Content-Type": "text/html"
            },
        )


# ==========================================================
# QUERY
# ==========================================================


def make_query() -> ExternalResearchQuery:

    return ExternalResearchQuery(
        company="Test Company",
        ticker="TEST",
        question=(
            "Is industrial demand improving?"
        ),
        query=(
            '"Test Company" '
            '"industrial demand improving"'
        ),
        intent="DEMAND_VALIDATION",
    )


# ==========================================================
# ISOLATED OBSERVATION ENGINE
# ==========================================================


def make_observation_engine() -> ObservationEngine:

    temp_dir = TemporaryDirectory()
    persistence = ObservationPersistence(
        path=Path(temp_dir.name) / "observations.json"
    )

    persistence.clear()

    engine = ObservationEngine(
        registry=ObservationRegistry(),
        persistence=persistence,
    )
    engine._test_temp_dir = temp_dir
    return engine


# ==========================================================
# VALID CONTENT
# ==========================================================


def valid_content() -> str:

    return (
        "Synthetic research indicates that industrial "
        "demand is improving with stronger order activity "
        "during the current testing period. This content "
        "is deliberately substantive so that the "
        "deterministic research quality gate accepts it."
    )


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    print("=" * 60)
    print(
        "EIOS EXTERNAL RESEARCH QUALITY "
        "INTEGRATION TEST"
    )
    print("=" * 60)

    # ======================================================
    # TEST 1 — ACCEPTED RESEARCH
    # ======================================================

    observation_engine = (
        make_observation_engine()
    )

    retriever = MockHTTPRetriever(
        valid_content()
    )

    orchestrator = (
        ExternalResearchOrchestrator(
            MockSearchProvider(),
            retriever=retriever,
            observation_engine=observation_engine,
        )
    )

    result = orchestrator.execute(
        make_query(),
        max_sources=1,
        observation_category="External Web",
        observation_confidence=70.0,
    )

    assert (
        len(result.observations)
        == 1
    )

    print(
        "Test 1 — Accepted Research → Observation : PASS"
    )

    # ======================================================
    # TEST 2 — REJECTED RESEARCH
    # ======================================================

    rejected_engine = (
        make_observation_engine()
    )

    rejected_retriever = MockHTTPRetriever(
        "Too short."
    )

    rejected_orchestrator = (
        ExternalResearchOrchestrator(
            MockSearchProvider(),
            retriever=rejected_retriever,
            observation_engine=rejected_engine,
        )
    )

    rejected_result = (
        rejected_orchestrator.execute(
            make_query(),
            max_sources=1,
            observation_category="External Web",
            observation_confidence=70.0,
        )
    )

    assert (
        len(
            rejected_result.observations
        )
        == 0
    )

    assert (
        rejected_engine.registry.count()
        == 0
    )

    print(
        "Test 2 — Rejected Research → No Observation : PASS"
    )

    # ======================================================
    # TEST 3 — PROVENANCE
    # ======================================================

    observation = (
        result.observations[0]
    )

    assert (
        observation.source
        == "https://example.com/research"
    )

    assert (
        observation.entity
        == "Test Company"
    )

    assert (
        observation.description
        == result.normalized_content[0]
        .normalized_text
    )

    assert (
        result.source_assessments[0]
        .source_url
        == observation.source
    )

    assert (
        result.normalized_content[0]
        .url
        == observation.source
    )

    print(
        "Test 3 — Provenance Preservation          : PASS"
    )

    # ======================================================
    # TEST 4 — DUPLICATE PROTECTION
    # ======================================================

    duplicate_result = (
        orchestrator.execute(
            make_query(),
            max_sources=1,
            observation_category="External Web",
            observation_confidence=70.0,
        )
    )

    assert (
        len(
            duplicate_result.observations
        )
        == 0
    )

    assert (
        observation_engine.registry.count()
        == 1
    )

    print(
        "Test 4 — Existing Duplicate Protection    : PASS"
    )

    # ======================================================
    # TEST 5 — RAW CONTENT PRESERVATION
    # ======================================================

    assert (
        result.normalized_content[0]
        .original_content
        == valid_content()
    )

    assert (
        result.retrieved_content[0]
        .content
        == valid_content()
    )

    print(
        "Test 5 — Raw Content Preservation          : PASS"
    )

    # ======================================================
    # TEST 6 — ANALYTICAL BOUNDARY
    # ======================================================

    assert not hasattr(
        result,
        "evidence",
    )

    assert not hasattr(
        result,
        "signals",
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
        "Test 6 — Analytical Boundary               : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "EIOS EXTERNAL RESEARCH QUALITY "
        "INTEGRATION : ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
