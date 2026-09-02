"""First governed consumers for company-event, contradiction and monitoring work."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.engine_analysis_intake import EngineAnalysisWorkItem
from modules.company_intelligence.governed_company_fact import GovernedCompanyFact


SUPPORTED_QUEUES = {"COMPANY_EVENT_ANALYSIS", "CONTRADICTION_SEARCH", "CONTINUOUS_MONITORING"}


@dataclass(frozen=True)
class InitialEngineAnalysisResult:
    schema_version: int
    result_id: str
    work_item_id: str
    fact_id: str
    company: str
    analysis_queue: str
    result_status: str
    confirmed_findings: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    monitoring_terms: tuple[str, ...]
    source_url: str
    completed_at: datetime
    creates_evidence: bool = False
    creates_catalyst: bool = False
    changes_verdict: bool = False


class InitialEngineAnalysisRepository:
    def __init__(self, path: Path):
        self.path = Path(path)

    def consume(self, fact: GovernedCompanyFact, work: EngineAnalysisWorkItem, *, completed_at: datetime) -> InitialEngineAnalysisResult:
        if work.fact_id != fact.fact_id:
            raise ValueError("engine work item does not bind to governed fact")
        if work.analysis_queue not in SUPPORTED_QUEUES:
            raise ValueError("analysis queue is not supported by the initial consumers")
        if any(item.work_item_id == work.work_item_id for item in self.read_all()):
            raise ValueError("engine work item is already consumed")
        status, findings, questions, terms = self._analyze(fact, work.analysis_queue)
        result = InitialEngineAnalysisResult(
            1, sha256(f"{work.work_item_id}\nINITIAL_ENGINE_RESULT_V1".encode()).hexdigest(),
            work.work_item_id, fact.fact_id, fact.company, work.analysis_queue,
            status, findings, questions, terms, fact.source_url, completed_at,
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(result); payload["completed_at"] = completed_at.isoformat()
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return result

    def consume_available(self, fact: GovernedCompanyFact, work_items, *, completed_at: datetime) -> tuple[InitialEngineAnalysisResult, ...]:
        existing = {item.work_item_id for item in self.read_all()}
        return tuple(
            self.consume(fact, work, completed_at=completed_at)
            for work in work_items
            if work.analysis_queue in SUPPORTED_QUEUES and work.work_item_id not in existing
        )

    def read_all(self) -> tuple[InitialEngineAnalysisResult, ...]:
        if not self.path.is_file():
            return ()
        results, ids, work_ids = [], set(), set()
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
                for key in ("confirmed_findings", "unresolved_questions", "monitoring_terms"):
                    payload[key] = tuple(payload[key])
                payload["completed_at"] = datetime.fromisoformat(payload["completed_at"])
                item = InitialEngineAnalysisResult(**payload)
                if item.schema_version != 1 or item.result_id in ids or item.work_item_id in work_ids:
                    raise ValueError("invalid or duplicate initial engine result")
                if item.creates_evidence or item.creates_catalyst or item.changes_verdict:
                    raise ValueError("initial engine result exceeded its authority")
                ids.add(item.result_id); work_ids.add(item.work_item_id); results.append(item)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid initial engine result at line {number}: {exc}") from exc
        return tuple(results)

    @staticmethod
    def _analyze(fact, queue):
        event = fact.event_type.replace("_", " ").lower()
        if queue == "COMPANY_EVENT_ANALYSIS":
            findings = (
                f"A human-approved primary-source passage records a {event} event for {fact.company}.",
                f"Statement posture is {fact.statement_posture.lower()} and approved source confidence is {fact.approved_confidence:g} percent.",
            )
            questions = ("What revenue, margin, cash-flow and timing impact follows?", "Was this event already expected by the market?")
            return "FACTUAL_EVENT_CONFIRMED_IMPACT_UNPROVEN", findings, questions, ()
        if queue == "CONTRADICTION_SEARCH":
            questions = (
                f"Do later filings contradict, delay, cancel or revise this {event}?",
                "Do exchange disclosures, regulators, customers or suppliers independently corroborate the event?",
                "Is management language more uncertain than the extracted passage suggests?",
            )
            return "CONTRADICTION_RESEARCH_REQUIRED", (), questions, InitialEngineAnalysisRepository._terms(fact)
        questions = ("Has the event changed, completed, been delayed or been cancelled?", "Has earnings transmission become measurable?")
        return "MONITORING_ACTIVE", (), questions, InitialEngineAnalysisRepository._terms(fact)

    @staticmethod
    def _terms(fact):
        values = [fact.company, fact.event_type.replace("_", " ").lower(), *fact.explicit_dates, *fact.explicit_amounts]
        return tuple(dict.fromkeys(value.strip() for value in values if value and value.strip()))


__all__ = ["InitialEngineAnalysisRepository", "InitialEngineAnalysisResult", "SUPPORTED_QUEUES"]
