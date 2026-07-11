import json
import os

BASE_DIR = os.path.dirname(__file__)

with open(
    os.path.join(BASE_DIR, "dossiers", "kpit.json"),
    "r",
    encoding="utf-8"
) as f:
    kpit_data = json.load(f)