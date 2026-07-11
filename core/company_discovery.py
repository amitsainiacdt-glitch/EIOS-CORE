import os
import json

DOSSIER_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "dossiers"
)

def discover_companies():

    companies = []

    for file in os.listdir(DOSSIER_FOLDER):

        if file.endswith(".json"):

            path = os.path.join(DOSSIER_FOLDER, file)

            with open(path, "r", encoding="utf-8") as f:

                data = json.load(f)

            companies.append(data)

    return companies