"""Print the current India Kharif case in plain English."""

from modules.external_intelligence.plain_english_live_status import render_plain_english_live_status


def main():
    print(render_plain_english_live_status(readiness_path="data/live_cases/india_kharif_2026/structured/india_kharif_2026_pre_inflection_readiness.json",queue_path="data/live_cases/india_kharif_2026/structured/india_kharif_2026_evidence_queue.json"),end="")


if __name__=="__main__": main()
