"""
EIOS Desktop Theme
Release 19
"""

import tkinter as tk
from tkinter import ttk

# --------------------------------------------------------
# COLORS
# --------------------------------------------------------

BACKGROUND = "#1E1E1E"
SIDEBAR = "#252526"
CARD = "#2D2D30"

TEXT = "#FFFFFF"
SUBTEXT = "#C8C8C8"

ACCENT = "#007ACC"
SUCCESS = "#28A745"
WARNING = "#FFC107"
DANGER = "#DC3545"

# --------------------------------------------------------
# FONTS
# --------------------------------------------------------

TITLE_FONT = ("Segoe UI", 20, "bold")
HEADER_FONT = ("Segoe UI", 14, "bold")
BODY_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 10)

# --------------------------------------------------------
# WINDOW
# --------------------------------------------------------

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

SIDEBAR_WIDTH = 220

# --------------------------------------------------------
# STYLE
# --------------------------------------------------------

def apply_theme(root):

    style = ttk.Style(root)

    style.theme_use("clam")

    root.configure(bg=BACKGROUND)

    style.configure(
        "TFrame",
        background=BACKGROUND
    )

    style.configure(
        "Sidebar.TFrame",
        background=SIDEBAR
    )

    style.configure(
        "Card.TFrame",
        background=CARD
    )

    style.configure(
        "TLabel",
        background=BACKGROUND,
        foreground=TEXT,
        font=BODY_FONT
    )

    style.configure(
        "Header.TLabel",
        font=HEADER_FONT,
        foreground=TEXT,
        background=BACKGROUND
    )

    style.configure(
        "Title.TLabel",
        font=TITLE_FONT,
        foreground=TEXT,
        background=BACKGROUND
    )

    style.configure(
        "TButton",
        font=BODY_FONT,
        padding=6
    )