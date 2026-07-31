"""
EIOS KPI Card
Release 20.0
"""

from tkinter import ttk


class KPICard(ttk.Frame):

    def __init__(self, parent, title, value, width=220):

        super().__init__(
            parent,
            padding=15,
        )

        self.configure(width=width)

        self.pack_propagate(False)

        self.title = ttk.Label(
            self,
            text=title,
            style="Header.TLabel",
        )

        self.title.pack(anchor="w")

        self.value = ttk.Label(
            self,
            text=str(value),
            style="Title.TLabel",
        )

        self.value.pack(
            anchor="w",
            pady=(10, 0),
        )

    def update_value(self, value):

        self.value.config(text=str(value))