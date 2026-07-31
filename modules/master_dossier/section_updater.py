"""
===============================================================================
EIOS
Section Updater

Purpose:
    Generic utility responsible for updating Master Dossier sections from
    analysis results.

    This class contains NO business logic. It only transfers validated data
    into the appropriate section.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from dataclasses import fields, is_dataclass


class SectionUpdater:
    """
    Generic updater for Master Dossier sections.

    Copies matching attributes from an analysis object into a destination
    section while preserving strong typing.
    """

    @staticmethod
    def update(section, analysis):
        """
        Update a Master Dossier section from an analysis object.

        Parameters
        ----------
        section:
            Destination section inside MasterDossier.

        analysis:
            Analysis object containing calculated values.

        Returns
        -------
        Updated section.
        """

        if analysis is None:
            return section

        # -------------------------------------------------------------
        # Dataclass -> Dataclass
        # -------------------------------------------------------------

        if is_dataclass(section):

            for field in fields(section):

                name = field.name

                if hasattr(analysis, name):

                    value = getattr(analysis, name)

                    if value is not None:
                        setattr(section, name, value)

        # -------------------------------------------------------------
        # Generic object fallback
        # -------------------------------------------------------------

        elif hasattr(section, "__dict__"):

            for name, value in vars(analysis).items():

                if hasattr(section, name):

                    if value is not None:
                        setattr(section, name, value)

        return section