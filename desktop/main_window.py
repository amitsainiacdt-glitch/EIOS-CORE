"""
EIOS Main Window
Release 19.3
"""

import tkinter as tk
from tkinter import ttk

from desktop.theme import (
    apply_theme,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SIDEBAR_WIDTH,
)

from desktop.pages.dashboard_page import DashboardPage


class MainWindow:

    def __init__(self, dossier):

        self.dossier = dossier

        self.root = tk.Tk()

        self.root.title("EVEREST INVESTMENT OPERATING SYSTEM")

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.root.minsize(1200, 700)

        apply_theme(self.root)

        self.build_layout()

    def build_layout(self):

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.sidebar = ttk.Frame(
            self.root,
            width=SIDEBAR_WIDTH,
            style="Sidebar.TFrame",
        )

        self.sidebar.pack(
            side="left",
            fill="y",
        )

        self.sidebar.pack_propagate(False)

        # =====================================================
        # CONTENT AREA
        # =====================================================

        self.content = ttk.Frame(self.root)

        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        # =====================================================
        # LOGO
        # =====================================================

        ttk.Label(
            self.sidebar,
            text="EIOS",
            style="Title.TLabel",
        ).pack(pady=25)

        # =====================================================
        # SIDEBAR BUTTONS
        # =====================================================

        self.buttons = {}

        pages = [
            "Dashboard",
            "Research",
            "Intelligence",
            "Committee",
            "Portfolio",
            "Settings",
        ]

        for page in pages:

            button = ttk.Button(
                self.sidebar,
                text=page,
                command=lambda p=page: self.show_page(p),
            )

            button.pack(
                fill="x",
                padx=10,
                pady=5,
            )

            self.buttons[page] = button

        # =====================================================
        # CREATE PAGES
        # =====================================================

        self.pages = {}

        self.pages["Dashboard"] = DashboardPage(
            self.content,
            self.dossier,
        )

        # Show first page

        self.show_page("Dashboard")

    # =========================================================
    # PAGE NAVIGATION
    # =========================================================

    def show_page(self, page_name):

        # Hide all pages

        for page in self.pages.values():

            page.pack_forget()

        # Dashboard already exists

        if page_name == "Dashboard":

            self.pages["Dashboard"].pack(
                fill="both",
                expand=True,
            )

            return

        # Placeholder pages

        frame = ttk.Frame(self.content)

        ttk.Label(
            frame,
            text=f"{page_name}\n\nComing Soon",
            style="Title.TLabel",
        ).pack(
            expand=True,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

    # =========================================================
    # START APPLICATION
    # =========================================================

    def run(self):

        self.root.mainloop()