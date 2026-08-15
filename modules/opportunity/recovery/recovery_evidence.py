"""
EIOS
Everest Investment Operating System

Recovery Evidence Model

Purpose:
Defines the passive evidence record consumed by the
Multi-Signal Recovery Engine.

Architecture:

Signal
    ↓
Temporal Signal Intelligence
    ↓
Recovery Detection
    ↓
RecoveryEvidence
    ↓
Multi-Signal Recovery Engine
    ↓
Multi-Signal Recovery Assessment

Design Principles:
- Passive data model only.
- No calculations.
- No persistence.
- No scoring.
- No valuation.
- No investment decision.
- No company-specific logic.
- No sector-specific logic.
- Source identity remains explicit.
- Signal identity remains explicit.
"""


from dataclasses import dataclass

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryAssessment,
)

from modules.opportunity.signals.signal_model import (
    SignalDomain,
)


# ==========================================================
# RECOVERY EVIDENCE
# ==========================================================


@dataclass
class RecoveryEvidence:
    """
    Passive evidence wrapper connecting a recovery assessment
    to its originating signal and independent source.

    The Multi-Signal Recovery Engine uses this object to
    determine breadth and corroboration without treating
    repeated observations from the same source as independent
    evidence.
    """

    # ------------------------------------------------------
    # Signal Identity
    # ------------------------------------------------------

    signal_id: str = ""

    # ------------------------------------------------------
    # Recovery Assessment
    # ------------------------------------------------------

    recovery_assessment: RecoveryAssessment = None

    # ------------------------------------------------------
    # Independent Source Identity
    # ------------------------------------------------------

    source_key: str = ""

    # ------------------------------------------------------
    # Intelligence Domain
    # ------------------------------------------------------

    domain: SignalDomain = (
        SignalDomain.COMPANY
    )


__all__ = [
    "RecoveryEvidence",
]