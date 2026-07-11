def analyse_financial_quality(company):

    score = 0

    # ROCE
    if company["financials"]["roce"] >= 20:
        score += 2
    elif company["financials"]["roce"] >= 15:
        score += 1

    # Debt
    if company["financials"]["debt_equity"] <= 0.5:
        score += 2
    elif company["financials"]["debt_equity"] <= 1:
        score += 1

    # Revenue Growth
    if company["financials"]["sales_growth"] >= 15:
        score += 2
    elif company["financials"]["sales_growth"] >= 10:
        score += 1

    # Profit Growth
    if company["financials"]["profit_growth"] >= 15:
        score += 2
    elif company["financials"]["profit_growth"] >= 10:
        score += 1

    # Cash Flow
    if company["financials"]["cashflow_positive"]:
        score += 2

    if score >= 9:
        return "A"

    elif score >= 7:
        return "B"

    elif score >= 5:
        return "C"

    else:
        return "D"