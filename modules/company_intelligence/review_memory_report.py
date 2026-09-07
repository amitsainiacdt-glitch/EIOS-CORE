"""Read-only replay checks for review memory, not investment accuracy evaluation."""
from datetime import datetime
from pathlib import Path

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate


def build_review_memory_report(ledger_path: Path, *, evaluated_at: datetime):
    if evaluated_at.tzinfo is None or evaluated_at.utcoffset() is None:
        raise ValueError('evaluation requires a timezone-aware timestamp')
    ledger = CompanyFactHumanReviewLedger(ledger_path)
    reviews = ledger.read_all()
    eligible, future, undated = [], 0, 0
    for review in reviews:
        if review.reviewed_at.tzinfo is None or review.reviewed_at.utcoffset() is None:
            undated += 1
        elif review.reviewed_at > evaluated_at:
            future += 1
        else:
            eligible.append(review)
    usable = [review for review in eligible if review.candidate_snapshot is not None]
    # A replay tests retention of known feedback, NOT generalization to unseen facts.
    sample = sorted(usable, key=lambda review: review.reviewed_at)[-100:]
    counts = {decision: sum(review.decision.value == decision for review in eligible)
              for decision in ('APPROVE', 'HOLD', 'REJECT')}
    checks, issues = [], []
    engine = CompanyCandidateMetaReviewEngine()
    for review in sample:
        item = CompanyFactReviewCandidate(**review.candidate_snapshot)
        baseline = engine.assess(item, reviewed_at=evaluated_at)
        remembered = engine.assess(item, reviewed_at=evaluated_at, review_ledger_path=ledger_path)
        restrictive = any(previous.decision.value in {'HOLD', 'REJECT'}
                          for previous in ledger.previous_decisions(item)
                          if previous.reviewed_at.tzinfo is not None and previous.reviewed_at <= evaluated_at)
        retained = f'REVIEW_MEMORY_{review.decision.value}_SAME_SOURCE_FACT' in remembered.reason_codes
        safe = (remembered.requires_human_review and remembered.requires_mandatory_meta
                and not remembered.creates_evidence and not remembered.creates_catalyst
                and not remembered.changes_verdict)
        passed = retained and safe and (not restrictive or remembered.decision == 'HOLD_FOR_RESEARCH')
        if not passed:
            issues.append(review.review_id)
        checks.append({'review_id': review.review_id, 'baseline_decision': baseline.decision,
                       'memory_decision': remembered.decision, 'feedback_retained': retained,
                       'authority_preserved': safe, 'passed': passed})
    return {
        'schema_version': 1, 'evaluated_at': evaluated_at.isoformat(),
        'status': 'REPLAY_CHECK_FAILED' if issues else ('KNOWN_FEEDBACK_REPLAY_PASSED' if sample else 'AWAITING_REVIEW_FEEDBACK'),
        'recorded_reviews': len(reviews), 'eligible_reviews': len(eligible),
        'decisions': counts, 'usable_memory_records': len(usable),
        'legacy_records_without_snapshot': len(eligible) - len(usable),
        'excluded_future_reviews': future, 'excluded_timezone_unknown_reviews': undated,
        'replay_sample_limit': 100, 'replayed_records': len(sample),
        'passed_replays': sum(check['passed'] for check in checks), 'failed_review_ids': issues,
        'checks': checks,
        'unseen_fact_accuracy': None, 'investment_prediction_accuracy': None,
        'meaning': 'Replays check that known human feedback is remembered safely. They do not measure learning on new companies, extraction accuracy, or investment returns.',
        'changes_verdict': False,
    }
