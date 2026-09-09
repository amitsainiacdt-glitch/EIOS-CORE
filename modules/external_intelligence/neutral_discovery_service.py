"""Builds a neutral research queue whose ordering cannot use familiarity context."""

import hashlib
import json
import re

from modules.external_intelligence.neutral_discovery import (
    NeutralDiscoveryCandidate, NeutralDiscoveryFactor, NeutralDiscoveryFactorKind,
    NeutralDiscoveryResult, NeutralDiscoveryUniverse,
)


class NeutralDiscoveryService:
    NON_AUTHORITY = "Neutral research-priority queue only; not an Opportunity, recommendation, position, or trade instruction."

    def select(self, universe):
        if not isinstance(universe, NeutralDiscoveryUniverse):
            raise ValueError("universe must be NeutralDiscoveryUniverse")
        if universe.schema_version != 1:
            raise ValueError("unsupported neutral-discovery schema")
        universe_id = self._text(universe.universe_id, "universe_id")
        sectors = self._unique_texts(universe.target_sector_ids, "target_sector_ids")
        if isinstance(universe.selection_limit, bool) or not isinstance(universe.selection_limit, int) or universe.selection_limit <= 0:
            raise ValueError("selection_limit must be a positive integer")
        if not universe.public_information_only:
            raise ValueError("neutral discovery accepts public information only")
        if universe.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("neutral discovery requires the canonical non-authority statement")
        if not isinstance(universe.candidates, tuple) or not universe.candidates:
            raise ValueError("candidates must be a non-empty tuple")

        normalized_sectors = {item.casefold(): item for item in sectors}
        seen, rows, anchors = set(), [], []
        for candidate in universe.candidates:
            if not isinstance(candidate, NeutralDiscoveryCandidate):
                raise ValueError("candidates must contain NeutralDiscoveryCandidate values")
            ticker = self._text(candidate.ticker, "ticker").upper()
            if ticker in seen:
                raise ValueError("candidate tickers must be unique")
            seen.add(ticker)
            company = self._text(candidate.company, "company")
            sector = self._text(candidate.sector_id, "sector_id")
            if sector.casefold() not in normalized_sectors:
                raise ValueError("candidate sector is outside the declared universe")
            fingerprint = self._sha(candidate.evidence_fingerprint)
            if not isinstance(candidate.factors, tuple) or not candidate.factors:
                raise ValueError("candidate requires objective discovery factors")
            kinds, priority, factor_rows = set(), 0, []
            for factor in candidate.factors:
                if not isinstance(factor, NeutralDiscoveryFactor) or not isinstance(factor.kind, NeutralDiscoveryFactorKind):
                    raise ValueError("discovery factor is invalid")
                if factor.kind in kinds:
                    raise ValueError("discovery factor kinds must be unique per candidate")
                kinds.add(factor.kind)
                if isinstance(factor.priority_points, bool) or not isinstance(factor.priority_points, int) or not 0 <= factor.priority_points <= 100:
                    raise ValueError("factor priority_points must be an integer from zero to 100")
                rationale = self._text(factor.rationale, "factor rationale")
                priority += factor.priority_points
                factor_rows.append((factor.kind.value, factor.priority_points, rationale))
            rows.append((ticker, company, normalized_sectors[sector.casefold()], fingerprint, priority, tuple(sorted(factor_rows))))
            if candidate.is_current_holding or candidate.is_watchlisted or candidate.was_previously_discussed:
                anchors.append(ticker)

        covered = tuple(sorted({row[2] for row in rows}))
        missing = tuple(sorted(set(sectors) - set(covered)))
        ranked = sorted(rows, key=lambda row: (-row[4], row[0]))
        selected = tuple(row[0] for row in ranked[:universe.selection_limit])
        payload = {"universe_id": universe_id, "target_sectors": sorted(sectors),
                   "candidates": [(row[0], row[2], row[3], row[4], row[5]) for row in sorted(rows)],
                   "selection_limit": universe.selection_limit, "selected": selected}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        reasons = ("DECLARED_SECTOR_UNIVERSE_INCOMPLETE",) if missing else ()
        return NeutralDiscoveryResult(
            universe_id, selected, tuple((row[0], row[4]) for row in ranked), covered, missing, digest,
            "HOLD_INCOMPLETE_UNIVERSE" if missing else "NEUTRAL_QUEUE_READY", reasons,
            tuple(sorted(anchors)), False, self.NON_AUTHORITY)

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _unique_texts(cls, values, name):
        if not isinstance(values, tuple) or not values:
            raise ValueError(f"{name} must be a non-empty tuple")
        result = tuple(cls._text(value, name) for value in values)
        if len({value.casefold() for value in result}) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result

    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", value):
            raise ValueError("evidence_fingerprint must be SHA-256")
        return value.casefold()


__all__ = ["NeutralDiscoveryService"]
