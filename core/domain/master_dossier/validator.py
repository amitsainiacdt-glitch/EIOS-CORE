"""
Validation logic for Master Dossiers.
"""

from .dossier import MasterDossier


class MasterDossierValidator:
    """
    Validates Master Dossier objects before they are
    persisted or processed.
    """

    @staticmethod
    def validate(dossier: MasterDossier):

        errors = []

        # ==========================================
        # Company Identity
        # ==========================================
        if not dossier.company_id:
            errors.append("company_id is required.")

        if not dossier.company_name:
            errors.append("company_name is required.")

        if not dossier.exchange:
            errors.append("exchange is required.")

        if not dossier.sector:
            errors.append("sector is required.")

        if not dossier.industry:
            errors.append("industry is required.")

        # ==========================================
        # Metadata
        # ==========================================
        if not dossier.version:
            errors.append("version is required.")

        # ==========================================
        # Validation Result
        # ==========================================
        if errors:
            raise ValueError(
                "\n".join(errors)
            )

        return True