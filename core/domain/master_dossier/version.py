"""
Version management for Master Dossiers.
"""

from datetime import datetime

from .dossier import MasterDossier


class MasterDossierVersionManager:
    """
    Handles version updates for Master Dossiers.
    """

    @staticmethod
    def bump_patch(dossier: MasterDossier) -> MasterDossier:
        """
        Increment patch version.
        Example:
            0.1.0 -> 0.1.1
        """

        major, minor, patch = map(int, dossier.version.split("."))

        patch += 1

        dossier.version = f"{major}.{minor}.{patch}"
        dossier.updated_at = datetime.utcnow()

        return dossier

    @staticmethod
    def bump_minor(dossier: MasterDossier) -> MasterDossier:
        """
        Increment minor version.
        Example:
            0.1.4 -> 0.2.0
        """

        major, minor, patch = map(int, dossier.version.split("."))

        minor += 1
        patch = 0

        dossier.version = f"{major}.{minor}.{patch}"
        dossier.updated_at = datetime.utcnow()

        return dossier

    @staticmethod
    def bump_major(dossier: MasterDossier) -> MasterDossier:
        """
        Increment major version.
        Example:
            0.9.5 -> 1.0.0
        """

        major, minor, patch = map(int, dossier.version.split("."))

        major += 1
        minor = 0
        patch = 0

        dossier.version = f"{major}.{minor}.{patch}"
        dossier.updated_at = datetime.utcnow()

        return dossier