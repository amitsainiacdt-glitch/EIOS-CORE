"""Verify governed Mispricing before any Asymmetry analysis."""

import hashlib
import json

from modules.external_intelligence.historical_comparison_asymmetry_eligibility_preview import HistoricalComparisonAsymmetryEligibilityPreview
from modules.external_intelligence.historical_comparison_opportunity_eligibility_preview_builder import HistoricalComparisonOpportunityEligibilityPreviewBuilder


class HistoricalComparisonAsymmetryEligibilityPreviewBuilder:
    REQUIRED_INPUTS = (
        "company", "scenarios", "assumptions",
        "invalidation_conditions", "disconfirming_evidence",
    )

    def build(self, *args, **kwargs):
        governed = HistoricalComparisonOpportunityEligibilityPreviewBuilder().build(*args, **kwargs)
        blockers = []
        if not governed.potential_mispricing:
            blockers.append("Materialized result no longer identifies potential mispricing.")
        warnings = (
            "Scenario probabilities must sum to approximately 100.",
            "Scenario assumptions, invalidation conditions, and disconfirming Evidence require explicit analyst input.",
        )
        identity = {
            "mispricing_creation_receipt_fingerprint": governed.mispricing_creation_receipt_fingerprint,
            "mispricing_fingerprint": governed.mispricing_fingerprint,
            "required_analysis_inputs": self.REQUIRED_INPUTS,
        }
        fingerprint = hashlib.sha256(
            json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()
        return HistoricalComparisonAsymmetryEligibilityPreview(
            fingerprint, not blockers, governed.company,
            governed.mispricing_fingerprint,
            governed.mispricing_creation_receipt_fingerprint,
            governed.mispricing_assessment_fingerprint,
            governed.mispricing_analysis_fingerprint,
            governed.potential_mispricing, governed.mispricing_score,
            governed.confidence, governed.gap_id,
            governed.expectation_gap_fingerprint, governed.catalyst_id,
            governed.catalyst_fingerprint, governed.valuation_fingerprint,
            governed.valuation_receipt_fingerprint, governed.signal_ids,
            governed.promoted_signal_ids, self.REQUIRED_INPUTS,
            tuple(blockers), warnings,
        )


__all__ = ["HistoricalComparisonAsymmetryEligibilityPreviewBuilder"]
