"""
EIOS
Everest Investment Operating System

External Observation Adapter Test
=================================

Validates the controlled boundary between externally obtained
information and the EIOS Observation layer.

The test intentionally does NOT access the internet.
"""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)
from modules.observation.observation_persistence import ObservationPersistence


def main() -> None:

    # ======================================================
    # ENGINE / ADAPTER EXISTS
    # ======================================================

    temp_dir = TemporaryDirectory()
    observation_engine = ObservationEngine(
        persistence=ObservationPersistence(
            Path(temp_dir.name) / "observations.json"
        )
    )

    adapter = ExternalObservationAdapter(
        observation_engine
    )

    assert adapter is not None

    print(
        "External Observation Adapter : PASS"
    )

    # ======================================================
    # INGEST EXTERNAL INFORMATION
    # ======================================================

    source_data = {
        "title": (
            "Industrial demand acceleration"
        ),
        "description": (
            "External source reports improving "
            "industrial demand."
        ),
        "source": (
            "Synthetic External Source"
        ),
        "category": "Industry",
        "entity": "TEST COMPANY",
        "confidence": 85.0,
    }

    source_copy = deepcopy(
        source_data
    )

    observation = adapter.ingest(
        **source_data
    )

    # ======================================================
    # OBSERVATION CREATION
    # ======================================================

    assert observation is not None

    print(
        "Observation Creation        : PASS"
    )

    # ======================================================
    # IDENTITY TRANSFER
    # ======================================================

    assert (
        observation.title
        == source_data["title"]
    )

    assert (
        observation.description
        == source_data["description"]
    )

    assert (
        observation.source
        == source_data["source"]
    )

    assert (
        observation.category
        == source_data["category"]
    )

    assert (
        observation.entity
        == source_data["entity"]
    )

    print(
        "Identity / Content Transfer : PASS"
    )

    # ======================================================
    # CONFIDENCE TRANSFER
    # ======================================================

    assert (
        observation.confidence
        == 85.0
    )

    print(
        "Confidence Transfer          : PASS"
    )

    # ======================================================
    # TIMESTAMP
    # ======================================================

    assert (
        observation.timestamp
        is not None
    )

    print(
        "Observation Timestamp        : PASS"
    )

    # ======================================================
    # REGISTRY HAND-OFF
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
        "Registry Hand-off            : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    assert (
        source_data
        == source_copy
    )

    print(
        "Input Immutability           : PASS"
    )

    # ======================================================
    # NUMERIC RANGE PROTECTION
    # ======================================================

    high = adapter.ingest(
        title="High Confidence",
        description="Test",
        source="Synthetic",
        category="Test",
        entity="TEST",
        confidence=150.0,
    )

    low = adapter.ingest(
        title="Low Confidence",
        description="Test",
        source="Synthetic",
        category="Test",
        entity="TEST",
        confidence=-25.0,
    )

    assert (
        high.confidence
        == 100.0
    )

    assert (
        low.confidence
        == 0.0
    )

    print(
        "Confidence Range Protection  : PASS"
    )

    # ======================================================
    # INVALID CONFIDENCE PROTECTION
    # ======================================================

    invalid = adapter.ingest(
        title="Invalid Confidence",
        description="Test",
        source="Synthetic",
        category="Test",
        entity="TEST",
        confidence="invalid",
    )

    assert (
        invalid.confidence
        == 0.0
    )

    print(
        "Invalid Confidence Protection: PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        observation,
        "valuation"
    )

    assert not hasattr(
        observation,
        "opportunity_score"
    )

    assert not hasattr(
        observation,
        "catalyst_score"
    )

    print(
        "No Analytical Fabrication     : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL → OBSERVATION "
        "ADAPTER : PASS"
    )


if __name__ == "__main__":
    main()
