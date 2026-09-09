"""Map one fully approved quarterly statement into a controlled quantitative Fact."""

from modules.intelligence_write import (
    ActorOrigin, ActorType, AuthorityScope, InformationClass, OriginType,
    SourceReference, ValidationStatus, WriteCommand, WriteOperation,
)


class GovernedQuarterlyControlledWriteAdapter:
    VERSION = "governed-quarterly-controlled-write-adapter-v1"

    def build_command(self, *, candidate, fact, source, figures, record_id, created_at):
        period_end = source["period_end"]
        basis = source["basis"]
        return WriteCommand(
            schema_version=1,
            command_id=f"controlled-quarterly:{record_id}",
            idempotency_key=f"governed-quarterly:{record_id}",
            operation=WriteOperation.PROPOSE_FACT,
            actor=ActorOrigin(
                actor_id=fact.human_review_id,
                actor_type=ActorType.HUMAN,
                actor_version="company-fact-human-review-v1",
                origin_id=fact.human_review_id,
                origin_type=OriginType.HUMAN_REVIEW,
                authority_scopes=(AuthorityScope.PROPOSE_FACT, AuthorityScope.VERIFY_FACT),
            ),
            requested_at=created_at,
            company_id=source["ticker"],
            entity=fact.company,
            information_class=InformationClass.FACT,
            semantic_key=f"quarterly-income-statement-core|{period_end}|{basis}",
            payload={
                "metric": "QUARTERLY_INCOME_STATEMENT_CORE",
                "value": dict(figures),
                "unit": "INR_CRORE",
                "period": period_end,
                "period_start": source["period_start"],
                "quarter": source["quarter"],
                "basis": basis,
                "candidate_id": candidate.candidate_id,
                "governed_fact_id": fact.fact_id,
                "human_review_id": fact.human_review_id,
            },
            source_references=(SourceReference(
                source_id=fact.fact_id,
                source_type="GOVERNED_QUARTERLY_FINANCIAL_RESULT",
                source_url=fact.source_url,
                document_hash=fact.document_hash,
                page_or_section=f"PDF page {source['pdf_page']}",
            ),),
            confidence=fact.approved_confidence,
            requested_validation_status=ValidationStatus.VERIFIED,
            correlation_id=record_id,
            causation_id=fact.fact_id,
        )


__all__ = ["GovernedQuarterlyControlledWriteAdapter"]
