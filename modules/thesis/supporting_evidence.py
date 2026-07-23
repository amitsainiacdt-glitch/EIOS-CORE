class SupportingEvidence:

    def build(self, dossier):

        evidence = []

        if dossier.business_quality:
            evidence.append(
                "Business Quality analysis completed successfully."
            )

        if dossier.financials:
            evidence.append(
                "Financial analysis supports the investment case."
            )

        if dossier.management:
            evidence.append(
                "Management assessment completed."
            )

        if dossier.competitive:
            evidence.append(
                "Competitive intelligence completed."
            )

        if dossier.valuation:
            evidence.append(
                "Valuation analysis available."
            )

        return {

            "Financial Evidence": [
                "Financial Engine completed."
            ] if dossier.financials else [],

            "Business Evidence": [
                "Business Quality Engine completed."
            ] if dossier.business_quality else [],

            "Management Evidence": [
                "Management Engine completed."
            ] if dossier.management else [],

            "Competitive Evidence": [
                "Competitive Intelligence completed."
            ] if dossier.competitive else [],

            "Industry Evidence": evidence,

            "Macro Evidence": [],

            "Evidence Strength":
                "Strong" if len(evidence) >= 4 else "Moderate",

            "Confidence":
                60
        }