"""
EIOS
Everest Investment Operating System

Observation Persistence

Purpose:
Provides durable storage for EIOS observations.

Architecture:

ObservationRegistry
        ↓
ObservationPersistence
        ↓
Persistent Observation State

Design Principles:
- Persistence is separate from the Observation model.
- Persistence is separate from ObservationEngine.
- JSON is used initially as a simple durable store.
- No analytical logic.
- No novelty logic.
- No opportunity logic.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List

from .observation import Observation, ObservationProvenance


class ObservationPersistence:
    """
    Durable storage for Observation objects.

    The persistence layer is intentionally independent
    from ObservationEngine and ObservationRegistry.
    """

    def __init__(
        self,
        path: str | Path = "data/observations.json",
    ):

        self.path = Path(path)

    # ======================================================
    # SAVE
    # ======================================================

    def save(
        self,
        observations: List[Observation],
    ) -> None:
        """
        Persist observations to disk.
        """

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = []

        for observation in observations:

            item = asdict(
                observation
            )

            item["timestamp"] = (
                observation.timestamp.isoformat()
            )

            if observation.provenance is not None:
                retrieved_at = item["provenance"].get(
                    "retrieved_at"
                )
                if retrieved_at is not None:
                    item["provenance"]["retrieved_at"] = (
                        retrieved_at.isoformat()
                    )

            payload.append(item)

        self.path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    # ======================================================
    # LOAD
    # ======================================================

    def load(self) -> List[Observation]:
        """
        Load observations from disk.

        Missing storage is treated as an empty state.
        """

        if not self.path.exists():

            return []

        raw = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

        observations = []

        for item in raw:

            item = dict(item)

            item["timestamp"] = (
                datetime.fromisoformat(
                    item["timestamp"]
                )
            )

            provenance = item.get("provenance")
            if provenance is not None:
                provenance = dict(provenance)
                retrieved_at = provenance.get("retrieved_at")
                if retrieved_at is not None:
                    provenance["retrieved_at"] = datetime.fromisoformat(
                        retrieved_at
                    )
                item["provenance"] = ObservationProvenance(
                    **provenance
                )

            observations.append(
                Observation(**item)
            )

        return observations

    # ======================================================
    # EXISTS
    # ======================================================

    def exists(self) -> bool:
        """
        Return whether persistent observation state exists.
        """

        return self.path.exists()

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(self) -> None:
        """
        Remove persistent observation state.
        """

        if self.path.exists():

            self.path.unlink()


__all__ = [
    "ObservationPersistence",
]
