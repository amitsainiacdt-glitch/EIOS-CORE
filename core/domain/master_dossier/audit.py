"""
Audit management for Master Dossiers.

Responsible for:
- Recording changes
- Maintaining audit history
- Providing traceability
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class AuditEntry:
    """
    Represents a single audit record.
    """

    timestamp: datetime
    action: str
    user: str
    description: str


class MasterDossierAuditManager:
    """
    Manages audit history for a Master Dossier.
    """

    def __init__(self):
        self._entries: List[AuditEntry] = []

    def record(
        self,
        action: str,
        user: str,
        description: str
    ):

        self._entries.append(
            AuditEntry(
                timestamp=datetime.utcnow(),
                action=action,
                user=user,
                description=description
            )
        )

    def history(self) -> List[AuditEntry]:
        """
        Returns complete audit history.
        """
        return self._entries

    def clear(self):
        """
        Clears audit history.
        """
        self._entries.clear()