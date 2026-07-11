import tkinter as tk
from tkinter import ttk
import sys
import os

# Allow EIOS to find the data folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data.anup_data import company as anup
from data.kpit_data import company as kpit
from data.coromandel_data import company as coromandel


# ==================================================
# EIOS COMPANY DATABASE
# ==================================================

companies = {
    "ANUP Engineering": anup,
    "KPIT Technologies": kpit,
    "Coromandel International": coromandel
}


# ==================================================
# MAIN WINDOW
# ==================================================

window = tk.Tk()
window.title("EIOS - Everest Investment Operating System")
window.geometry("1000x650")
window.minsize(900, 600)


# ==================================================
# MASTER DOSSIER ENGINE
# ==================================================

def show_company(company_name):

    data = companies[company_name]

    dossier = tk.Toplevel(window)
    dossier.title(data["Name"] + " - EIOS Master Dossier")
    dossier.geometry("900x650")

    # Company heading

    tk.Label(
        dossier,
        text=data["Name"],
        font=("Arial", 24, "bold")
    ).pack(pady=(20, 5))

    tk.Label(
        dossier,
        text="EIOS MASTER DOSSIER",
        font=("Arial", 13, "bold")
    ).pack(pady=(0, 15))


    # Notebook creates professional tabs

    notebook = ttk.Notebook(dossier)
    notebook.pack(fill="both", expand=True, padx=20, pady=10)


    # ---------------- OVERVIEW TAB ----------------

    overview = ttk.Frame(notebook)
    notebook.add(overview, text="Overview")

    overview_text = f"""
Company Name: {data["Name"]}

Business Quality: {data["Business Quality"]}

Management: {data["Management"]}

Moat: {data["Moat"]}

Financial Quality: {data["Financial Quality"]}

Valuation: {data["Valuation"]}

Expected CAGR: {data["Expected CAGR"]}

Current Status: {data["Status"]}
"""

    tk.Label(
        overview,
        text=overview_text,
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30, pady=25)


    # ---------------- BUSINESS QUALITY TAB ----------------

    business = ttk.Frame(notebook)
    notebook.add(business, text="Business Quality")

    tk.Label(
        business,
        text="BUSINESS QUALITY ANALYSIS",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        business,
        text=(
            "Business model analysis\n\n"
            "Industry structure\n\n"
            "Growth runway\n\n"
            "Competitive positioning\n\n"
            "EIOS Status: Pending full evidence validation"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- MANAGEMENT TAB ----------------

    management = ttk.Frame(notebook)
    notebook.add(management, text="Management")

    tk.Label(
        management,
        text="MANAGEMENT & CAPITAL ALLOCATION",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        management,
        text=(
            "Promoter assessment\n\n"
            "Capital allocation history\n\n"
            "Governance\n\n"
            "Management credibility\n\n"
            "EIOS Status: Pending full evidence validation"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- MOAT TAB ----------------

    moat = ttk.Frame(notebook)
    notebook.add(moat, text="Moat")

    tk.Label(
        moat,
        text="COMPETITIVE ADVANTAGE & MOAT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        moat,
        text=(
            "Competitive advantages\n\n"
            "Barriers to entry\n\n"
            "Pricing power\n\n"
            "Customer stickiness\n\n"
            "Moat durability\n\n"
            "EIOS Status: Pending full evidence validation"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- FINANCIALS TAB ----------------

    financials = ttk.Frame(notebook)
    notebook.add(financials, text="Financials")

    tk.Label(
        financials,
        text="FINANCIAL QUALITY",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        financials,
        text=(
            "Revenue growth\n\n"
            "Profit growth\n\n"
            "Margins\n\n"
            "Return on capital\n\n"
            "Cash conversion\n\n"
            "Balance sheet quality\n\n"
            "EIOS Status: Pending financial data integration"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- VALUATION TAB ----------------

    valuation = ttk.Frame(notebook)
    notebook.add(valuation, text="Valuation")

    tk.Label(
        valuation,
        text="EIOS VALUATION ENGINE",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        valuation,
        text=(
            f"Current Assessment: {data['Valuation']}\n\n"
            f"Expected CAGR: {data['Expected CAGR']}\n\n"
            "Fair Value: Pending\n\n"
            "Margin of Safety: Pending\n\n"
            "Bear Case: Pending\n\n"
            "Base Case: Pending\n\n"
            "Bull Case: Pending"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- RISKS TAB ----------------

    risks = ttk.Frame(notebook)
    notebook.add(risks, text="Risks")

    tk.Label(
        risks,
        text="RISK & CONTRADICTION ENGINE",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        risks,
        text=(
            "Business risks\n\n"
            "Management risks\n\n"
            "Financial risks\n\n"
            "Disruption risks\n\n"
            "Thesis killers\n\n"
            "Contradictory evidence\n\n"
            "EIOS Status: Pending evidence review"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- EVIDENCE TAB ----------------

    evidence = ttk.Frame(notebook)
    notebook.add(evidence, text="Evidence Register")

    tk.Label(
        evidence,
        text="EIOS EVIDENCE REGISTER",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        evidence,
        text=(
            "Annual Reports: Pending integration\n\n"
            "Conference Calls: Pending integration\n\n"
            "Investor Presentations: Pending integration\n\n"
            "Exchange Filings: Pending integration\n\n"
            "Competitor Evidence: Pending integration\n\n"
            "Evidence Reliability Grade: Pending"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


    # ---------------- VERDICT TAB ----------------

    verdict = ttk.Frame(notebook)
    notebook.add(verdict, text="EIOS Verdict")

    tk.Label(
        verdict,
        text="EIOS INVESTMENT COMMITTEE VERDICT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        verdict,
        text=(
            f"Current Status: {data['Status']}\n\n"
            "Business Quality Vote: Pending\n\n"
            "Investment Today Vote: Pending\n\n"
            "Portfolio Fit Vote: Pending\n\n"
            "Correction Classification: Pending\n\n"
            "Regret Test: Pending\n\n"
            "Final CIO Decision: Pending full EIOS validation"
        ),
        font=("Arial", 12),
        justify="left"
    ).pack(anchor="nw", padx=30)


# ==================================================
# COMPANY REGISTRY
# ==================================================

def company_registry():

    registry = tk.Toplevel(window)
    registry.title("EIOS Company Registry")
    registry.geometry("600x500")

    tk.Label(
        registry,
        text="EIOS Company Registry",
        font=("Arial", 22, "bold")
    ).pack(pady=25)

    tk.Label(
        registry,
        text=f"Tracked Companies: {len(companies)}",
        font=("Arial", 12)
    ).pack(pady=(0, 20))

    for company_name in companies:

        tk.Button(
            registry,
            text=company_name,
            width=40,
            height=2,
            command=lambda name=company_name: show_company(name)
        ).pack(pady=8)


# ==================================================
# MAIN DASHBOARD
# ==================================================

tk.Label(
    window,
    text="EIOS",
    font=("Arial", 34, "bold")
).pack(pady=(40, 5))

tk.Label(
    window,
    text="Everest Investment Operating System",
    font=("Arial", 17)
).pack(pady=(0, 10))

tk.Label(
    window,
    text="Evidence • Conviction • Valuation • Portfolio Discipline",
    font=("Arial", 11)
).pack(pady=(0, 30))

tk.Button(
    window,
    text="Company Registry",
    width=38,
    height=2,
    command=company_registry
).pack(pady=8)

tk.Button(
    window,
    text="Research Engine",
    width=38,
    height=2
).pack(pady=8)

tk.Button(
    window,
    text="Portfolio",
    width=38,
    height=2
).pack(pady=8)

tk.Button(
    window,
    text="Watchlist",
    width=38,
    height=2
).pack(pady=8)

tk.Button(
    window,
    text="Exit",
    width=38,
    command=window.destroy
).pack(pady=25)


# ==================================================
# START EIOS
# ==================================================

window.mainloop()