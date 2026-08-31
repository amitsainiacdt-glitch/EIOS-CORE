"""Plain-English renderer for governed live-case readiness and queue artifacts."""

import json
from pathlib import Path


def render_plain_english_live_status(*,readiness_path,queue_path):
    readiness=json.loads(Path(readiness_path).read_text(encoding="utf-8")); queue=json.loads(Path(queue_path).read_text(encoding="utf-8"))
    assessment=readiness["assessment"]; ceiling=readiness["causal_interpretation_confidence_ceiling"]
    lines=[
        f"Case: {readiness['inputs']['case_id']}",
        f"Current stage: {assessment['stage']}",
        f"What this means: {assessment['permitted_claim']}",
        f"Maximum confidence in the causal interpretation: {ceiling['maximum_confidence_percent']}% ({'eligible' if ceiling['confidence_eligible'] else 'not eligible for a formal hypothesis'})",
        "",
        "What is verified:",
        "- Current official rainfall evidence is structured and review-only.",
        "- Current crop-area progress is structured across four reporting dates.",
        "- Fertilizer availability, geographic balance, and aggregate consumption have governed records.",
        "- Contradicting evidence is retained rather than hidden.",
        "",
        "What is still missing:",
    ]
    lines.extend(f"- {item}" for item in readiness["inputs"]["unresolved_gaps"])
    lines.extend(("","Research queue:"))
    eligible=[item for item in queue["items"] if item["eligible_now"]]
    if eligible:
        lines.extend(f"- {item['need_id']}: {item['action']}" for item in eligible)
    else:
        lines.append("- No external action is eligible now; sources are under backoff, require user-issued access, or are deliberately deferred.")
    lines.extend(("","Safety boundary:",readiness["non_authority_statement"],f"Production objects created by this status report: {'yes' if readiness['creates_observation'] else 'no'}"))
    return "\n".join(lines)+"\n"


__all__=["render_plain_english_live_status"]
