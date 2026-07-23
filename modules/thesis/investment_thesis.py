class InvestmentThesis:

    def build(self, dossier):

        business_quality = dossier.business_quality
        financials = dossier.financials
        management = dossier.management
        valuation = dossier.valuation
        competitive = dossier.competitive

        business_summary = (
            f"{dossier.company_name} operates in the "
            f"{dossier.industry} industry."
        )

        investment_thesis = (
            "The company demonstrates attractive business "
            "fundamentals based on completed EIOS research."
        )

        long_term_drivers = [
            "Business Quality",
            "Financial Strength",
            "Competitive Position",
            "Management Execution",
            "Capital Allocation"
        ]

        competitive_advantage = (
            business_quality.get(
                "Competitive Advantage",
                "Under Evaluation"
            )
            if isinstance(business_quality, dict)
            else "Under Evaluation"
        )

        expected_outcome = (
            "Potential Long-term Compounder"
        )

        time_horizon = "5-10 Years"

        return {

            "Business Summary":
                business_summary,

            "Investment Thesis":
                investment_thesis,

            "Long-term Drivers":
                long_term_drivers,

            "Competitive Advantage":
                competitive_advantage,

            "Expected Outcome":
                expected_outcome,

            "Time Horizon":
                time_horizon,

            "Supporting Modules": {
                "Business Quality": bool(business_quality),
                "Financial Analysis": bool(financials),
                "Management Analysis": bool(management),
                "Competitive Analysis": bool(competitive),
                "Valuation": bool(valuation)
            },

            "Confidence":
                60
        }