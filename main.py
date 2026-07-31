"""
Module: EIOS Entry Point

Purpose:
Starts the Everest Investment Operating System.
"""

from core.application import EIOSApplication
from desktop.app import DesktopApplication


def main():

    app = EIOSApplication()

    dossier = app.run()

    desktop = DesktopApplication(dossier)

    desktop.run()


if __name__ == "__main__":
    main()