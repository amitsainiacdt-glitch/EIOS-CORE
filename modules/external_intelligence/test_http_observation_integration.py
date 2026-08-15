"""
EIOS
Everest Investment Operating System

HTTP → Observation Integration Test
====================================

Validates the complete external-information boundary:

HTTP
  ↓
RetrievedContent
  ↓
ExternalObservationAdapter
  ↓
Observation

This test intentionally stops at Observation.

It does not create:
- Evidence
- Signals
- Catalysts
- Valuation
- Opportunity conclusions
"""

from modules.external_intelligence.http_retriever import (
    HTTPExternalRetriever,
)

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)


def main() -> None:

    # ======================================================
    # COMPONENTS
    # ======================================================

    retriever = HTTPExternalRetriever()

    observation_engine = ObservationEngine()

    adapter = ExternalObservationAdapter(
        observation_engine
    )

    print(
        "HTTP Retriever Exists          : PASS"
    )

    print(
        "Observation Adapter Exists     : PASS"
    )

    # ======================================================
    # RETRIEVE
    # ======================================================

    retrieved = retriever.retrieve(
        "https://example.com"
    )

    assert retrieved.status_code == 200

    assert retrieved.content

    print(
        "External Content Retrieved     : PASS"
    )

    # ======================================================
    # SOURCE PRESERVATION
    # ======================================================

    assert (
        retrieved.url
        == "https://example.com"
    )

    assert (
        retrieved.status_code
        == 200
    )

    print(
        "Source Identity Preserved      : PASS"
    )

    # ======================================================
    # CONVERT TO OBSERVATION
    # ======================================================

    observation = adapter.ingest(
        title="External Web Observation",
        description=retrieved.content,
        source=retrieved.url,
        category="External Web",
        entity="Example",
        confidence=70.0,
    )

    assert observation is not None

    print(
        "Observation Creation           : PASS"
    )

    # ======================================================
    # CONTENT HAND-OFF
    # ======================================================

    assert (
        observation.description
        == retrieved.content
    )

    print(
        "Content → Observation          : PASS"
    )

    # ======================================================
    # SOURCE HAND-OFF
    # ======================================================

    assert (
        observation.source
        == retrieved.url
    )

    print(
        "Source → Observation           : PASS"
    )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    assert (
        observation.confidence
        == 70.0
    )

    print(
        "Confidence Boundary            : PASS"
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
        "Observation Registry           : PASS"
    )

    # ======================================================
    # TIMESTAMP
    # ======================================================

    assert (
        observation.timestamp
        is not None
    )

    print(
        "Observation Timestamp           : PASS"
    )

    # ======================================================
    # STOP AT OBSERVATION
    # ======================================================

    assert not hasattr(
        observation,
        "valuation",
    )

    assert not hasattr(
        observation,
        "opportunity_score",
    )

    assert not hasattr(
        observation,
        "catalyst_score",
    )

    print(
        "Analytical Boundary Preserved  : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS HTTP → OBSERVATION "
        "INTEGRATION : PASS"
    )


if __name__ == "__main__":
    main()