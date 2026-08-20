"""
EIOS
Everest Investment Operating System

Historical Comparison Engine
============================

Purpose
-------
Compares a current Observation against a historical Observation.

Architecture
------------

Current Observation
        +
Historical Observation
        ↓
HistoricalComparisonEngine
        ↓
HistoricalComparison

Design Principles
-----------------
- Owns historical comparison logic only.
- Does not replace ObservationNoveltyEngine.
- Does not modify observations.
- Does not create Evidence.
- Does not create Signals.
- Does not create Catalysts.
- Does not perform valuation.
- Does not make investment decisions.
- Does not invent quantitative deltas.
- Does not infer positive or negative direction from arbitrary prose.
- Deterministic output.
"""

from __future__ import annotations

from modules.observation.historical_comparison import (
    ChangeDirection,
    ComparisonType,
    HistoricalComparison,
    Materiality,
)

from modules.observation.observation import (
    Observation,
)


class HistoricalComparisonEngine:
    """
    Compares two observations without mutating either one.
    """

    def compare(
        self,
        current_observation: Observation,
        historical_observation: Observation,
    ) -> HistoricalComparison:
        """
        Compare a current observation against a historical observation.

        The comparison deliberately ignores timestamp-only differences.

        A source difference alone does not constitute an information
        change. It is preserved as SOURCE_CHANGE so provenance remains
        visible.

        Textual changes in title or description are classified as
        INFORMATION_CHANGE.

        No direction or quantitative delta is inferred from free text.
        """

        if current_observation is None:
            raise ValueError(
                "current_observation must not be None"
            )

        if historical_observation is None:
            raise ValueError(
                "historical_observation must not be None"
            )

        # ------------------------------------------------------
        # INFORMATION COMPARISON
        # ------------------------------------------------------

        same_title = (
            current_observation.title.strip()
            == historical_observation.title.strip()
        )

        same_description = (
            current_observation.description.strip()
            == historical_observation.description.strip()
        )

        same_category = (
            current_observation.category.strip()
            == historical_observation.category.strip()
        )

        same_entity = (
            current_observation.entity.strip()
            == historical_observation.entity.strip()
        )

        same_source = (
            current_observation.source.strip()
            == historical_observation.source.strip()
        )

        # ------------------------------------------------------
        # IDENTICAL INFORMATION
        # ------------------------------------------------------

        if (
            same_title
            and same_description
            and same_category
            and same_entity
        ):

            if same_source:

                comparison_type = (
                    ComparisonType.NO_CHANGE
                )

            else:

                comparison_type = (
                    ComparisonType.SOURCE_CHANGE
                )

            return HistoricalComparison(
                current_observation=current_observation,
                historical_observation=historical_observation,
                comparison_type=comparison_type,
                change_detected=False,
                change_direction=(
                    ChangeDirection.UNKNOWN
                ),
                materiality=Materiality.UNKNOWN,
                delta=None,
                provenance=(
                    "Current and historical observations "
                    "preserved for provenance comparison."
                ),
            )

        # ------------------------------------------------------
        # INFORMATION CHANGE
        # ------------------------------------------------------

        return HistoricalComparison(
            current_observation=current_observation,
            historical_observation=historical_observation,
            comparison_type=(
                ComparisonType.INFORMATION_CHANGE
            ),
            change_detected=True,
            change_direction=(
                ChangeDirection.UNKNOWN
            ),
            materiality=Materiality.UNKNOWN,
            delta=None,
            provenance=(
                "Current and historical observations "
                "preserved for historical comparison."
            ),
        )


__all__ = [
    "HistoricalComparisonEngine",
]