class ContradictingEvidence:

    def build(self, dossier):

        risks = dossier.risks if dossier.risks else []

        return {

            "Business Risks":
                risks,

            "Financial Risks":
                [],

            "Management Concerns":
                [],

            "Competitive Threats":
                [],

            "Industry Risks":
                [],

            "Macro Risks":
                [],

            "Bear Case":
                "Further evidence required to invalidate thesis.",

            "Confidence":
                60
        }