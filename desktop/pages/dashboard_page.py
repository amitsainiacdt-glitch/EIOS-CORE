"""
EIOS Dashboard Page
Release 20.0

Executive Dashboard
"""

from tkinter import ttk

from desktop.widgets.kpi_card import KPICard
from desktop.charts.revenue_chart import RevenueChart


class DashboardPage(ttk.Frame):

    def __init__(self, parent, dossier):

        super().__init__(parent)

        self.dossier = dossier

        self.build()

    # ==========================================================
    # BUILD DASHBOARD
    # ==========================================================

    def build(self):

        ttk.Label(
            self,
            text="Executive Dashboard",
            style="Title.TLabel",
        ).pack(anchor="w", pady=(0, 20))

        recommendation = self.dossier.decision.get(
            "recommendation",
            "-"
        )

        confidence = self.dossier.decision.get(
            "confidence",
            "-"
        )

        intrinsic = "-"

        if "Intrinsic Value" in self.dossier.valuation:

            intrinsic = (
                self.dossier.valuation[
                    "Intrinsic Value"
                ].fair_value
            )

        # ======================================================
        # KPI CARDS
        # ======================================================

        card_frame = ttk.Frame(self)

        card_frame.pack(
            fill="x",
            pady=(0, 25),
        )

        KPICard(
            card_frame,
            "Company",
            self.dossier.ticker,
        ).pack(
            side="left",
            padx=6,
        )

        KPICard(
            card_frame,
            "Recommendation",
            recommendation,
        ).pack(
            side="left",
            padx=6,
        )

        KPICard(
            card_frame,
            "Intrinsic Value",
            intrinsic,
        ).pack(
            side="left",
            padx=6,
        )

        KPICard(
            card_frame,
            "Confidence",
            confidence,
        ).pack(
            side="left",
            padx=6,
        )

        # ======================================================
        # DETAILS
        # ======================================================

        details = ttk.LabelFrame(
            self,
            text="Investment Summary",
            padding=15,
        )

        details.pack(
            fill="x",
            pady=10,
        )

        self.add_row(
            details,
            "Company",
            self.dossier.company_name,
        )

        self.add_row(
            details,
            "Ticker",
            self.dossier.ticker,
        )

        self.add_row(
            details,
            "Recommendation",
            recommendation,
        )

        self.add_row(
            details,
            "Confidence",
            confidence,
        )

        self.add_row(
            details,
            "Intrinsic Value",
            intrinsic,
        )
        self.add_row(
            details,
            "Business Rating",
            self.dossier.business.rating or "-",
        )

        self.add_row(
            details,
           "Financial Rating",
            self.dossier.financial.rating or "-",
        )

        self.add_row(
            details,
            "Management Rating",
            self.dossier.management.get(
                "Overall Score",
                {}
            ).get(
                "Rating",
                "-"
            ),
        )

        self.add_row(
            details,
            "Risk Rating",
            self.dossier.risks.get(
                "Overall Risk",
                {}
            ).get(
                "Rating",
                "-"
            ),
        )

        self.add_row(
            details,
            "Competitive Rating",
            self.dossier.competitive.get(
                "Overall Score",
                {}
            ).get(
                "Rating",
                "-"
            ),
        )
        self.add_row(
            details,
            "Valuation Rating",
            self.dossier.valuation.get(
                "Overall Score",
                {}
            ).get(
                "Rating",
                "-"
            ),
        )

        # ======================================================
        # REVENUE CHART
        # ======================================================

        chart_frame = ttk.LabelFrame(
            self,
            text="Revenue Trend",
            padding=10,
        )

        chart_frame.pack(
            fill="both",
            expand=True,
            pady=20,
        )

        RevenueChart(
            chart_frame,
            revenue=[
                620,
                710,
                845,
                980,
                1200,
            ],
        ).pack(
            fill="both",
            expand=True,
        )

    # ==========================================================
    # ROW
    # ==========================================================

    def add_row(self, parent, label, value):

        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            pady=3,
        )

        ttk.Label(
            frame,
            text=label,
            width=24,
            style="Header.TLabel",
        ).pack(
            side="left",
        )

        ttk.Label(
            frame,
            text=str(value),
        ).pack(
            side="left",
        )