"""Explicit governed Mispricing materialization with append-only receipts."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path

from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_analysis_preview_builder import HistoricalComparisonMispricingAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_mispricing_assessment_decision import HistoricalComparisonMispricingAssessmentDecision, HistoricalComparisonMispricingAssessmentDisposition
from modules.external_intelligence.historical_comparison_mispricing_creation_receipt import HistoricalComparisonMispricingCreationReceipt
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.opportunity.expectation_gap_engine import ExpectationGapEngine
from modules.opportunity.mispricing_engine import MispricingAssessment, MispricingEngine


class HistoricalComparisonMispricingCreationLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("Mispricing creation path must identify a file")

    def materialize(
        self, inputs, reviews, catalyst_assessment, catalyst_creation,
        gap_assessment, gap_creation, valuation, valuation_receipt, assessment,
        *, cmp, creator, rationale, created_at, builder=None,
        mispricing_assumptions=(), mispricing_invalidation_conditions=(), **kwargs,
    ):
        if not isinstance(assessment, HistoricalComparisonMispricingAssessmentDecision):
            raise ValueError("assessment must be a Mispricing assessment")
        if assessment.disposition != HistoricalComparisonMispricingAssessmentDisposition.APPROVED:
            raise ValueError("only an Approved Mispricing assessment may be materialized")
        creator = self._text(creator, "creator")
        rationale = self._text(rationale, "rationale")
        created_at = self._datetime(created_at)
        try:
            if created_at < assessment.reviewed_at:
                raise ValueError("Mispricing creation timestamp precedes its human assessment")
        except TypeError as exc:
            raise ValueError("Mispricing timestamps use inconsistent timezone awareness") from exc

        existing = self.read_all()
        assessment_fingerprint = self.assessment_fingerprint(assessment)
        if any(item.assessment_fingerprint == assessment_fingerprint for item in existing):
            raise ValueError("this approved Mispricing assessment was already materialized")

        valuation_fingerprint = HistoricalComparisonValuationSnapshotLedger.valuation_fingerprint(valuation)
        valuation_receipt_fingerprint = HistoricalComparisonMispricingAnalysisPreviewBuilder.valuation_receipt_fingerprint(valuation_receipt)
        if (
            assessment.valuation_fingerprint != valuation_fingerprint
            or assessment.valuation_receipt_fingerprint != valuation_receipt_fingerprint
            or assessment.expectation_gap_fingerprint != gap_creation.expectation_gap_fingerprint
            or assessment.catalyst_fingerprint != gap_creation.catalyst_fingerprint
            or assessment.company != kwargs.get("company")
        ):
            raise ValueError("assessment does not bind to the supplied governed Mispricing inputs")

        preview = (builder or HistoricalComparisonMispricingAnalysisPreviewBuilder()).build(
            inputs, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
            gap_creation, valuation, valuation_receipt, cmp=cmp,
            mispricing_assumptions=mispricing_assumptions,
            mispricing_invalidation_conditions=mispricing_invalidation_conditions,
            **kwargs,
        )
        if (
            preview.analysis_fingerprint, preview.eligibility_fingerprint,
            preview.valuation_fingerprint, preview.valuation_receipt_fingerprint,
            preview.expectation_gap_fingerprint, preview.catalyst_fingerprint,
            preview.company, preview.potential_mispricing, preview.mispricing_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
        ) != (
            assessment.analysis_fingerprint, assessment.eligibility_fingerprint,
            assessment.valuation_fingerprint, assessment.valuation_receipt_fingerprint,
            assessment.expectation_gap_fingerprint, assessment.catalyst_fingerprint,
            assessment.company, assessment.potential_mispricing, assessment.mispricing_score,
            assessment.confidence, assessment.signal_ids, assessment.promoted_signal_ids,
        ):
            raise ValueError("assessment does not bind to the reconstructed Mispricing analysis")

        catalyst_keys = ("theme", "cluster_id", "catalyst_id", "trigger", "description", "economic_impact", "earnings_impact", "valuation_impact")
        _, catalyst = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(
            inputs, reviews, **{key: kwargs[key] for key in catalyst_keys}
        )
        gap_keys = ("gap_id", "company", "sector", "market_expectation", "eios_expectation", "market_earnings_expectation", "eios_earnings_expectation", "assumptions", "invalidation_conditions")
        gap = ExpectationGapEngine().analyze(catalyst=catalyst, **{key: kwargs[key] for key in gap_keys})
        if HistoricalComparisonExpectationGapCreationLedger.expectation_gap_fingerprint(gap) != preview.expectation_gap_fingerprint:
            raise ValueError("reconstructed Expectation Gap differs from its creation receipt")
        result = MispricingEngine().analyze(
            company=kwargs["company"], cmp=float(cmp), valuation=valuation,
            catalyst=catalyst, expectation_gap=gap,
            assumptions=list(mispricing_assumptions),
            invalidation_conditions=list(mispricing_invalidation_conditions),
        )
        fingerprint = self.mispricing_fingerprint(result)
        if any(item.mispricing_fingerprint == fingerprint for item in existing):
            raise ValueError("this Mispricing identity already has a creation receipt")
        receipt = HistoricalComparisonMispricingCreationReceipt(
            1, preview.analysis_fingerprint, assessment_fingerprint,
            preview.eligibility_fingerprint, preview.valuation_fingerprint,
            preview.valuation_receipt_fingerprint, preview.gap_id,
            preview.expectation_gap_fingerprint, preview.catalyst_id,
            preview.catalyst_fingerprint, preview.company, preview.cmp,
            fingerprint, preview.potential_mispricing, preview.mispricing_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
            creator, rationale, created_at,
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return result, receipt

    def read_all(self):
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("Mispricing creation path must be a file")
        result, assessments, identities = [], set(), set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid Mispricing creation receipt at line {number}: {exc}") from exc
                if item.assessment_fingerprint in assessments or item.mispricing_fingerprint in identities:
                    raise ValueError(f"Duplicate Mispricing creation receipt at line {number}")
                assessments.add(item.assessment_fingerprint)
                identities.add(item.mispricing_fingerprint)
                result.append(item)
        return tuple(result)

    @staticmethod
    def mispricing_fingerprint(result):
        if not isinstance(result, MispricingAssessment):
            raise ValueError("materializer did not return a MispricingAssessment")
        def clean(value):
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, dict):
                return {key: clean(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [clean(item) for item in value]
            return value
        payload = json.dumps(clean(asdict(result)), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(payload.encode()).hexdigest()

    @staticmethod
    def assessment_fingerprint(assessment):
        payload = {
            **assessment.__dict__, "disposition": assessment.disposition.value,
            "signal_ids": list(assessment.signal_ids),
            "promoted_signal_ids": list(assessment.promoted_signal_ids),
            "conditions": list(assessment.conditions),
            "monitoring_requirements": list(assessment.monitoring_requirements),
            "reviewed_at": assessment.reviewed_at.isoformat(),
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @classmethod
    def _parse(cls, value):
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError("unsupported Mispricing creation schema")
        potential = value["potential_mispricing"]
        if not isinstance(potential, bool) or not potential:
            raise ValueError("materialized Mispricing must identify potential mispricing")
        signals = cls._texts(value["signal_ids"], "signal_ids")
        promoted = cls._texts(value["promoted_signal_ids"], "promoted_signal_ids")
        if not signals or not promoted or not set(promoted).issubset(signals):
            raise ValueError("promoted Signal IDs must be a non-empty subset")
        return HistoricalComparisonMispricingCreationReceipt(
            1, cls._sha(value["analysis_fingerprint"]), cls._sha(value["assessment_fingerprint"]),
            cls._sha(value["eligibility_fingerprint"]), cls._sha(value["valuation_fingerprint"]),
            cls._sha(value["valuation_receipt_fingerprint"]), cls._text(value["gap_id"], "gap_id"),
            cls._sha(value["expectation_gap_fingerprint"]), cls._text(value["catalyst_id"], "catalyst_id"),
            cls._sha(value["catalyst_fingerprint"]), cls._text(value["company"], "company"),
            cls._positive(value["cmp"], "cmp"), cls._sha(value["mispricing_fingerprint"]), potential,
            cls._score(value["mispricing_score"], "mispricing_score"), cls._score(value["confidence"], "confidence"),
            signals, promoted, cls._text(value["creator"], "creator"), cls._text(value["rationale"], "rationale"),
            cls._iso(value["created_at"]),
        )

    @staticmethod
    def _payload(item):
        return {**item.__dict__, "signal_ids": list(item.signal_ids), "promoted_signal_ids": list(item.promoted_signal_ids), "created_at": item.created_at.isoformat()}
    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()
    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)):
            raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if len({value.casefold() for value in result}) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result
    @classmethod
    def _sha(cls, value):
        value = cls._text(value, "fingerprint")
        if len(value) != 64:
            raise ValueError("fingerprint must be SHA-256")
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()
    @staticmethod
    def _score(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"{name} must be on the 0-100 scale")
        return float(value)
    @staticmethod
    def _positive(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a positive finite number")
        return float(value)
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime):
            raise ValueError("created_at must be a datetime")
        return value
    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str):
            raise ValueError("created_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value))


__all__ = ["HistoricalComparisonMispricingCreationLedger"]
