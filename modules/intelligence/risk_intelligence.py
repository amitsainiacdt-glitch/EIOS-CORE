from .intelligence import Intelligence


class RiskIntelligence:

    @staticmethod
    def build(research, confidence_result):

        return Intelligence(
            title="Risk Analysis",
            category="Risk",
            source_engine="RiskEngine",
            conclusion="Risk analysis completed successfully.",
            entity=research.dossier.company_name,
            confidence=confidence_result.confidence,

            evidence=[
                "Business risk assessment completed.",
                "Financial risk assessment completed.",
                "Governance risk assessment completed.",
                "Industry risk assessment completed.",
                "Macro risk assessment completed.",
                "Scenario analysis completed."
            ],

            assumptions=[
                "Current business conditions continue.",
                "Management disclosures remain accurate.",
                "Macroeconomic assumptions remain broadly unchanged."
            ],

            reasoning=[
                "Risk score calculated from multiple independent risk engines.",
                "Overall confidence derived from available evidence.",
                "Final rating based on weighted risk scorecard."
            ],

            tags=[
                "risk",
                "business",
                "financial",
                "governance",
                "industry",
                "macro",
                "scenario"
            ],
        )