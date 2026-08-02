"""
Module: EIOS Entry Point

Purpose:
Starts the Everest Investment Operating System.

Architecture:
- Core always runs.
- Desktop is optional.
"""

from core.application import EIOSApplication


def main():

    app = EIOSApplication()

    dossier = app.run()

    # ---------------------------------------------------------
    # Launch Desktop (Optional)
    # ---------------------------------------------------------

    try:
        from desktop.app import DesktopApplication

        desktop = DesktopApplication(dossier)
        desktop.run()

    except Exception as exc:

        print()
        print("=" * 60)
        print("DESKTOP NOT AVAILABLE")
        print("=" * 60)
        print(exc)
        print()
        print("Continuing in console mode...")
        print("=" * 60)


if __name__ == "__main__":
    main()