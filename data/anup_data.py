import json
import os

BASE_DIR = os.path.dirname(__file__)

with open(
    os.path.join(BASE_DIR, "dossiers", "anup.json"),
    "r",
    encoding="utf-8"
) as f:
    anup_data = json.load(f)