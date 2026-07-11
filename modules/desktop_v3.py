import tkinter as tk
import sys
import os

# Allow EIOS to find the data folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.anup_data import company as anup
from data.kpit_data import company as kpit
from data.coromandel_data import company as coromandel


# ---------------- COMPANY DATABASE ----------------

companies = {
    "ANUP Engineering": anup,
    "KPIT Technologies": kpit,
    "Coromandel International": coromandel
}


# ---------------- MAIN WINDOW ----------------

window = tk.Tk()
window.title("EIOS - Everest Investment Operating System")
window.geometry("850x550")


# ---------------- MASTER DOSSIER ----------------

def show_company(company_name):

    data = companies[company_name]

    company_window = tk.Toplevel(window)
    company_window.title(data["Name"] + " - Master Dossier")
    company_window.geometry("600x500")

    tk.Label(
        company_window,
        text=data["Name"],
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(
        company_window,
        text="EIOS MASTER DOSSIER",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tk.Label(
        company_window,
        text="Business Quality : " + data["Business Quality"],
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        company_window,
        text="Management : " + data["Management"],
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        company_window,
        text="Moat : " + data["Moat"],
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        company_window,
        text="Financial Quality : " + data["Financial Quality"],
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        company_window,
        text="Valuation : " + data["Valuation"],
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        company_window,
        text="Expected CAGR : " + data["Expected CAGR"],
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        company_window,
        text="Status : " + data["Status"],
        font=("Arial", 12, "bold")
    ).pack(pady=15)


# ---------------- COMPANY REGISTRY ----------------

def company_registry():

    registry = tk.Toplevel(window)
    registry.title("EIOS Company Registry")
    registry.geometry("550x450")

    tk.Label(
        registry,
        text="EIOS Company Registry",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    for company_name in companies:

        tk.Button(
            registry,
            text=company_name,
            width=35,
            command=lambda name=company_name: show_company(name)
        ).pack(pady=8)


# ---------------- MAIN DASHBOARD ----------------

tk.Label(
    window,
    text="EIOS",
    font=("Arial", 30, "bold")
).pack(pady=(30, 5))

tk.Label(
    window,
    text="Everest Investment Operating System",
    font=("Arial", 16)
).pack(pady=(0, 30))

tk.Button(
    window,
    text="Company Registry",
    width=35,
    height=2,
    command=company_registry
).pack(pady=10)

tk.Button(
    window,
    text="Research Engine",
    width=35,
    height=2
).pack(pady=10)

tk.Button(
    window,
    text="Portfolio",
    width=35,
    height=2
).pack(pady=10)

tk.Button(
    window,
    text="Exit",
    width=35,
    command=window.destroy
).pack(pady=25)


# ---------------- START EIOS ----------------

window.mainloop()