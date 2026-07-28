"""
Module: EIOS Entry Point

Purpose:
Starts the Everest Investment Operating System.
"""
from modules.research_context.research_context import ResearchContext
from core.application import EIOSApplication


def main():
    app = EIOSApplication()
    app.run()


if __name__ == "__main__":
    main()