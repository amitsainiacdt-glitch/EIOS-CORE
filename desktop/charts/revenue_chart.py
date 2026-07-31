"""
Revenue Trend Chart
Release 20.2
"""

from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class RevenueChart(ttk.Frame):

    def __init__(self, parent, revenue):

        super().__init__(parent)

        fig = Figure(figsize=(6, 3), dpi=100)

        ax = fig.add_subplot(111)

        years = list(range(1, len(revenue) + 1))

        ax.plot(
            years,
            revenue,
            linewidth=2,
            marker="o",
        )

        ax.set_title("Revenue Trend")

        ax.set_xlabel("Year")

        ax.set_ylabel("Revenue")

        canvas = FigureCanvasTkAgg(
            fig,
            master=self,
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
        )