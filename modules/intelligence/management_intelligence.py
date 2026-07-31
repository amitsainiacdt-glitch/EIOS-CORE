from .intelligence import Intelligence


class ManagementIntelligence:

    @staticmethod
    def build(research, confidence_result):

        return Intelligence(
            title="Management Analysis",
            category="Management",
            source_engine="ManagementEngine",
            conclusion="Management analysis completed successfully.",
            entity=research.dossier.company_name,
            confidence=confidence_result.confidence,

            evidence=[
                "Management assessment completed."
            ],

            assumptions=[
                "Management disclosures are accurate."
            ],

            reasoning=[
                "Management quality evaluated using predefined framework."
            ],

            tags=[
                "management"
            ],
        )