"""Build governed, page-aware company fact candidates for META review."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.public_factual_candidate_extractor import PublicFactualCandidateExtractor


@dataclass(frozen=True)
class CompanyFactReviewCandidate:
    schema_version: int
    candidate_id: str
    company: str
    event_type: str
    statement_posture: str
    source_passage: str
    explicit_amounts: tuple[str, ...]
    explicit_dates: tuple[str, ...]
    pdf_page: int | None
    source_url: str
    document_hash: str
    extraction_id: str
    extraction_method: str
    review_status: str = "PENDING_META_REVIEW"
    creates_evidence: bool = False


class CompanyFactReviewQueueBuilder:
    PAGE_MARKER = re.compile(r"\[\[PDF_PAGE_(\d+)\]\]")

    def __init__(self, output_path: Path):
        self.output_path = Path(output_path)

    def build(self, *, acquisition, extraction, admission, company: str, generated_at: datetime) -> tuple[CompanyFactReviewCandidate, ...]:
        preview = PublicFactualCandidateExtractor().extract(
            acquisition=acquisition, extraction=extraction,
            admission=admission, subject_entity=company,
        )
        text = extraction.extracted_text or ""
        candidates = tuple(
            CompanyFactReviewCandidate(
                1, item.candidate_id, company, item.event_type,
                item.statement_posture, self._clean_passage(item.source_passage),
                item.explicit_amounts, item.explicit_dates,
                self._page_at(text, item.passage_start), item.source_url,
                item.document_hash, item.extraction_id, item.extraction_method,
            )
            for item in preview.candidates
        )
        payload = {
            "schema_version": 1,
            "company": company,
            "generated_at": generated_at.isoformat(),
            "acquisition_id": preview.acquisition_id,
            "extraction_id": preview.extraction_id,
            "candidate_count": len(candidates),
            "candidates": [self._payload(item) for item in candidates],
            "warnings": list(preview.warnings),
            "creates_evidence": False,
            "requires_meta_review": True,
            "requires_human_review": True,
        }
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.output_path.with_suffix(self.output_path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.output_path)
        return candidates

    @classmethod
    def _page_at(cls, text: str, position: int) -> int | None:
        matches = tuple(match for match in cls.PAGE_MARKER.finditer(text) if match.start() <= max(0, position))
        return int(matches[-1].group(1)) if matches else None

    @classmethod
    def _clean_passage(cls, passage: str) -> str:
        return cls.PAGE_MARKER.sub("", passage).strip()

    @staticmethod
    def _payload(item):
        payload = asdict(item)
        payload["explicit_amounts"] = list(item.explicit_amounts)
        payload["explicit_dates"] = list(item.explicit_dates)
        return payload


__all__ = ["CompanyFactReviewCandidate", "CompanyFactReviewQueueBuilder"]
