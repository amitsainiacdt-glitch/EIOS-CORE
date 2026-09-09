"""Create a held, hash-bound financial corroboration record from official NSE iXBRL."""
import argparse
import hashlib
import json
from pathlib import Path

from modules.company_intelligence.exchange_ixbrl_financial import parse_exchange_ixbrl_financial


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--source-url", required=True)
    args = parser.parse_args()
    path = (ROOT / args.file).resolve()
    if ROOT not in path.parents:
        raise ValueError("input must remain inside EIOS")
    body = path.read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    report = parse_exchange_ixbrl_financial(body.decode("utf-8", errors="replace"),
                                            source_url=args.source_url, document_hash=digest)
    output = ROOT / "data/runtime/exchange_ixbrl" / digest / "corroboration.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "ticker": report["metadata"]["ticker"],
                      "metric_count": len(report["values_inr_lakh"]), "output": str(output),
                      "creates_approved_facts": False}))


if __name__ == "__main__":
    main()
