"""Deterministic NSE iXBRL column binding with exception-only human routing."""
from __future__ import annotations

from modules.company_intelligence.exchange_ixbrl_column_review import candidate_fingerprint, prepare_column_review


def assess_automatic_column_binding(candidate: dict) -> dict:
    preview = prepare_column_review(candidate)
    metadata = candidate["metadata"]
    contexts = candidate.get("column_contexts")
    reasons = []
    selected = None
    if preview["column_count"] == 1:
        selected = 0
        reasons.append("ONLY_ONE_NUMERIC_COLUMN")
    elif contexts is None:
        reasons.append("MULTIPLE_COLUMNS_WITHOUT_EXPLICIT_PERIOD_CONTEXT")
    elif not isinstance(contexts, list) or len(contexts) != preview["column_count"]:
        reasons.append("COLUMN_CONTEXT_COUNT_MISMATCH")
    else:
        matches = []
        for index, context in enumerate(contexts):
            if not isinstance(context, dict):
                continue
            if (context.get("period_start") == metadata["period_start"]
                    and context.get("period_end") == metadata["period_end"]
                    and str(context.get("basis", "")).casefold() == str(metadata["basis"]).casefold()):
                matches.append(index)
        if len(matches) == 1:
            selected = matches[0]
            reasons.append("EXACT_PERIOD_AND_BASIS_CONTEXT_MATCH")
        elif not matches:
            reasons.append("NO_COLUMN_MATCHES_DECLARED_PERIOD_AND_BASIS")
        else:
            reasons.append("MULTIPLE_COLUMNS_MATCH_DECLARED_PERIOD_AND_BASIS")
    status = "AUTO_BOUND_PROVISIONAL" if selected is not None else "NEEDS_HUMAN_COLUMN_REVIEW"
    return {
        "schema_version": 1, "candidate_fingerprint": candidate_fingerprint(candidate),
        "status": status, "selected_column": selected, "reasons": reasons,
        "binding_authority": "DETERMINISTIC_METADATA_RULES_V1",
        "validation_status": "PROVISIONAL", "requires_human_review": selected is None,
        "creates_approved_facts": False,
    }


def apply_automatic_column_binding(candidate: dict, assessment: dict) -> dict:
    current = assess_automatic_column_binding(candidate)
    if assessment != current or current["status"] != "AUTO_BOUND_PROVISIONAL":
        raise ValueError("current deterministic assessment does not permit automatic binding")
    index = current["selected_column"]
    return {
        **candidate,
        "values_inr_lakh": {metric: [values[index]] for metric, values in candidate["values_inr_lakh"].items()},
        "column_binding": {
            "selected_column": index, "method": current["binding_authority"],
            "candidate_fingerprint": current["candidate_fingerprint"],
            "reasons": current["reasons"], "validation_status": "PROVISIONAL",
        },
        "status": "EXCHANGE_CORROBORATION_CANDIDATE",
        "creates_approved_facts": False,
    }


__all__ = ["assess_automatic_column_binding", "apply_automatic_column_binding"]
