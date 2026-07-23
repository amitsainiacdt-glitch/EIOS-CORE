"""
Master Dossier
==============

The Master Dossier is the central business entity of EIOS.

Every company researched in EIOS is represented by exactly one
Master Dossier.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any


@dataclass
class MasterDossier:
    """
    Canonical representation of a company inside EIOS.
    """

    # ==========================================================
    # Company Identity
    # ==========================================================
    company_id: str
    company_name: str
    exchange: str
    sector: str
    industry: str

    # ==========================================================
    # Research Sections
    # ==========================================================
    business: Dict[str, Any] = field(default_factory=dict)
    financials: Dict[str, Any] = field(default_factory=dict)
    management: Dict[str, Any] = field(default_factory=dict)
    moat: Dict[str, Any] = field(default_factory=dict)
    valuation: Dict[str, Any] = field(default_factory=dict)
    risks: Dict[str, Any] = field(default_factory=dict)
    evidence: Dict[str, Any] = field(default_factory=dict)
    monitoring: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Metadata
    # ==========================================================
    version: str = "0.1.0"

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ==========================================================
    # Utility Methods
    # ==========================================================
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the dossier into a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MasterDossier":
        """
        Create a MasterDossier from a dictionary.
        """
        return cls(**data)