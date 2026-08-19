"""
EIOS
Everest Investment Operating System

Signal Cluster → Catalyst Bridge
================================

Purpose
-------
Provides a controlled integration boundary between the
Signal Aggregation layer and the existing CatalystClassifier.

Architecture

Signal
    ↓
SignalAggregationEngine
    ↓
SignalCluster
    ↓
SignalClusterCatalystBridge
    ↓
CatalystClassifier
    ↓
CatalystClassification


Design Principles
-----------------
- Uses the existing CatalystClassifier.
- Does not create a second Catalyst engine.
- Does not mutate Signal objects.
- Does not mutate SignalCluster.
- Does not perform valuation.
- Does not score opportunities.
- Does not make investment decisions.
- Preserves Signal identity.
- Preserves CatalystClassifier reasoning.
- Preserves unclassified signals.
- Provides an explicit boundary between
  signal aggregation and catalyst classification.
"""

from __future__ import annotations

from modules.opportunity.catalyst.catalyst_classifier import (
    CatalystClassification,
    CatalystClassifier,
)

from modules.opportunity.signals.signal_aggregation import (
    SignalCluster,
)


class SignalClusterCatalystBridge:
    """
    Controlled handoff from SignalCluster to the existing
    CatalystClassifier.

    This class performs orchestration only.

    All catalyst classification remains inside
    CatalystClassifier.
    """

    def __init__(
        self,
        classifier: CatalystClassifier | None = None,
    ) -> None:

        self.classifier = (
            classifier
            if classifier is not None
            else CatalystClassifier()
        )

    # ======================================================
    # PUBLIC API
    # ======================================================

    def classify(
        self,
        *,
        cluster: SignalCluster,
    ) -> CatalystClassification:
        """
        Classify the Signals contained inside a SignalCluster.

        The cluster itself is not modified.

        The contained Signal objects are passed directly to
        the existing CatalystClassifier.

        The cluster theme is supplied as causal-chain context.
        """

        if cluster is None:
            raise ValueError(
                "cluster must not be None"
            )

        signals = list(
            cluster.signals
        )

        # --------------------------------------------------
        # EMPTY CLUSTER
        # --------------------------------------------------

        if not signals:

            return self.classifier.classify(
                signals=[],
                causal_chain=cluster.theme,
            )

        # --------------------------------------------------
        # EXISTING CATALYST CLASSIFIER
        # --------------------------------------------------

        return self.classifier.classify(
            signals=signals,
            causal_chain=cluster.theme,
        )


__all__ = [
    "SignalClusterCatalystBridge",
]