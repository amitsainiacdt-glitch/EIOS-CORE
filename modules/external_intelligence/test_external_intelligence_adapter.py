"""
EIOS
Everest Investment Operating System

External Intelligence Adapter Test
===================================

Validates the controlled boundary between external
Observations and the EIOS Intelligence Mesh.

No internet access is performed.
"""

from datetime import datetime

from modules.external_intelligence.external_intelligence_adapter import (
    ExternalIntelligenceAdapter,
)

from modules.observation.observation import (
    Observation,
)

from modules.research_context.research_context import (
    ResearchContext,
)


def make_observation():

    return Observation(
        title="Industrial demand acceleration",
        description=(
            "External source reports improving "
            "industrial demand."
        ),
        source="Synthetic External Source",
        category="External Web",
        entity="The Anup Engineering Limited",
        confidence=85.0,
        timestamp=datetime(
            2026,
            8,
            18,
            13,
            0,
            0,
        ),
    )


def main():

    print("=" * 60)
    print(
        "EIOS EXTERNAL INTELLIGENCE ADAPTER TEST"
    )
    print("=" * 60)

    # ======================================================
    # TEST 1 — CONTEXT VALIDATION
    # ======================================================

    context = ResearchContext()

    adapter = ExternalIntelligenceAdapter(
        context
    )

    assert adapter.context is context

    print(
        "Test 1 — Adapter Creation          : PASS"
    )

    # ======================================================
    # TEST 2 — OBSERVATION CREATION
    # ======================================================

    observation = make_observation()

    assert observation is not None

    print(
        "Test 2 — Observation Input         : PASS"
    )

    # ======================================================
    # TEST 3 — PUBLISH
    # ======================================================

    intelligence = adapter.publish(
        observation
    )

    assert intelligence is not None

    print(
        "Test 3 — Intelligence Creation     : PASS"
    )

    # ======================================================
    # TEST 4 — IDENTITY PRESERVATION
    # ======================================================

    assert (
        intelligence.title
        == observation.title
    )

    assert (
        intelligence.entity
        == observation.entity
    )

    assert (
        intelligence.category
        == observation.category
    )

    assert (
        intelligence.confidence
        == observation.confidence
    )

    print(
        "Test 4 — Identity Preservation     : PASS"
    )

    # ======================================================
    # TEST 5 — SOURCE
    # ======================================================

    assert (
        intelligence.source_engine
        == "ExternalResearch"
    )

    print(
        "Test 5 — Source Classification      : PASS"
    )

    # ======================================================
    # TEST 6 — SOURCE EVIDENCE
    # ======================================================

    assert (
        intelligence.evidence
        == [
            observation.source
        ]
    )

    print(
        "Test 6 — Source Preservation         : PASS"
    )

    # ======================================================
    # TEST 7 — CONCLUSION
    # ======================================================

    assert (
        intelligence.conclusion
        == observation.description
    )

    print(
        "Test 7 — Conclusion Preservation    : PASS"
    )

    # ======================================================
    # TEST 8 — TIMESTAMP
    # ======================================================

    assert (
        intelligence.timestamp
        == observation.timestamp
    )

    print(
        "Test 8 — Timestamp Preservation     : PASS"
    )

    # ======================================================
    # TEST 9 — INTELLIGENCE MESH
    # ======================================================

    assert (
        context.get_intelligence_mesh().count()
        == 1
    )

    assert (
        context.get_intelligence_mesh().get_all()[0]
        is intelligence
    )

    print(
        "Test 9 — Intelligence Mesh Handoff  : PASS"
    )

    # ======================================================
    # TEST 10 — CONTEXT PUBLICATION
    # ======================================================

    assert (
        len(
            context.get_intelligence_mesh().get_all()
        )
        == 1
    )

    print(
        "Test 10 — ResearchContext Handoff  : PASS"
    )

    # ======================================================
    # TEST 11 — NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        intelligence,
        "valuation",
    )

    assert not hasattr(
        intelligence,
        "opportunity_score",
    )

    assert not hasattr(
        intelligence,
        "catalyst_score",
    )

    print(
        "Test 11 — No Analytical Fabrication : PASS"
    )

    # ======================================================
    # TEST 12 — MULTIPLE OBSERVATIONS
    # ======================================================

    second = Observation(
        title="New capacity announced",
        description=(
            "External source reports a new "
            "capacity development."
        ),
        source="Synthetic Source 2",
        category="External Web",
        entity="The Anup Engineering Limited",
        confidence=75.0,
        timestamp=datetime(
            2026,
            8,
            18,
            13,
            1,
            0,
        ),
    )

    published = adapter.publish_many(
        [
            second,
        ]
    )

    assert len(
        published
    ) == 1

    assert (
        context.get_intelligence_mesh().count()
        == 2
    )

    print(
        "Test 12 — Multiple Publication     : PASS"
    )

    # ======================================================
    # TEST 13 — NONE OBSERVATION
    # ======================================================

    try:

        adapter.publish(
            None
        )

        raise AssertionError(
            "None observation should fail"
        )

    except ValueError:

        pass

    print(
        "Test 13 — Invalid Observation Guard : PASS"
    )

    # ======================================================
    # TEST 14 — NONE CONTEXT
    # ======================================================

    try:

        ExternalIntelligenceAdapter(
            None
        )

        raise AssertionError(
            "None context should fail"
        )

    except ValueError:

        pass

    print(
        "Test 14 — Context Validation         : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL INTELLIGENCE ADAPTER : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()