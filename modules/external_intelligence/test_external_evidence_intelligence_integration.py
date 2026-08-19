"""
EIOS
Everest Investment Operating System

External Evidence → Intelligence Integration Test
===================================================

Validates the controlled integration:

External Observation
        ↓
EvidenceEngine
        ↓
Canonical Evidence
        ↓
EvidenceIntelligenceAdapter
        ↓
ResearchContext
        ↓
IntelligenceMesh

The existing Opportunity Evidence path is also verified:

Observation
        ↓
EvidenceAssessmentEngine
        ↓
Opportunity EvidenceItem
        ↓
OpportunityEvidenceEngine

Design Principle
----------------
The canonical Evidence path and Opportunity EvidenceItem path
remain separate contracts.

This test does not modify production orchestration.
"""

from datetime import datetime

from modules.evidence.evidence_engine import (
    EvidenceEngine,
)

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_assessment_engine import (
    EvidenceAssessmentEngine,
)

from modules.external_intelligence.evidence_intelligence_adapter import (
    EvidenceIntelligenceAdapter,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.opportunity.evidence_engine import (
    OpportunityEvidenceEngine,
)

from modules.research_context.research_context import (
    ResearchContext,
)


def main() -> None:

    print("=" * 60)
    print(
        "EIOS EXTERNAL EVIDENCE → INTELLIGENCE "
        "INTEGRATION TEST"
    )
    print("=" * 60)

    # ======================================================
    # CONTEXT
    # ======================================================

    context = ResearchContext()

    assert context is not None

    print(
        "Test 1 — ResearchContext Creation       : PASS"
    )

    # ======================================================
    # EXTERNAL OBSERVATION
    # ======================================================

    observation_engine = ObservationEngine()

    observation = observation_engine.observe(
        title="Industrial demand improvement",
        description=(
            "External research indicates improving "
            "industrial demand for the company."
        ),
        source="https://example.com/industrial-demand",
        category="External Web",
        entity="Tata Motors",
        confidence=80.0,
    )

    assert observation is not None

    print(
        "Test 2 — External Observation           : PASS"
    )

    # ======================================================
    # CANONICAL EVIDENCE
    # ======================================================

    evidence_engine = EvidenceEngine()

    evidence = (
        evidence_engine.create_from_observation(
            observation
        )
    )

    assert evidence is not None

    assert (
        evidence.title
        == observation.title
    )

    assert (
        evidence.description
        == observation.description
    )

    assert (
        evidence.source
        == observation.source
    )

    assert (
        evidence.entity
        == observation.entity
    )

    assert (
        evidence.confidence
        == observation.confidence
    )

    assert (
        evidence.reliability
        == 100
    )

    print(
        "Test 3 — Canonical Evidence Creation    : PASS"
    )

    # ======================================================
    # EVIDENCE INTELLIGENCE ADAPTER
    # ======================================================

    adapter = EvidenceIntelligenceAdapter(
        context
    )

    intelligence = adapter.publish(
        evidence
    )

    assert intelligence is not None

    print(
        "Test 4 — Evidence → Intelligence        : PASS"
    )

    # ======================================================
    # INTELLIGENCE IDENTITY
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
        intelligence.conclusion
        == evidence.description
    )

    assert (
        intelligence.entity
        == evidence.entity
    )

    assert (
        intelligence.confidence
        == evidence.confidence
    )

    print(
        "Test 5 — Intelligence Identity           : PASS"
    )

    # ======================================================
    # PROVENANCE
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
        "Test 6 — Provenance Preservation         : PASS"
    )

    # ======================================================
    # INTELLIGENCE MESH
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
        "Test 7 — Intelligence Mesh Handoff      : PASS"
    )

    # ======================================================
    # OPPORTUNITY EVIDENCE PATH
    # ======================================================

    assessment = EvidenceAssessment(
        category="Demand",
        direction="Supporting",
        strength=85.0,
        confidence=80.0,
        independent_confirmation=1,
        is_primary_source=False,
        is_time_sensitive=True,
        notes=(
            "Explicit assessment for integration test."
        ),
    )

    assessment_engine = (
        EvidenceAssessmentEngine()
    )

    evidence_item = (
        assessment_engine.assess(
            observation=observation,
            assessment=assessment,
            evidence_id="EXT-INT-001",
        )
    )

    assert evidence_item is not None

    assert (
        evidence_item.statement
        == observation.description
    )

    assert (
        evidence_item.source
        == observation.source
    )

    assert (
        evidence_item.category
        == "Demand"
    )

    print(
        "Test 8 — Opportunity Evidence Path      : PASS"
    )

    # ======================================================
    # OPPORTUNITY ENGINE
    # ======================================================

    opportunity_engine = (
        OpportunityEvidenceEngine()
    )

    pack = opportunity_engine.analyze(
        company="Tata Motors",
        supporting_evidence=[
            evidence_item
        ],
        contradictory_evidence=[],
        assumptions=[
            "Industrial demand improvement persists."
        ],
        kill_switches=[
            "Material demand reversal"
        ],
        monitoring_signals=[
            "Industrial demand growth"
        ],
    )

    assert pack is not None

    assert (
        len(
            pack.supporting_evidence
        )
        == 1
    )

    assert (
        pack.supporting_evidence[0]
        is evidence_item
    )

    print(
        "Test 9 — Opportunity Engine Preserved   : PASS"
    )

    # ======================================================
    # ANALYTICAL BOUNDARY
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
        "Test 10 — Analytical Boundary           : PASS"
    )

    # ======================================================
    # EVIDENCE IMMUTABILITY
    # ======================================================

    assert (
        evidence.title
        == observation.title
    )

    assert (
        evidence.description
        == observation.description
    )

    assert (
        evidence.source
        == observation.source
    )

    assert (
        evidence.entity
        == observation.entity
    )

    print(
        "Test 11 — Evidence Identity Preserved   : PASS"
    )

    # ======================================================
    # OBSERVATION IMMUTABILITY
    # ======================================================

    assert (
        observation.title
        == "Industrial demand improvement"
    )

    assert (
        observation.entity
        == "Tata Motors"
    )

    assert (
        observation.source
        == "https://example.com/industrial-demand"
    )

    print(
        "Test 12 — Observation Identity Preserved: PASS"
    )

    # ======================================================
    # FINAL MESH STATE
    # ======================================================

    assert (
        context.get_intelligence_mesh().count()
        == 1
    )

    print(
        "Test 13 — Final Intelligence State      : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL EVIDENCE → INTELLIGENCE "
        "INTEGRATION : ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()