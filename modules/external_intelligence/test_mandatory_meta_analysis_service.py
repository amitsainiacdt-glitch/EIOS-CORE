"""Offline end-to-end tests for the governed mandatory Meta service."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.mandatory_meta_analysis import MetaAnalysisConclusion, MetaContradictionBurden, MetaKillTestResult, MetaKillTestStatus
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaAnalysisGate
from modules.external_intelligence.mandatory_meta_analysis_service import MandatoryMetaAnalysisService
from modules.external_intelligence.mandatory_meta_analysis_repository import MandatoryMetaAnalysisRepository
from modules.external_intelligence.mandatory_meta_analysis_repository import StoredMandatoryMetaAnalysis
from modules.external_intelligence.mandatory_meta_review_ledger import MandatoryMetaReviewLedger
from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry
from modules.external_intelligence.temporal_leading_indicator_preview import IndicatorEvidenceRelationship, TemporalIndicatorEvidenceLink
from modules.external_intelligence.temporal_leading_indicator_service import TemporalLeadingIndicatorService
from modules.external_intelligence.pre_inflection_assessment_service import PreInflectionAssessmentService
from modules.external_intelligence.pre_inflection_repository import PreInflectionRepository, StoredPreInflectionAssessment
from modules.external_intelligence.pre_inflection_review_ledger import PreInflectionReviewLedger
from modules.external_intelligence.price_recognition import PublicMarketRecognitionSnapshot
from modules.external_intelligence.price_recognition_service import PriceRecognitionService
from modules.external_intelligence.price_recognition_repository import PriceRecognitionRepository, StoredPriceRecognition
from modules.external_intelligence.price_recognition_review_ledger import PriceRecognitionReviewLedger
from modules.external_intelligence.eip_classification_service import EIPClassificationService
from modules.external_intelligence.eip_repository import EIPRepository
from modules.external_intelligence.eip_review_ledger import EIPReviewLedger
from modules.external_intelligence.eip_evidence_review_candidate_service import EIPEvidenceReviewCandidateService


def main():
    now = datetime(2026, 8, 30, 0, tzinfo=timezone.utc)
    records = tuple(
        PublicTemporalEvidenceRecord(1, f"TE-{i}", f"{i:064x}", "Alpha Limited", event, "ASSERTED", now + timedelta(days=days), now + timedelta(days=days), "PUBLISHED_AT", "https://public.example/a", f"{i+10:064x}", f"C-{i}", f"P-{i}", f"R-{i}", f"Fact {i}", f"Exact passage {i}")
        for i, event, days in ((1, "TENDER", 0), (2, "ORDER_CONTRACT", 180))
    )
    registry = SectorCausalIndicatorRegistry.initial_library()
    preview = TemporalLeadingIndicatorService(registry).preview(
        entity="Alpha Limited", sector_id="INDUSTRIALS", indicator_id="INDUSTRIAL_ORDER_CONVERSION", temporal_evidence=records,
        links=(
            TemporalIndicatorEvidenceLink("TE-1", "INDUSTRIAL_ORDER_CONVERSION", "TENDER_AUTHORITY", IndicatorEvidenceRelationship.SUPPORTS, "Independent tender authority."),
            TemporalIndicatorEvidenceLink("TE-2", "INDUSTRIAL_ORDER_CONVERSION", "NSE_FILING", IndicatorEvidenceRelationship.SUPPORTS, "Company exchange filing."),
        ),
    )
    kill_tests = tuple(
        MetaKillTestResult("INDUSTRIAL_ORDER_CONVERSION", test, MetaKillTestStatus.NOT_TRIGGERED, ("TE-1", "TE-2"), "No public trigger found.")
        for test in registry.get("INDUSTRIAL_ORDER_CONVERSION").kill_tests
    )
    service = MandatoryMetaAnalysisService(MandatoryMetaAnalysisGate(registry), clock=lambda: now + timedelta(days=181))
    arguments = dict(
        assessment_id="META-RUN-1", temporal_evidence=records, indicator_previews=(preview,), entity_scope=("Alpha Limited",),
        sector_scope=("INDUSTRIALS",), causal_hypotheses=("Tender award may be converting into executable company backlog.",),
        contradictions=(), missing_expected_evidence=("Execution and revenue recognition are not yet confirmed.",), coverage_gaps=(),
        syndication_findings=("The tender and exchange filing have distinct originating documents.",),
        cross_scope_transmissions=("Government tender authority evidence precedes the company order filing.",),
        research_gaps=("Track execution milestones and customer funding.",), kill_test_results=kill_tests,
        conclusion=MetaAnalysisConclusion.EMERGING, contradiction_burden=MetaContradictionBurden.LOW,
        uncertainty_statement="Execution timing and margin conversion remain uncertain.", assessor="Mandatory Meta Service",
    )
    ready = service.assess(**arguments)
    assert ready.gate_result.decision.value == "READY_FOR_PRE_INFLECTION"
    assert ready.assessment.input_indicator_preview_fingerprints == (preview.preview_fingerprint,)
    assert ready.assessment.non_authority_statement == service.NON_AUTHORITY

    triggered = replace(kill_tests[0], status=MetaKillTestStatus.TRIGGERED, rationale="Public cancellation disclosed.")
    held = service.assess(**{**arguments, "assessment_id": "META-RUN-2", "kill_test_results": (triggered,) + kill_tests[1:]})
    assert held.gate_result.decision.value == "HOLD_FOR_RESEARCH" and "KILL_TEST_TRIGGERED" in held.gate_result.reason_codes

    missing_kill = service.assess(**{**arguments, "assessment_id": "META-RUN-3", "kill_test_results": kill_tests[:-1]})
    assert missing_kill.gate_result.decision.value == "BLOCKED" and "KILL_TEST_COVERAGE_MISMATCH" in missing_kill.gate_result.reason_codes
    with TemporaryDirectory() as directory:
        root = Path(directory)
        repository = MandatoryMetaAnalysisRepository(root / "meta.jsonl")
        stored = repository.add(ready.assessment)
        assert repository.all() == (stored,)
        reviews = MandatoryMetaReviewLedger(root / "reviews.jsonl", service.gate)
        authorized = reviews.record(
            stored, temporal_evidence=records, indicator_previews=(preview,), review_id="META-REV-1",
            decision="AUTHORIZE_PRE_INFLECTION_REVIEW", notes="Evidence may proceed to governed Pre-Inflection review only.",
            reviewed_at=now + timedelta(days=182), reviewer="Human Meta Reviewer",
        )
        assert authorized.gate_decision == "READY_FOR_PRE_INFLECTION" and reviews.all() == (authorized,)
        pre_inflection = PreInflectionAssessmentService(service.gate).preview(
            preview_id="PRE-1", stored_meta=stored, meta_review=authorized,
            temporal_evidence=records, indicator_previews=(preview,),
            what_is_changing="Independent tender and company-order evidence is persisting across the expected observation window.",
            why_now="The tender precedes the exchange-filed order and the configured persistence threshold has now been met.",
            confirmation_requirements=("Execution milestones", "Revenue recognition", "Customer funding confirmation"),
            invalidation_conditions=("Order cancellation", "Material execution delay", "Counterparty insolvency"),
            balance_sheet_governance_risks=("Working-capital funding capacity", "Execution governance", "Customer concentration"),
        )
        assert pre_inflection.strength.value == "EMERGING"
        assert pre_inflection.market_recognition_status == "NOT_ASSESSED"
        assert pre_inflection.eligible_for_human_pre_inflection_review
        assert pre_inflection.expected_lead_time_quarters == (1, 4)
        pre_repository = PreInflectionRepository(root / "pre-inflection.jsonl")
        stored_pre = pre_repository.add(pre_inflection)
        assert pre_repository.all() == (stored_pre,)
        pre_reviews = PreInflectionReviewLedger(root / "pre-inflection-reviews.jsonl", PreInflectionAssessmentService(service.gate))
        pre_authorized = pre_reviews.record(
            stored_pre, stored_meta=stored, meta_review=authorized, temporal_evidence=records,
            indicator_previews=(preview,), review_id="PRE-REV-1", decision="AUTHORIZE_PRICE_RECOGNITION_REVIEW",
            notes="Authorize only the governed Price Recognition review.", reviewed_at=now + timedelta(days=184),
            reviewer="Human Pre-Inflection Reviewer",
        )
        assert pre_authorized.preview_fingerprint == stored_pre.preview_fingerprint
        assert pre_reviews.all() == (pre_authorized,)
        market = PublicMarketRecognitionSnapshot(
            1, "MKT-1", "Alpha Limited", now + timedelta(days=185), True, ("PUBLIC_MARKET_DATA",),
            100.0, 105.0, 2.0, 5.0, 8.0, 10.0, 2.0, 80.0, 140.0, 1.1, 3.0, 0.1, 10.0,
        )
        recognition = PriceRecognitionService().preview(
            stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            pre_inflection_review=pre_authorized, market_snapshot=market,
        )
        assert recognition.state.value == "UNRECOGNIZED" and recognition.eligible_for_eip_review
        recognition_repository = PriceRecognitionRepository(root / "recognition.jsonl")
        stored_recognition = recognition_repository.add(recognition)
        assert recognition_repository.all() == (stored_recognition,)
        recognition_reviews = PriceRecognitionReviewLedger(root / "recognition-reviews.jsonl", PriceRecognitionService())
        eip_authorized = recognition_reviews.record(
            stored_recognition, stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            pre_inflection_review=pre_authorized, market_snapshot=market, review_id="PRICE-REV-1",
            decision="AUTHORIZE_EIP_REVIEW", notes="Market recognition remains low enough for governed EIP review.",
            reviewed_at=now + timedelta(days=186), reviewer="Human Price Recognition Reviewer",
        )
        assert eip_authorized.recognition_state == "UNRECOGNIZED" and recognition_reviews.all() == (eip_authorized,)
        stage_two = EIPClassificationService().classify(
            classification_id="EIP-1", stored_pre_inflection=stored_pre,
            current_pre_inflection=pre_inflection, stored_recognition=stored_recognition,
            current_recognition=recognition, recognition_review=eip_authorized,
            risk_disposition="CONTAINED", risk_rationale="Working-capital and governance risks are identified but not yet fully cleared.",
            valuation_room="SUFFICIENT", valuation_rationale="Public valuation evidence indicates remaining room subject to confirmation.",
        )
        assert stage_two.stage.value == "STAGE_2_PRE_INFLECTION" and stage_two.eligible_for_human_eip_review
        fully = PriceRecognitionService().preview(
            stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            pre_inflection_review=pre_authorized,
            market_snapshot=replace(
                market, snapshot_id="MKT-2", current_price=150.0, sector_relative_return_pct=25.0,
                abnormal_volume_ratio=2.0, valuation_rerating_pct=30.0,
                analyst_revision_breadth=0.8, media_attention_change_pct=100.0,
            ),
        )
        assert fully.state.value == "FULLY_RECOGNIZED_POTENTIALLY_LATE" and not fully.eligible_for_eip_review
        fully_stored = PriceRecognitionRepository(root / "fully-recognition.jsonl").add(fully)
        fully_market = replace(
            market, snapshot_id="MKT-2", current_price=150.0, sector_relative_return_pct=25.0,
            abnormal_volume_ratio=2.0, valuation_rerating_pct=30.0,
            analyst_revision_breadth=0.8, media_attention_change_pct=100.0,
        )
        try:
            PriceRecognitionReviewLedger(root / "fully-review.jsonl", PriceRecognitionService()).record(
                fully_stored, stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
                pre_inflection_review=pre_authorized, market_snapshot=fully_market,
                review_id="PRICE-REV-LATE", decision="AUTHORIZE_EIP_REVIEW", notes="Attempted late authorization.", reviewed_at=now, reviewer="Reviewer",
            )
        except ValueError as exc:
            assert "not eligible" in str(exc)
        else:
            raise AssertionError("fully recognized case authorized for EIP")
        fully_rejected = PriceRecognitionReviewLedger(root / "fully-rejected.jsonl", PriceRecognitionService()).record(
            fully_stored, stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            pre_inflection_review=pre_authorized, market_snapshot=fully_market, review_id="PRICE-REV-REJECT-LATE",
            decision="REJECT_RECOGNITION_ASSESSMENT", notes="Broad recognition makes the case potentially late.",
            reviewed_at=now + timedelta(days=186), reviewer="Human Price Recognition Reviewer",
        )
        stage_five = EIPClassificationService().classify(
            classification_id="EIP-5", stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            stored_recognition=fully_stored, current_recognition=fully, recognition_review=fully_rejected,
            risk_disposition="CONTAINED", risk_rationale="Risks documented.", valuation_room="INSUFFICIENT",
            valuation_rationale="Broad recognition and rerating have reduced remaining valuation room.",
        )
        assert stage_five.stage.value == "STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE"
        assert not stage_five.eligible_for_human_eip_review
        insufficient = PriceRecognitionService().preview(
            stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            pre_inflection_review=pre_authorized,
            market_snapshot=replace(
                market, snapshot_id="MKT-3", sector_relative_return_pct=None, week_52_low=None,
                week_52_high=None, abnormal_volume_ratio=None, valuation_rerating_pct=None,
                analyst_revision_breadth=None, media_attention_change_pct=None,
            ),
        )
        assert insufficient.state.value == "INSUFFICIENT_DATA" and not insufficient.eligible_for_eip_review
        try:
            PriceRecognitionReviewLedger(root / "forged-price-review.jsonl", PriceRecognitionService()).record(
                StoredPriceRecognition("0" * 64, recognition), stored_pre_inflection=stored_pre,
                current_pre_inflection=pre_inflection, pre_inflection_review=pre_authorized,
                market_snapshot=market, review_id="PRICE-FORGED", decision="REJECT_RECOGNITION_ASSESSMENT",
                notes="Forged test.", reviewed_at=now, reviewer="Reviewer",
            )
        except ValueError as exc:
            assert "fingerprint mismatch" in str(exc)
        else:
            raise AssertionError("forged Price Recognition accepted")
        try:
            PreInflectionReviewLedger(root / "forged-pre-reviews.jsonl", PreInflectionAssessmentService(service.gate)).record(
                StoredPreInflectionAssessment("0" * 64, pre_inflection), stored_meta=stored, meta_review=authorized,
                temporal_evidence=records, indicator_previews=(preview,), review_id="PRE-FORGED",
                decision="REJECT_ASSESSMENT", notes="Forged test.", reviewed_at=now, reviewer="Reviewer",
            )
        except ValueError as exc:
            assert "fingerprint mismatch" in str(exc)
        else:
            raise AssertionError("forged Pre-Inflection record accepted")
        coherent_assessment = replace(
            ready.assessment, assessment_id="META-COHERENT", conclusion=MetaAnalysisConclusion.COHERENT,
            contradiction_burden=MetaContradictionBurden.NONE, missing_expected_evidence=(), coverage_gaps=(), research_gaps=(),
        )
        coherent_stored = MandatoryMetaAnalysisRepository(root / "coherent-meta.jsonl").add(coherent_assessment)
        coherent_review = MandatoryMetaReviewLedger(root / "coherent-review.jsonl", service.gate).record(
            coherent_stored, temporal_evidence=records, indicator_previews=(preview,), review_id="META-REV-COHERENT",
            decision="AUTHORIZE_PRE_INFLECTION_REVIEW", notes="Coherent evidence authorized for research-stage review.",
            reviewed_at=now + timedelta(days=183), reviewer="Human Meta Reviewer",
        )
        strong = PreInflectionAssessmentService(service.gate).preview(
            preview_id="PRE-STRONG", stored_meta=coherent_stored, meta_review=coherent_review,
            temporal_evidence=records, indicator_previews=(preview,), what_is_changing="Order conversion is independently confirmed.",
            why_now="Persistence and independent confirmation requirements are met.",
            confirmation_requirements=("Execution milestone",), invalidation_conditions=("Cancellation",),
            balance_sheet_governance_risks=("Working capital",),
        )
        assert strong.strength.value == "STRONG"
        strong_repository = PreInflectionRepository(root / "strong-pre.jsonl")
        stored_strong = strong_repository.add(strong)
        strong_pre_review = PreInflectionReviewLedger(root / "strong-pre-review.jsonl", PreInflectionAssessmentService(service.gate)).record(
            stored_strong, stored_meta=coherent_stored, meta_review=coherent_review,
            temporal_evidence=records, indicator_previews=(preview,), review_id="PRE-REV-STRONG",
            decision="AUTHORIZE_PRICE_RECOGNITION_REVIEW", notes="Strong case authorized for recognition review.",
            reviewed_at=now + timedelta(days=184), reviewer="Human Pre-Inflection Reviewer",
        )
        strong_recognition = PriceRecognitionService().preview(
            stored_pre_inflection=stored_strong, current_pre_inflection=strong,
            pre_inflection_review=strong_pre_review, market_snapshot=market,
        )
        stored_strong_recognition = PriceRecognitionRepository(root / "strong-recognition.jsonl").add(strong_recognition)
        strong_price_review = PriceRecognitionReviewLedger(root / "strong-price-review.jsonl", PriceRecognitionService()).record(
            stored_strong_recognition, stored_pre_inflection=stored_strong, current_pre_inflection=strong,
            pre_inflection_review=strong_pre_review, market_snapshot=market, review_id="PRICE-REV-STRONG",
            decision="AUTHORIZE_EIP_REVIEW", notes="Recognition remains low.", reviewed_at=now + timedelta(days=186),
            reviewer="Human Price Recognition Reviewer",
        )
        stage_three = EIPClassificationService().classify(
            classification_id="EIP-3", stored_pre_inflection=stored_strong,
            current_pre_inflection=strong, stored_recognition=stored_strong_recognition,
            current_recognition=strong_recognition, recognition_review=strong_price_review,
            risk_disposition="CLEAR", risk_rationale="No unresolved balance-sheet or governance kill condition remains.",
            valuation_room="SUFFICIENT", valuation_rationale="Recognition and valuation evidence indicate sufficient remaining room.",
        )
        assert stage_three.stage.value == "STAGE_3_EARLIEST_INVESTABLE_POINT"
        assert stage_three.eligible_for_human_eip_review
        partial_market = replace(market, snapshot_id="MKT-PARTIAL", current_price=125.0, sector_relative_return_pct=12.0)
        partial_recognition = PriceRecognitionService().preview(
            stored_pre_inflection=stored_strong, current_pre_inflection=strong,
            pre_inflection_review=strong_pre_review, market_snapshot=partial_market,
        )
        assert partial_recognition.state.value == "PARTIALLY_RECOGNIZED"
        stored_partial = PriceRecognitionRepository(root / "partial-recognition.jsonl").add(partial_recognition)
        partial_review = PriceRecognitionReviewLedger(root / "partial-price-review.jsonl", PriceRecognitionService()).record(
            stored_partial, stored_pre_inflection=stored_strong, current_pre_inflection=strong,
            pre_inflection_review=strong_pre_review, market_snapshot=partial_market, review_id="PRICE-REV-PARTIAL",
            decision="AUTHORIZE_EIP_REVIEW", notes="Partial recognition authorized for stage review.",
            reviewed_at=now + timedelta(days=186), reviewer="Human Price Recognition Reviewer",
        )
        stage_four = EIPClassificationService().classify(
            classification_id="EIP-4", stored_pre_inflection=stored_strong, current_pre_inflection=strong,
            stored_recognition=stored_partial, current_recognition=partial_recognition,
            recognition_review=partial_review, risk_disposition="CLEAR", risk_rationale="Risks reviewed.",
            valuation_room="SUFFICIENT", valuation_rationale="Some valuation room remains.",
        )
        assert stage_four.stage.value == "STAGE_4_EARLY_CONFIRMATION"
        eip_repository = EIPRepository(root / "eip.jsonl")
        stored_stage_three = eip_repository.add(stage_three)
        assert eip_repository.all() == (stored_stage_three,)
        eip_reviews = EIPReviewLedger(root / "eip-reviews.jsonl", EIPClassificationService())
        stage_three_authorized = eip_reviews.record(
            stored_stage_three,
            stored_pre_inflection=stored_strong, current_pre_inflection=strong,
            stored_recognition=stored_strong_recognition, current_recognition=strong_recognition,
            recognition_review=strong_price_review, review_id="EIP-REV-3",
            decision="AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW",
            notes="Stage 3 may enter the existing governed Evidence review only.",
            reviewed_at=now + timedelta(days=187), reviewer="Human EIP Reviewer",
        )
        assert stage_three_authorized.stage == "STAGE_3_EARLIEST_INVESTABLE_POINT"
        assert eip_reviews.all() == (stage_three_authorized,)
        evidence_candidate = EIPEvidenceReviewCandidateService().build(
            candidate_id="EIP-EVIDENCE-REVIEW-3", stored_eip=stored_stage_three,
            eip_review=stage_three_authorized, stored_pre_inflection=stored_strong,
            stored_meta=coherent_stored, temporal_evidence=records,
        )
        assert evidence_candidate.requires_human_evidence_assessment
        assert tuple(item.temporal_evidence_id for item in evidence_candidate.evidence_references) == ("TE-1", "TE-2")
        assert evidence_candidate.non_authority_statement == EIPEvidenceReviewCandidateService.NON_AUTHORITY
        assert EIPEvidenceReviewCandidateService().build(
            candidate_id="EIP-EVIDENCE-REVIEW-3", stored_eip=stored_stage_three,
            eip_review=stage_three_authorized, stored_pre_inflection=stored_strong,
            stored_meta=coherent_stored, temporal_evidence=reversed(records),
        ).candidate_fingerprint == evidence_candidate.candidate_fingerprint
        try:
            EIPEvidenceReviewCandidateService().build(
                candidate_id="EIP-EVIDENCE-BAD", stored_eip=stored_stage_three,
                eip_review=stage_three_authorized, stored_pre_inflection=stored_strong,
                stored_meta=coherent_stored, temporal_evidence=records[:-1],
            )
            raise AssertionError("incomplete authorized Meta evidence must not produce a review candidate")
        except ValueError as exc:
            assert "does not match authorized Meta inputs" in str(exc)

        stored_stage_two = EIPRepository(root / "eip-stage-two.jsonl").add(stage_two)
        stage_two_reviews = EIPReviewLedger(root / "eip-stage-two-reviews.jsonl", EIPClassificationService())
        try:
            stage_two_reviews.record(
                stored_stage_two,
                stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
                stored_recognition=stored_recognition, current_recognition=recognition,
                recognition_review=eip_authorized, review_id="EIP-REV-2-BAD",
                decision="AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW", notes="Must not authorize.",
                reviewed_at=now + timedelta(days=187), reviewer="Human EIP Reviewer",
            )
            raise AssertionError("Stage 2 must not reach downstream Evidence review")
        except ValueError as exc:
            assert "only eligible Stage 3 or Stage 4" in str(exc)
        stage_two_held = stage_two_reviews.record(
            stored_stage_two,
            stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            stored_recognition=stored_recognition, current_recognition=recognition,
            recognition_review=eip_authorized, review_id="EIP-REV-2",
            decision="HOLD_EIP_RESEARCH", notes="Evidence is still emerging.",
            reviewed_at=now + timedelta(days=187), reviewer="Human EIP Reviewer",
        )
        assert stage_two_held.decision.value == "HOLD_EIP_RESEARCH"
        try:
            EIPEvidenceReviewCandidateService().build(
                candidate_id="EIP-EVIDENCE-STAGE-2", stored_eip=stored_stage_two,
                eip_review=stage_two_held, stored_pre_inflection=stored_pre,
                stored_meta=stored, temporal_evidence=records,
            )
            raise AssertionError("held EIP must not produce an Evidence review candidate")
        except ValueError as exc:
            assert "not authorized" in str(exc)

        stored_stage_five = EIPRepository(root / "eip-stage-five.jsonl").add(stage_five)
        stage_five_reviews = EIPReviewLedger(root / "eip-stage-five-reviews.jsonl", EIPClassificationService())
        try:
            stage_five_reviews.record(
                stored_stage_five,
                stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
                stored_recognition=fully_stored, current_recognition=fully,
                recognition_review=fully_rejected, review_id="EIP-REV-5-BAD",
                decision="HOLD_EIP_RESEARCH", notes="Must not disguise a late case as a hold.",
                reviewed_at=now + timedelta(days=187), reviewer="Human EIP Reviewer",
            )
            raise AssertionError("Stage 5 must be rejected rather than held")
        except ValueError as exc:
            assert "Stage 5 must be rejected" in str(exc)
        stage_five_rejected = stage_five_reviews.record(
            stored_stage_five,
            stored_pre_inflection=stored_pre, current_pre_inflection=pre_inflection,
            stored_recognition=fully_stored, current_recognition=fully,
            recognition_review=fully_rejected, review_id="EIP-REV-5",
            decision="REJECT_EIP_CLASSIFICATION", notes="Potentially late; reject as an EIP candidate.",
            reviewed_at=now + timedelta(days=187), reviewer="Human EIP Reviewer",
        )
        assert stage_five_rejected.decision.value == "REJECT_EIP_CLASSIFICATION"
        try:
            EIPReviewLedger(root / "eip-forged-reviews.jsonl", EIPClassificationService()).record(
                replace(stored_stage_three, classification_fingerprint="0" * 64),
                stored_pre_inflection=stored_strong, current_pre_inflection=strong,
                stored_recognition=stored_strong_recognition, current_recognition=strong_recognition,
                recognition_review=strong_price_review, review_id="EIP-REV-FORGED",
                decision="AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW", notes="Must fail.",
                reviewed_at=now + timedelta(days=187), reviewer="Human EIP Reviewer",
            )
            raise AssertionError("forged EIP fingerprint must be rejected")
        except ValueError as exc:
            assert "fingerprint mismatch" in str(exc)
        try:
            PreInflectionAssessmentService(service.gate).preview(
                preview_id="PRE-BAD", stored_meta=stored,
                meta_review=replace(authorized, assessment_fingerprint="0" * 64),
                temporal_evidence=records, indicator_previews=(preview,),
                what_is_changing="Changed", why_now="Now",
                confirmation_requirements=("Confirm",), invalidation_conditions=("Invalidate",),
                balance_sheet_governance_risks=("Risk",),
            )
        except ValueError as exc:
            assert "bind" in str(exc)
        else:
            raise AssertionError("mismatched Meta review reached Pre-Inflection")
        try:
            MandatoryMetaReviewLedger(root / "forged-reviews.jsonl", service.gate).record(
                StoredMandatoryMetaAnalysis("0" * 64, ready.assessment), temporal_evidence=records,
                indicator_previews=(preview,), review_id="META-FORGED", decision="REJECT_ASSESSMENT",
                notes="Forged fingerprint test.", reviewed_at=now, reviewer="Reviewer",
            )
        except ValueError as exc:
            assert "fingerprint mismatch" in str(exc)
        else:
            raise AssertionError("forged stored Meta assessment accepted")
        held_stored = MandatoryMetaAnalysisRepository(root / "held-meta.jsonl").add(held.assessment)
        held_receipt = MandatoryMetaReviewLedger(root / "held-reviews.jsonl", service.gate).record(
            held_stored, temporal_evidence=records, indicator_previews=(preview,), review_id="META-REV-2",
            decision="HOLD_FOR_RESEARCH", notes="Triggered cancellation kill test requires resolution.",
            reviewed_at=now + timedelta(days=182), reviewer="Human Meta Reviewer",
        )
        assert held_receipt.gate_decision == "HOLD_FOR_RESEARCH"
        blocked_stored = MandatoryMetaAnalysisRepository(root / "blocked-meta.jsonl").add(missing_kill.assessment)
        try:
            MandatoryMetaReviewLedger(root / "blocked-reviews.jsonl", service.gate).record(
                blocked_stored, temporal_evidence=records, indicator_previews=(preview,), review_id="META-REV-3",
                decision="HOLD_FOR_RESEARCH", notes="Attempted override.", reviewed_at=now, reviewer="Reviewer",
            )
        except ValueError as exc:
            assert "rejected and rebuilt" in str(exc)
        else:
            raise AssertionError("human review overrode a technically blocked Meta assessment")
    print("MANDATORY META-ANALYSIS SERVICE: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
