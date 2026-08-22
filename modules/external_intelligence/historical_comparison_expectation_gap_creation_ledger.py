"""Explicit Expectation Gap materialization with append-only receipts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path

from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview_builder import HistoricalComparisonExpectationGapAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_expectation_gap_assessment_decision import HistoricalComparisonExpectationGapAssessmentDecision, HistoricalComparisonExpectationGapAssessmentDisposition
from modules.external_intelligence.historical_comparison_expectation_gap_creation_receipt import HistoricalComparisonExpectationGapCreationReceipt
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.opportunity.expectation_gap_engine import ExpectationGap, ExpectationGapEngine


class HistoricalComparisonExpectationGapCreationLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("Expectation Gap creation path must identify a file")

    def materialize(self, inputs, reviews, catalyst_assessment, catalyst_creation, assessment, *, creator, rationale, created_at, builder=None, **kwargs):
        if not isinstance(assessment, HistoricalComparisonExpectationGapAssessmentDecision):
            raise ValueError("assessment must be an Expectation Gap assessment")
        if assessment.disposition != HistoricalComparisonExpectationGapAssessmentDisposition.APPROVED:
            raise ValueError("only an Approved Expectation Gap assessment may be materialized")
        creator, rationale, created_at = self._text(creator, "creator"), self._text(rationale, "rationale"), self._datetime(created_at)
        try:
            if created_at < assessment.reviewed_at:
                raise ValueError("Expectation Gap creation timestamp precedes its human assessment")
        except TypeError as exc:
            raise ValueError("Expectation Gap timestamps use inconsistent timezone awareness") from exc
        existing = self.read_all()
        assessment_fingerprint = self.assessment_fingerprint(assessment)
        if any(item.gap_id == assessment.gap_id for item in existing):
            raise ValueError("gap_id already has a creation receipt")
        if any(item.assessment_fingerprint == assessment_fingerprint for item in existing):
            raise ValueError("this approved assessment was already materialized")
        preview = (builder or HistoricalComparisonExpectationGapAnalysisPreviewBuilder()).build(
            inputs, reviews, catalyst_assessment, catalyst_creation, **kwargs
        )
        if (
            preview.analysis_fingerprint, preview.eligibility_fingerprint, preview.catalyst_id,
            preview.catalyst_fingerprint, preview.gap_id, preview.material_gap,
            preview.positive_gap, preview.negative_gap, preview.gap_score, preview.confidence,
            preview.signal_ids, preview.promoted_signal_ids,
        ) != (
            assessment.analysis_fingerprint, assessment.eligibility_fingerprint, assessment.catalyst_id,
            assessment.catalyst_fingerprint, assessment.gap_id, assessment.material_gap,
            assessment.positive_gap, assessment.negative_gap, assessment.gap_score, assessment.confidence,
            assessment.signal_ids, assessment.promoted_signal_ids,
        ):
            raise ValueError("assessment does not bind to the reconstructed Expectation Gap analysis")
        catalyst_keys = ("theme", "cluster_id", "catalyst_id", "trigger", "description", "economic_impact", "earnings_impact", "valuation_impact")
        _, catalyst = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(
            inputs, reviews, **{key: kwargs[key] for key in catalyst_keys}
        )
        gap_keys = ("gap_id", "company", "sector", "market_expectation", "eios_expectation", "market_earnings_expectation", "eios_earnings_expectation", "assumptions", "invalidation_conditions")
        gap = ExpectationGapEngine().analyze(catalyst=catalyst, **{key: kwargs[key] for key in gap_keys})
        gap_fingerprint = self.expectation_gap_fingerprint(gap)
        receipt = HistoricalComparisonExpectationGapCreationReceipt(
            1, preview.analysis_fingerprint, assessment_fingerprint, preview.eligibility_fingerprint,
            preview.catalyst_id, preview.catalyst_fingerprint, preview.gap_id, gap_fingerprint,
            preview.material_gap, preview.positive_gap, preview.negative_gap, preview.gap_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids, creator, rationale, created_at,
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return gap, receipt

    def read_all(self):
        if not self.path.exists(): return ()
        result, gap_ids, assessments = [], set(), set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Expectation Gap creation receipt at line {number}: {exc}") from exc
                if item.gap_id in gap_ids or item.assessment_fingerprint in assessments: raise ValueError(f"Duplicate Expectation Gap creation receipt at line {number}")
                gap_ids.add(item.gap_id); assessments.add(item.assessment_fingerprint); result.append(item)
        return tuple(result)

    @staticmethod
    def expectation_gap_fingerprint(gap):
        if not isinstance(gap, ExpectationGap): raise ValueError("materializer did not return an ExpectationGap")
        def clean(value):
            if isinstance(value, Enum): return value.value
            if isinstance(value, dict): return {key: clean(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)): return [clean(item) for item in value]
            return value
        return hashlib.sha256(json.dumps(clean(asdict(gap)), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @staticmethod
    def assessment_fingerprint(assessment):
        payload = {**assessment.__dict__, "disposition": assessment.disposition.value, "signal_ids": list(assessment.signal_ids), "promoted_signal_ids": list(assessment.promoted_signal_ids), "conditions": list(assessment.conditions), "monitoring_requirements": list(assessment.monitoring_requirements), "reviewed_at": assessment.reviewed_at.isoformat()}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @classmethod
    def _parse(cls, value):
        if not isinstance(value, dict) or value.get("schema_version") != 1: raise ValueError("unsupported Expectation Gap creation schema")
        signals, promoted = cls._texts(value["signal_ids"], "signal_ids"), cls._texts(value["promoted_signal_ids"], "promoted_signal_ids")
        material, positive, negative = value["material_gap"], value["positive_gap"], value["negative_gap"]
        if not all(isinstance(item, bool) for item in (material, positive, negative)) or material != (positive or negative) or positive and negative: raise ValueError("invalid Expectation Gap direction")
        return HistoricalComparisonExpectationGapCreationReceipt(1, cls._sha(value["analysis_fingerprint"]), cls._sha(value["assessment_fingerprint"]), cls._sha(value["eligibility_fingerprint"]), cls._text(value["catalyst_id"], "catalyst_id"), cls._sha(value["catalyst_fingerprint"]), cls._text(value["gap_id"], "gap_id"), cls._sha(value["expectation_gap_fingerprint"]), material, positive, negative, cls._number(value["gap_score"]), cls._number(value["confidence"]), signals, promoted, cls._text(value["creator"], "creator"), cls._text(value["rationale"], "rationale"), cls._iso(value["created_at"]))

    @staticmethod
    def _payload(item): return {**item.__dict__, "signal_ids": list(item.signal_ids), "promoted_signal_ids": list(item.promoted_signal_ids), "created_at": item.created_at.isoformat()}
    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if len(set(result)) != len(result): raise ValueError(f"{name} must not contain duplicates")
        return result
    @classmethod
    def _sha(cls, value):
        value = cls._text(value, "fingerprint")
        if len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()
    @staticmethod
    def _number(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100: raise ValueError("score must be on the 0-100 scale")
        return float(value)
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("created_at must be a datetime")
        return value
    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str): raise ValueError("created_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value))


__all__ = ["HistoricalComparisonExpectationGapCreationLedger"]
