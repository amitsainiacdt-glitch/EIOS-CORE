"""
EIOS Score Card
Release 20.1
"""

from tkinter import ttk


class ScoreCard(ttk.Frame):

    def __init__(
        self,
        parent,
        title,
        score,
        rating,
        width=220,
        height=120,
    ):

        super().__init__(
            parent,
            padding=15,
        )

        self.configure(
            width=width,
            height=height,
        )

        self.pack_propagate(False)

        ttk.Label(
            self,
            text=title,
            style="Header.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            self,
            text=str(rating),
            style="Title.TLabel",
        ).pack(
            anchor="center",
            pady=(15, 5),
        )

        ttk.Label(
            self,
            text=f"Score : {score}",
        ).pack(anchor="center")

    def update(self, score, rating):

        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(
            self,
            text="Updated",
            style="Header.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            self,
            text=str(rating),
            style="Title.TLabel",
        ).pack(
            anchor="center",
            pady=(15, 5),
        )

        ttk.Label(
            self,
            text=f"Score : {score}",
        ).pack(anchor="center")