import tkinter as tk
from tkinter import ttk
import json
import os


# ==================================================
# PATH SETUP
# ==================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DOSSIER_PATH = os.path.join(
    BASE_DIR,
    "data",
    "dossiers",
    "anup.json"
)


# ==================================================
# LOAD ANUP MASTER DOSSIER
# ==================================================

def load_dossier():

    with open(DOSSIER_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


anup_data = load_dossier()


# ==================================================
# MAIN WINDOW
# ==================================================

window = tk.Tk()

window.title("EIOS - Everest Investment Operating System")

window.geometry("1100x700")

window.minsize(950, 600)


# ==================================================
# HELPER FUNCTION
# ==================================================

def create_text_tab(notebook, title, heading, content):

    frame = ttk.Frame(notebook)

    notebook.add(frame, text=title)

    tk.Label(
        frame,
        text=heading,
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    text_box = tk.Text(
        frame,
        wrap="word",
        font=("Arial", 11),
        padx=20,
        pady=20
    )

    text_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    text_box.insert("1.0", content)

    text_box.config(state="disabled")


# ==================================================
# ANUP MASTER DOSSIER
# ==================================================

def show_anup_dossier():

    data = anup_data

    dossier = tk.Toplevel(window)

    dossier.title(
        data["company"]["name"] +
        " - EIOS Master Dossier"
    )

    dossier.geometry("1000x700")


    tk.Label(
        dossier,
        text=data["company"]["name"],
        font=("Arial", 24, "bold")
    ).pack(pady=(20, 5))


    tk.Label(
        dossier,
        text=(
            "Ticker: " +
            data["company"]["ticker"] +
            "   |   Sector: " +
            data["company"]["sector"] +
            "   |   Status: " +
            data["company"]["status"]
        ),
        font=("Arial", 11)
    ).pack(pady=(0, 15))


    notebook = ttk.Notebook(dossier)

    notebook.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


    # ---------------- OVERVIEW ----------------

    overview = data["overview"]

    overview_content = f"""
BUSINESS SUMMARY

{overview["business_summary"]}


INVESTMENT THESIS

{overview["investment_thesis"]}


KEY PRODUCTS

{overview["key_products"]}


KEY CUSTOMERS

{overview["key_customers"]}


GROWTH DRIVERS

{overview["growth_drivers"]}
"""

    create_text_tab(
        notebook,
        "Overview",
        "COMPANY OVERVIEW",
        overview_content
    )


    # ---------------- BUSINESS QUALITY ----------------

    business = data["business_quality"]

    business_content = f"""
STATUS

{business["status"]}


BUSINESS MODEL

{business["business_model"]}


INDUSTRY STRUCTURE

{business["industry_structure"]}


GROWTH RUNWAY

{business["growth_runway"]}


COMPETITIVE POSITIONING

{business["competitive_positioning"]}


CYCLICALITY

{business["cyclicality"]}


SCORE

{business["score"]}
"""

    create_text_tab(
        notebook,
        "Business Quality",
        "BUSINESS QUALITY ANALYSIS",
        business_content
    )


    # ---------------- MANAGEMENT ----------------

    management = data["management"]

    management_content = f"""
STATUS

{management["status"]}


PROMOTER ASSESSMENT

{management["promoter_assessment"]}


CAPITAL ALLOCATION

{management["capital_allocation"]}


GOVERNANCE

{management["governance"]}


MANAGEMENT CREDIBILITY

{management["management_credibility"]}


SUCCESSION RISK

{management["succession_risk"]}


SCORE

{management["score"]}
"""

    create_text_tab(
        notebook,
        "Management",
        "MANAGEMENT & CAPITAL ALLOCATION",
        management_content
    )


    # ---------------- MOAT ----------------

    moat = data["moat"]

    moat_content = f"""
STATUS

{moat["status"]}


COMPETITIVE ADVANTAGES

{moat["competitive_advantages"]}


BARRIERS TO ENTRY

{moat["barriers_to_entry"]}


PRICING POWER

{moat["pricing_power"]}


CUSTOMER STICKINESS

{moat["customer_stickiness"]}


MOAT DURABILITY

{moat["moat_durability"]}


SCORE

{moat["score"]}
"""

    create_text_tab(
        notebook,
        "Moat",
        "COMPETITIVE ADVANTAGE & MOAT",
        moat_content
    )


    # ---------------- FINANCIALS ----------------

    financials = data["financial_quality"]

    financial_content = f"""
STATUS

{financials["status"]}


REVENUE GROWTH

{financials["revenue_growth"]}


PROFIT GROWTH

{financials["profit_growth"]}


MARGINS

{financials["margins"]}


RETURN ON CAPITAL

{financials["return_on_capital"]}


CASH CONVERSION

{financials["cash_conversion"]}


BALANCE SHEET

{financials["balance_sheet"]}


SCORE

{financials["score"]}
"""

    create_text_tab(
        notebook,
        "Financials",
        "FINANCIAL QUALITY",
        financial_content
    )


    # ---------------- VALUATION ----------------

    valuation = data["valuation"]

    valuation_content = f"""
STATUS

{valuation["status"]}


CURRENT PRICE

{valuation["current_price"]}


FAIR VALUE

{valuation["fair_value"]}


MARGIN OF SAFETY

{valuation["margin_of_safety"]}


EXPECTED CAGR

{valuation["expected_cagr"]}


BEAR CASE

{valuation["bear_case"]}


BASE CASE

{valuation["base_case"]}


BULL CASE

{valuation["bull_case"]}
"""

    create_text_tab(
        notebook,
        "Valuation",
        "EIOS VALUATION ENGINE",
        valuation_content
    )


    # ---------------- RISKS ----------------

    risks = data["risks"]

    risks_content = f"""
BUSINESS RISKS

{risks["business_risks"]}


MANAGEMENT RISKS

{risks["management_risks"]}


FINANCIAL RISKS

{risks["financial_risks"]}


DISRUPTION RISKS

{risks["disruption_risks"]}


THESIS KILLERS

{risks["thesis_killers"]}
"""

    create_text_tab(
        notebook,
        "Risks",
        "RISK & CONTRADICTION ENGINE",
        risks_content
    )


    # ---------------- EVIDENCE REGISTER ----------------

    evidence = data["evidence_register"]

    evidence_content = f"""
ANNUAL REPORTS

{evidence["annual_reports"]}


CONFERENCE CALLS

{evidence["conference_calls"]}


INVESTOR PRESENTATIONS

{evidence["investor_presentations"]}


EXCHANGE FILINGS

{evidence["exchange_filings"]}


COMPETITOR EVIDENCE

{evidence["competitor_evidence"]}


EXTERNAL RESEARCH

{evidence["external_research"]}
"""

    create_text_tab(
        notebook,
        "Evidence Register",
        "EIOS EVIDENCE REGISTER",
        evidence_content
    )


    # ---------------- CONTRADICTION ENGINE ----------------

    contradiction = data["contradiction_engine"]

    contradiction_content = f"""
SUPPORTING EVIDENCE

{contradiction["supporting_evidence"]}


CONTRADICTORY EVIDENCE

{contradiction["contradictory_evidence"]}


UNRESOLVED QUESTIONS

{contradiction["unresolved_questions"]}
"""

    create_text_tab(
        notebook,
        "Contradictions",
        "EIOS CONTRADICTION ENGINE",
        contradiction_content
    )


    # ---------------- EIOS VERDICT ----------------

    committee = data["investment_committee"]

    verdict_content = f"""
BUSINESS QUALITY VOTE

{committee["business_quality_vote"]}


INVESTMENT TODAY VOTE

{committee["investment_today_vote"]}


PORTFOLIO FIT VOTE

{committee["portfolio_fit_vote"]}


REGRET TEST

{committee["regret_test"]}


FINAL CIO DECISION

{committee["final_cio_decision"]}
"""

    create_text_tab(
        notebook,
        "EIOS Verdict",
        "INVESTMENT COMMITTEE VERDICT",
        verdict_content
    )


# ==================================================
# COMPANY REGISTRY
# ==================================================

def company_registry():

    registry = tk.Toplevel(window)

    registry.title("EIOS Company Registry")

    registry.geometry("600x450")


    tk.Label(
        registry,
        text="EIOS Company Registry",
        font=("Arial", 22, "bold")
    ).pack(pady=30)


    tk.Button(
        registry,
        text="The Anup Engineering Limited",
        width=40,
        height=2,
        command=show_anup_dossier
    ).pack(pady=10)


# ==================================================
# MAIN DASHBOARD
# ==================================================

tk.Label(
    window,
    text="EIOS",
    font=("Arial", 36, "bold")
).pack(pady=(50, 5))


tk.Label(
    window,
    text="Everest Investment Operating System",
    font=("Arial", 18)
).pack(pady=(0, 10))


tk.Label(
    window,
    text="Evidence • Conviction • Valuation • Portfolio Discipline",
    font=("Arial", 11)
).pack(pady=(0, 35))


tk.Button(
    window,
    text="Company Registry",
    width=40,
    height=2,
    command=company_registry
).pack(pady=10)


tk.Button(
    window,
    text="Research Engine",
    width=40,
    height=2
).pack(pady=10)


tk.Button(
    window,
    text="Portfolio",
    width=40,
    height=2
).pack(pady=10)


tk.Button(
    window,
    text="Exit",
    width=40,
    command=window.destroy
).pack(pady=30)


# ==================================================
# START EIOS
# ==================================================

window.mainloop()
