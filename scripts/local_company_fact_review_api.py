"""Local-only HTTP bridge for governed company fact review decisions."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.record_company_fact_review import main as record_review
from scripts.sync_local_status_dashboard import main as sync_dashboard


HOST = "127.0.0.1"
PORT = 3001
ALLOWED_ORIGINS = {"http://localhost:3000", "http://127.0.0.1:3000"}


class ReviewHandler(BaseHTTPRequestHandler):
    server_version = "EIOSReviewBridge/1.0"

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path != "/health":
            return self._json(404, {"ok": False, "error": "Not found"})
        self._json(200, {"ok": True, "service": "EIOS local fact review"})

    def do_POST(self):
        if self.path != "/review":
            return self._json(404, {"ok": False, "error": "Not found"})
        origin = self.headers.get("Origin")
        if origin not in ALLOWED_ORIGINS:
            return self._json(403, {"ok": False, "error": "Review requests are accepted only from the local EIOS dashboard."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 16_384:
                raise ValueError("Invalid request size")
            payload = json.loads(self.rfile.read(size))
            decision = str(payload.get("decision", "")).upper()
            if decision not in {"APPROVE", "HOLD", "REJECT"}:
                raise ValueError("Decision must be APPROVE, HOLD or REJECT")
            rationale = str(payload.get("rationale", "")).strip()
            if len(rationale) < 10:
                raise ValueError("Please provide a rationale of at least 10 characters")
            argv = [
                "--queue", str(payload.get("queuePath", "")),
                "--meta", str(payload.get("metaPath", "")),
                "--candidate-id", str(payload.get("candidateId", "")),
                "--review-id", f"HUMAN-{uuid4().hex}",
                "--decision", decision,
                "--rationale", rationale,
                "--reviewer", str(payload.get("reviewer", "EIOS_LOCAL_USER")).strip() or "EIOS_LOCAL_USER",
            ]
            if decision == "APPROVE":
                confidence = payload.get("approvedConfidence")
                if confidence is None:
                    raise ValueError("Approval confidence is required")
                argv.extend(["--approved-confidence", str(confidence)])
            record_review(argv)
            sync_dashboard()
            self._json(200, {"ok": True, "decision": decision, "message": "Decision recorded in the append-only EIOS audit ledger."})
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self._json(400, {"ok": False, "error": str(exc)})
        except Exception:
            self._json(500, {"ok": False, "error": "The review could not be recorded. No decision was written."})

    def log_message(self, format, *args):
        return

    def _cors_headers(self):
        origin = self.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self._cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    print(f"EIOS local fact review service running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), ReviewHandler).serve_forever()


if __name__ == "__main__":
    main()
