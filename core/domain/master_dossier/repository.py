"""
Repository for Master Dossiers.

Responsible for:
- Save
- Load
- Delete
- Exists
"""

import json
from pathlib import Path

from .dossier import MasterDossier


class MasterDossierRepository:

    def __init__(self, storage_path: str = "data/dossiers"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save(self, dossier: MasterDossier):

        file_path = self.storage_path / f"{dossier.company_id}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                dossier.to_dict(),
                file,
                indent=4,
                default=str
            )

    def load(self, company_id: str) -> MasterDossier:

        file_path = self.storage_path / f"{company_id}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"{company_id} not found.")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return MasterDossier.from_dict(data)

    def exists(self, company_id: str) -> bool:

        file_path = self.storage_path / f"{company_id}.json"

        return file_path.exists()

    def delete(self, company_id: str):

        file_path = self.storage_path / f"{company_id}.json"

        if file_path.exists():
            file_path.unlink()