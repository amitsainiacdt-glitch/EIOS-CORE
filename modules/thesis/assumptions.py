class Assumptions:

    def build(self, dossier):

        assumptions = []

        # Business Quality
        if dossier.business_quality:
            assumptions.append(
                "Business quality remains intact."
            )

        # Financials
        if dossier.financials:
            assumptions.append(
                "Financial performance continues to support long-term growth."
            )

        # Management
        if dossier.management:
            assumptions.append(
                "Management continues disciplined capital allocation."
            )

        # Competitive Position
        if dossier.competitive:
            assumptions.append(
                "Competitive position remains sustainable."
            )

        # Valuation
        if dossier.valuation:
            assumptions.append(
                "Current valuation supports long-term investment returns."
            )

        return {

            "Key Assumptions": assumptions,

            "Business Assumptions": [
                "Business model remains durable."
            ],

            "Financial Assumptions": [
                "Revenue and earnings continue to grow."
            ],

            "Management Assumptions": [
                "Governance standards remain strong."
            ],

            "Industry Assumptions": [
                "Industry demand remains healthy."
            ],

            "Macro Assumptions": [
                "Macroeconomic environment remains supportive."
            ],

            "Confidence": 60
        }