"""
EIOS
Everest Investment Operating System

Opportunity Evidence Engine Test
"""

from modules.opportunity.evidence_engine import (
    EvidenceItem,
    KillSwitch,
    OpportunityEvidenceEngine,
)


def main():

    engine = OpportunityEvidenceEngine()

    print("=" * 60)
    print("EIOS OPPORTUNITY EVIDENCE ENGINE TEST")
    print("=" * 60)

    # ======================================================
    # CASE 1 — STRONG EVIDENCE
    # ======================================================

    strong = engine.analyze(
        company="Test Company",
        supporting_evidence=[
            EvidenceItem(
                evidence_id="EV-001",
                statement="Order inflows accelerated.",
                source="Company Filing",
                category="Company",
                strength=90.0,
                confidence=90.0,
                independent_confirmation=2,
                is_primary_source=True,
            ),
            EvidenceItem(
                evidence_id="EV-002",
                statement="Industry capex is increasing.",
                source="Industry Data",
                category="Macro",
                strength=85.0,
                confidence=85.0,
                independent_confirmation=3,
                is_primary_source=True,
            ),
            EvidenceItem(
                evidence_id="EV-003",
                statement="Capacity utilisation is improving.",
                source="Industry Research",
                category="Sector",
                strength=80.0,
                confidence=85.0,
                independent_confirmation=2,
            ),
        ],
        contradictory_evidence=[
            EvidenceItem(
                evidence_id="EV-004",
                statement="Commodity prices remain volatile.",
                source="Market Data",
                category="Commodity",
                direction="Contradictory",
                strength=20.0,
                confidence=70.0,
                independent_confirmation=1,
            )
        ],
        assumptions=[
            "Industrial capex remains elevated.",
            "Company converts orders into revenue.",
        ],
        kill_switches=[
            KillSwitch(
                name="Order Collapse",
                condition="Order inflows decline materially.",
                severity="High",
                measurable=True,
                threshold="Two consecutive quarters",
                monitoring_frequency="Quarterly",
            )
        ],
        monitoring_signals=[
            "Order inflows",
            "Capacity utilisation",
            "Customer capex",
        ],
    )

    print("\nCase 1 — Strong Evidence")
    print(f"Evidence Score : {strong.evidence_score:.2f}")
    print(f"Confidence     : {strong.confidence:.2f}")
    print(f"Evidence Gaps  : {len(strong.evidence_gaps)}")
    print(f"Sufficient     : {strong.sufficiently_supported}")

    assert strong.evidence_score >= 60.0
    assert strong.confidence >= 60.0
    assert strong.sufficiently_supported

    print("PASS")

    # ======================================================
    # CASE 2 — WEAK EVIDENCE
    # ======================================================

    weak = engine.analyze(
        company="Weak Company",
        supporting_evidence=[
            EvidenceItem(
                evidence_id="EV-101",
                statement="Management sounded positive.",
                source="News Article",
                category="Management",
                strength=40.0,
                confidence=45.0,
                independent_confirmation=0,
            )
        ],
        assumptions=[
            "Management commentary proves demand.",
        ],
    )

    print("\nCase 2 — Weak Evidence")
    print(f"Evidence Score : {weak.evidence_score:.2f}")
    print(f"Confidence     : {weak.confidence:.2f}")
    print(f"Sufficient     : {weak.sufficiently_supported}")

    assert not weak.sufficiently_supported
    assert len(weak.evidence_gaps) > 0

    print("PASS")

    # ======================================================
    # CASE 3 — SERIOUS CONTRADICTION
    # ======================================================

    contradiction = engine.analyze(
        company="Contradiction Company",
        supporting_evidence=[
            EvidenceItem(
                evidence_id="EV-201",
                statement="Orders are growing.",
                source="Company Filing",
                category="Company",
                strength=85.0,
                confidence=90.0,
                independent_confirmation=2,
                is_primary_source=True,
            ),
            EvidenceItem(
                evidence_id="EV-202",
                statement="Capacity is expanding.",
                source="Company Filing",
                category="Capacity",
                strength=80.0,
                confidence=85.0,
                independent_confirmation=2,
                is_primary_source=True,
            ),
            EvidenceItem(
                evidence_id="EV-203",
                statement="Sector demand is improving.",
                source="Industry Data",
                category="Sector",
                strength=80.0,
                confidence=85.0,
                independent_confirmation=2,
            ),
        ],
        contradictory_evidence=[
            EvidenceItem(
                evidence_id="EV-204",
                statement="Major customer has reduced orders.",
                source="Customer Evidence",
                category="Customer",
                direction="Contradictory",
                strength=90.0,
                confidence=90.0,
                independent_confirmation=2,
            )
        ],
        assumptions=[
            "Customer weakness is temporary.",
        ],
        kill_switches=[
            KillSwitch(
                name="Customer Loss",
                condition="Major customer permanently reduces orders.",
                severity="Critical",
                measurable=True,
                threshold="More than 20% decline",
                monitoring_frequency="Quarterly",
            )
        ],
        monitoring_signals=[
            "Customer orders",
        ],
    )

    print("\nCase 3 — Serious Contradiction")
    print(f"Evidence Score : {contradiction.evidence_score:.2f}")
    print(f"Confidence     : {contradiction.confidence:.2f}")
    print(f"Warnings       : {len(contradiction.warnings)}")

    assert contradiction.confidence < strong.confidence
    assert len(contradiction.contradictory_evidence) == 1

    print("PASS")

    # ======================================================
    # CASE 4 — NO PRIMARY SOURCE
    # ======================================================

    secondary_only = engine.analyze(
        company="Secondary Source Company",
        supporting_evidence=[
            EvidenceItem(
                evidence_id="EV-301",
                statement="Industry demand appears strong.",
                source="News",
                category="Sector",
                strength=80.0,
                confidence=80.0,
                independent_confirmation=2,
            ),
            EvidenceItem(
                evidence_id="EV-302",
                statement="Analysts expect growth.",
                source="Broker Research",
                category="Earnings",
                strength=75.0,
                confidence=75.0,
                independent_confirmation=2,
            ),
            EvidenceItem(
                evidence_id="EV-303",
                statement="Investor interest is rising.",
                source="Market Commentary",
                category="Market",
                strength=70.0,
                confidence=70.0,
                independent_confirmation=2,
            ),
        ],
        assumptions=[
            "Secondary research is accurate.",
        ],
        kill_switches=[
            KillSwitch(
                name="Demand Reversal",
                condition="Industry demand weakens.",
            )
        ],
        monitoring_signals=[
            "Industry demand",
        ],
    )

    print("\nCase 4 — No Primary Source")
    print(f"Evidence Gaps : {len(secondary_only.evidence_gaps)}")
    print(f"Sufficient     : {secondary_only.sufficiently_supported}")

    assert any(
        "primary-source" in gap.lower()
        for gap in secondary_only.evidence_gaps
    )

    print("PASS")

    # ======================================================
    # CASE 5 — NO KILL SWITCH
    # ======================================================

    no_kill_switch = engine.analyze(
        company="No Kill Switch Company",
        supporting_evidence=[
            EvidenceItem(
                evidence_id="EV-401",
                statement="Orders increasing.",
                source="Company Filing",
                category="Company",
                strength=90.0,
                confidence=90.0,
                independent_confirmation=2,
                is_primary_source=True,
            ),
            EvidenceItem(
                evidence_id="EV-402",
                statement="Capex cycle improving.",
                source="Industry Data",
                category="Macro",
                strength=85.0,
                confidence=85.0,
                independent_confirmation=2,
                is_primary_source=True,
            ),
            EvidenceItem(
                evidence_id="EV-403",
                statement="Utilisation improving.",
                source="Industry Data",
                category="Sector",
                strength=80.0,
                confidence=85.0,
                independent_confirmation=2,
            ),
        ],
        assumptions=[
            "Demand remains strong.",
        ],
        monitoring_signals=[
            "Orders",
            "Utilisation",
        ],
    )

    print("\nCase 5 — No Kill Switch")
    print(f"Evidence Gaps : {len(no_kill_switch.evidence_gaps)}")

    assert any(
        "kill switches" in gap.lower()
        for gap in no_kill_switch.evidence_gaps
    )

    assert not no_kill_switch.sufficiently_supported

    print("PASS")

    # ======================================================
    # FINAL
    # ======================================================

    print("\n" + "=" * 60)
    print("OPPORTUNITY EVIDENCE ENGINE : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
    