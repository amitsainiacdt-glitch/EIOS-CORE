"""Governed contract for EIOS analysis of a company's annual-report history."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class StudyStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PARTIAL = "PARTIAL"
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"


@dataclass(frozen=True)
class StudyFinding:
    finding_id: str
    category: str
    headline: str
    interpretation: str
    fact_ids: tuple[str, ...]
    confidence_percent: int
    status: str = "PRELIMINARY"

    def __post_init__(self) -> None:
        if not self.fact_ids:
            raise ValueError("every study finding must cite at least one extracted fact")
        if not 0 <= self.confidence_percent <= 100:
            raise ValueError("confidence_percent must be between 0 and 100")


@dataclass(frozen=True)
class AnnualReportStudy:
    schema_version: int
    company: str
    ticker: str
    requested_years: int
    available_years: int
    extracted_years: int
    reviewed_years: int
    status: StudyStatus
    findings: tuple[StudyFinding, ...]
    missing_work: tuple[str, ...]
    meta_status: str
    meta_permitted_conclusion: str
    verdict_status: str = "RESEARCH_HOLD"
    creates_recommendation: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("unsupported schema version")
        if not 0 <= self.reviewed_years <= self.extracted_years <= self.available_years <= self.requested_years:
            raise ValueError("annual-report coverage counts are inconsistent")
        if self.status == StudyStatus.READY_FOR_HUMAN_REVIEW and self.extracted_years != self.requested_years:
            raise ValueError("a complete study requires every requested year to be extracted")
        if self.creates_recommendation:
            raise ValueError("annual-report study cannot create a recommendation")

    @property
    def extraction_coverage_percent(self) -> int:
        return round(self.extracted_years / self.requested_years * 100) if self.requested_years else 0

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["extraction_coverage_percent"] = self.extraction_coverage_percent
        for finding in payload["findings"]:
            finding["fact_ids"] = list(finding["fact_ids"])
        payload["missing_work"] = list(payload["missing_work"])
        return payload


__all__ = ["AnnualReportStudy", "StudyFinding", "StudyStatus"]
