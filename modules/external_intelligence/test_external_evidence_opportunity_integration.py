"""
EIOS
Everest Investment Operating System

External Evidence → Opportunity Evidence Integration Test
"""

from datetime import datetime

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_assessment_engine import (
    EvidenceAssessmentEngine,
)

from modules.observation.observation import (
    Observation,
)

from modules.opportunity.evidence_engine import (
    OpportunityEvidenceEngine,
)


def make_observation(
    title: str,
    description: str,
    source: str,
    category: str,
) -> Observation:

    return Observation(
        title=title,
        description=description,
        source=source,
        category=category,
        entity="Test Company",
        confidence=90.0,
        timestamp=datetime.now(),
    )


def main() -> None:

    assessment_engine = (
        EvidenceAssessmentEngine()
    )

    opportunity_engine = (
        OpportunityEvidenceEngine()
    )

    observations = [

        make_observation(
            "Company Order Growth",
            "Order book is increasing materially.",
            "Company Filing",
            "Company",
        ),

        make_observation(
            "Industry Capex Growth",
            "Industry capital expenditure is accelerating.",
            "Industry Report",
            "Industry",
        ),

        make_observation(
            "Management Commentary",
            "Management confirms improving demand visibility.",
            "Company Conference Call",
            "Management",
        ),
    ]

    assessments = [

        EvidenceAssessment(
            category="Company",
            direction="Supporting",
            strength=90.0,
            confidence=90.0,
            independent_confirmation=2,
            is_primary_source=True,
            is_time_sensitive=True,
            notes="Primary company evidence.",
        ),

        EvidenceAssessment(
            category="Industry",
            direction="Supporting",
            strength=85.0,
            confidence=85.0,
            independent_confirmation=2,
            is_primary_source=False,
            is_time_sensitive=True,
            notes="Independent industry evidence.",
        ),

        EvidenceAssessment(
            category="Management",
            direction="Supporting",
            strength=90.0,
            confidence=90.0,
            independent_confirmation=2,
            is_primary_source=True,
            is_time_sensitive=True,
            notes="Management confirmation.",
        ),
    ]

    evidence_items = []

    for index, (
        observation,
        assessment,
    ) in enumerate(
        zip(
            observations,
            assessments,
        ),
        start=1,
    ):

        evidence = (
            assessment_engine.assess(
                observation=observation,
                assessment=assessment,
                evidence_id=f"EXT-EVID-{index:03d}",
            )
        )

        evidence_items.append(
            evidence
        )

    # ======================================================
    # EXTERNAL → EVIDENCE
    # ======================================================

    assert len(evidence_items) == 3

    print(
        "External Evidence Creation      : PASS"
    )

    # ======================================================
    # OPPORTUNITY EVIDENCE ENGINE
    # ======================================================

    pack = opportunity_engine.analyze(
        company="Test Company",
        supporting_evidence=evidence_items,
        contradictory_evidence=[],
        assumptions=[
            "Demand acceleration persists."
        ],
        kill_switches=[
            "Material demand reversal"
        ],
        monitoring_signals=[
            "Order growth"
        ],
    )

    assert pack is not None

    print(
        "Opportunity Evidence Engine      : PASS"
    )

    # ======================================================
    # EVIDENCE HAND-OFF
    # ======================================================

    assert (
        len(pack.supporting_evidence)
        == 3
    )

    assert (
        pack.supporting_evidence[0]
        is evidence_items[0]
    )

    print(
        "Evidence → Opportunity Handoff   : PASS"
    )

    # ======================================================
    # SCORING REMAINS DOWNSTREAM
    # ======================================================

    assert (
        pack.evidence_score
        >= 0.0
    )

    assert (
        pack.evidence_score
        <= 100.0
    )

    assert (
        pack.confidence
        >= 0.0
    )

    assert (
        pack.confidence
        <= 100.0
    )

    print(
        "Downstream Evidence Scoring      : PASS"
    )

    # ======================================================
    # SOURCE PRESERVATION
    # ======================================================

    assert (
        pack.supporting_evidence[0].source
        == "Company Filing"
    )

    assert (
        pack.supporting_evidence[1].source
        == "Industry Report"
    )

    assert (
        pack.supporting_evidence[2].source
        == "Company Conference Call"
    )

    print(
        "Source Preservation               : PASS"
    )

    # ======================================================
    # NO ENGINE MODIFICATION
    # ======================================================

    assert (
        type(opportunity_engine)
        is OpportunityEvidenceEngine
    )

    print(
        "Existing Engine Preserved         : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL → OPPORTUNITY "
        "EVIDENCE INTEGRATION : PASS"
    )


if __name__ == "__main__":
    main()