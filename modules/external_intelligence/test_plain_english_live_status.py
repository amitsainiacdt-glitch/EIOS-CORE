import json
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.plain_english_live_status import render_plain_english_live_status


def main():
    with TemporaryDirectory() as directory:
        root=Path(directory); readiness=root/"readiness.json"; queue=root/"queue.json"
        readiness.write_text(json.dumps({"inputs":{"case_id":"CASE","unresolved_gaps":["Current reservoir evidence is missing."]},"assessment":{"stage":"WEATHER_CROP_HINT_ONLY","permitted_claim":"Weather and crop hint only."},"causal_interpretation_confidence_ceiling":{"maximum_confidence_percent":10,"confidence_eligible":False},"non_authority_statement":"Research only.","creates_observation":False}),encoding="utf-8")
        queue.write_text(json.dumps({"items":[{"need_id":"RESERVOIR","action":"WAIT","eligible_now":False}]}),encoding="utf-8")
        text=render_plain_english_live_status(readiness_path=readiness,queue_path=queue)
        assert "WEATHER_CROP_HINT_ONLY" in text and "10%" in text and "Current reservoir evidence is missing" in text and "Production objects created by this status report: no" in text
    print("PLAIN-ENGLISH LIVE STATUS: ALL TESTS PASSED")


if __name__=="__main__": main()
