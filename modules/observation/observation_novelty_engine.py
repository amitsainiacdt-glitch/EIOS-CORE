"""
EIOS
Everest Investment Operating System

Observation Novelty Engine
==========================

Purpose
-------
Determines whether an incoming Observation contains information
that has already been observed by EIOS.

Architecture
------------

External Research
        ↓
Observation
        ↓
ObservationNoveltyEngine
        ↓
   ┌────┴────┐
   │         │
  NEW     DUPLICATE
   │         │
   ↓         ↓
retain     ignore

Design Principles
-----------------
- Deterministic.
- Passive with respect to investment analysis.
- No valuation.
- No opportunity scoring.
- No signal generation.
- No external retrieval.
- Does not modify Observation.
- Uses content identity rather than timestamp.
- Same information from the same source should not be
  repeatedly ingested.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable

from .observation import Observation


# ==========================================================
# NOVELTY RESULT
# ==========================================================


@dataclass(frozen=True)
class ObservationNoveltyResult:
    """
    Result of a novelty assessment.
    """

    is_new: bool

    fingerprint: str

    matched_observation: Observation | None = None

    reason: str = ""


# ==========================================================
# NOVELTY ENGINE
# ==========================================================


class ObservationNoveltyEngine:
    """
    Determines whether an Observation is new relative to
    previously registered observations.

    The engine does not persist observations itself.

    The caller supplies the existing observations.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    def assess(
        self,
        observation: Observation,
        existing_observations: Iterable[Observation],
    ) -> ObservationNoveltyResult:
        """
        Determine whether `observation` is new.

        Two observations are considered duplicates when their
        normalized identity fields produce the same fingerprint.

        Timestamp is deliberately excluded.

        This means the same article retrieved on different
        research runs is still recognized as the same
        information.
        """

        if observation is None:
            raise ValueError(
                "observation must not be None"
            )

        fingerprint = self.fingerprint(
            observation
        )

        for existing in existing_observations:

            if existing is None:
                continue

            existing_fingerprint = self.fingerprint(
                existing
            )

            if existing_fingerprint == fingerprint:

                return ObservationNoveltyResult(
                    is_new=False,
                    fingerprint=fingerprint,
                    matched_observation=existing,
                    reason=(
                        "Observation matches an existing "
                        "observation."
                    ),
                )

        return ObservationNoveltyResult(
            is_new=True,
            fingerprint=fingerprint,
            matched_observation=None,
            reason=(
                "Observation has not previously been "
                "registered."
            ),
        )

    # ======================================================
    # FINGERPRINT
    # ======================================================

    @classmethod
    def fingerprint(
        cls,
        observation: Observation,
    ) -> str:
        """
        Create a deterministic fingerprint for an observation.

        Timestamp is intentionally excluded.

        The fingerprint is based on:

            title
            description
            source
            category
            entity
        """

        if observation is None:
            raise ValueError(
                "observation must not be None"
            )

        identity = "|".join(
            [
                cls._normalize(
                    observation.title
                ),
                cls._normalize(
                    observation.description
                ),
                cls._normalize(
                    observation.source
                ),
                cls._normalize(
                    observation.category
                ),
                cls._normalize(
                    observation.entity
                ),
            ]
        )

        return hashlib.sha256(
            identity.encode(
                "utf-8"
            )
        ).hexdigest()

    # ======================================================
    # NORMALIZATION
    # ======================================================

    @staticmethod
    def _normalize(
        value: str | None,
    ) -> str:
        """
        Normalize text before fingerprinting.

        The normalization is intentionally conservative.

        It:
        - handles None
        - converts to string
        - strips surrounding whitespace
        - collapses repeated whitespace
        - normalizes case
        """

        if value is None:
            return ""

        text = str(value).strip()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.casefold()


# ==========================================================
# EXPORTS
# ==========================================================


__all__ = [
    "ObservationNoveltyResult",
    "ObservationNoveltyEngine",
]