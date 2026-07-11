import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.anup_data import company

# ---------------- MAIN WINDOW ----------------

window = tk.Tk()
window.title("EIOS - Everest Investment Operating System")
window.geometry("800x500")


# ---------------- COMPANY WINDOW ----------------

def show_company(name):

    company_window = tk.Toplevel(window)
    company_window.title(name)
    company_window.geometry("500x450")

    tk.Label(
        company_window,
        text=company["Name"],
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        company_window,
        text="Business Quality : " + company["Business Quality"]
    ).pack()

    tk.Label(
        company_window,
        text="Management : " + company["Management"]
    ).pack()

    tk.Label(
        company_window,
        text="Moat : " + company["Moat"]
    ).pack()

    tk.Label(
        company_window,
        text="Financial Quality : " + company["Financial Quality"]
    ).pack()

    tk.Label(
        company_window,
        text="Valuation : " + company["Valuation"]
    ).pack()

    tk.Label(
        company_window,
        text="Expected CAGR : " + company["Expected CAGR"]
    ).pack()

    tk.Label(
        company_window,
        text="Status : " + company["Status"]
    ).pack(pady=10)


# ---------------- COMPANY REGISTRY ----------------

def company_registry():

    registry = tk.Toplevel(window)
    registry.title("Company Registry")
    registry.geometry("500x400")

    tk.Label(
        registry,
        text="EIOS Company Registry",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        registry,
        text="ANUP Engineering",
        width=30,
        command=lambda: show_company("ANUP Engineering")
    ).pack(pady=5)

    tk.Button(
        registry,
        text="KPIT Technologies",
        width=30,
        command=lambda: show_company("KPIT Technologies")
    ).pack(pady=5)

    tk.Button(
        registry,
        text="Coromandel International",
        width=30,
        command=lambda: show_company("Coromandel International")
    ).pack(pady=5)


# ---------------- MAIN SCREEN ----------------

tk.Label(
    window,
    text="EIOS\nEverest Investment Operating System",
    font=("Arial", 22, "bold")
).pack(pady=25)

tk.Button(
    window,
    text="Company Registry",
    width=30,
    command=company_registry
).pack(pady=10)

tk.Button(
    window,
    text="Research Engine",
    width=30
).pack(pady=10)

tk.Button(
    window,
    text="Portfolio",
    width=30
).pack(pady=10)

tk.Button(
    window,
    text="Exit",
    width=30,
    command=window.destroy
).pack(pady=20)

window.mainloop()