"""
EIOS
Everest Investment Operating System

Evidence → Intelligence Adapter Test
=====================================

Validates the controlled boundary:

Evidence
    ↓
EvidenceIntelligenceAdapter
    ↓
Intelligence
    ↓
ResearchContext
    ↓
IntelligenceMesh
"""

from datetime import datetime

from modules.evidence.evidence import Evidence

from modules.external_intelligence.evidence_intelligence_adapter import (
    EvidenceIntelligenceAdapter,
)

from modules.research_context.research_context import (
    ResearchContext,
)


def main() -> None:

    print("=" * 60)
    print("EIOS EVIDENCE → INTELLIGENCE ADAPTER TEST")
    print("=" * 60)

    # ======================================================
    # TEST 1 — ADAPTER CREATION
    # ======================================================

    context = ResearchContext()

    adapter = EvidenceIntelligenceAdapter(
        context
    )

    assert adapter is not None

    print(
        "Test 1 — Adapter Creation             : PASS"
    )

    # ======================================================
    # TEST 2 — EVIDENCE CREATION
    # ======================================================

    timestamp = datetime.now()

    evidence = Evidence(
        title="Industrial demand improvement",
        category="Demand",
        description=(
            "Industrial demand has improved "
            "according to the verified source."
        ),
        source="https://example.com/source",
        entity="Tata Motors",
        reliability=90.0,
        confidence=80.0,
        timestamp=timestamp,
    )

    original = {
        "title": evidence.title,
        "category": evidence.category,
        "description": evidence.description,
        "source": evidence.source,
        "entity": evidence.entity,
        "reliability": evidence.reliability,
        "confidence": evidence.confidence,
        "timestamp": evidence.timestamp,
    }

    print(
        "Test 2 — Evidence Creation             : PASS"
    )

    # ======================================================
    # TEST 3 — INTELLIGENCE CREATION
    # ======================================================

    intelligence = adapter.publish(
        evidence
    )

    assert intelligence is not None

    print(
        "Test 3 — Intelligence Creation         : PASS"
    )

    # ======================================================
    # TEST 4 — IDENTITY PRESERVATION
    # ======================================================

    assert (
        intelligence.title
        == evidence.title
    )

    assert (
        intelligence.category
        == evidence.category
    )

    assert (
        intelligence.entity
        == evidence.entity
    )

    assert (
        intelligence.conclusion
        == evidence.description
    )

    print(
        "Test 4 — Identity Preservation          : PASS"
    )

    # ======================================================
    # TEST 5 — PROVENANCE PRESERVATION
    # ======================================================

    assert (
        intelligence.evidence
        == [evidence.source]
    )

    assert (
        intelligence.source_engine
        == "EvidenceEngine"
    )

    assert (
        intelligence.timestamp
        == evidence.timestamp
    )

    print(
        "Test 5 — Provenance Preservation        : PASS"
    )

    # ======================================================
    # TEST 6 — CONFIDENCE TRANSFER
    # ======================================================

    assert (
        intelligence.confidence
        == evidence.confidence
    )

    print(
        "Test 6 — Confidence Transfer            : PASS"
    )

    # ======================================================
    # TEST 7 — INTELLIGENCE MESH HANDOFF
    # ======================================================

    mesh = (
        context.get_intelligence_mesh()
    )

    assert (
        mesh.count()
        == 1
    )

    assert (
        mesh.get_all()[0]
        is intelligence
    )

    print(
        "Test 7 — Intelligence Mesh Handoff     : PASS"
    )

    # ======================================================
    # TEST 8 — NO ANALYTICAL FABRICATION
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
        "Test 8 — No Analytical Fabrication     : PASS"
    )

    # ======================================================
    # TEST 9 — EVIDENCE IMMUTABILITY
    # ======================================================

    assert (
        evidence.title
        == original["title"]
    )

    assert (
        evidence.category
        == original["category"]
    )

    assert (
        evidence.description
        == original["description"]
    )

    assert (
        evidence.source
        == original["source"]
    )

    assert (
        evidence.entity
        == original["entity"]
    )

    assert (
        evidence.reliability
        == original["reliability"]
    )

    assert (
        evidence.confidence
        == original["confidence"]
    )

    assert (
        evidence.timestamp
        == original["timestamp"]
    )

    print(
        "Test 9 — Evidence Immutability          : PASS"
    )

    # ======================================================
    # TEST 10 — MISSING EVIDENCE GUARD
    # ======================================================

    try:

        adapter.publish(
            None
        )

        raise AssertionError(
            "None evidence was accepted"
        )

    except ValueError:

        pass

    print(
        "Test 10 — Missing Evidence Guard       : PASS"
    )

    # ======================================================
    # TEST 11 — TYPE GUARD
    # ======================================================

    try:

        adapter.publish(
            "invalid"
        )

        raise AssertionError(
            "Invalid evidence type was accepted"
        )

    except TypeError:

        pass

    print(
        "Test 11 — Evidence Type Guard           : PASS"
    )

    # ======================================================
    # TEST 12 — MULTIPLE PUBLICATION
    # ======================================================

    second = Evidence(
        title="Export order improvement",
        category="Orders",
        description=(
            "The company received a new "
            "international export order."
        ),
        source="https://example.com/order",
        entity="Tata Motors",
        reliability=85.0,
        confidence=75.0,
        timestamp=datetime.now(),
    )

    published = (
        adapter.publish_many(
            [
                second
            ]
        )
    )

    assert (
        len(published)
        == 1
    )

    assert (
        published[0].title
        == second.title
    )

    assert (
        mesh.count()
        == 2
    )

    print(
        "Test 12 — Multiple Evidence Publication : PASS"
    )

    # ======================================================
    # TEST 13 — FINAL STATE
    # ======================================================

    assert (
        context.get_intelligence_mesh().count()
        == 2
    )

    items = (
        context
        .get_intelligence_mesh()
        .get_all()
    )

    assert (
        items[0].title
        == evidence.title
    )

    assert (
        items[1].title
        == second.title
    )

    print(
        "Test 13 — Final State Integrity         : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EVIDENCE → INTELLIGENCE ADAPTER "
        ": ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()