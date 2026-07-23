class ThesisScorecard:

    def build(
        self,
        thesis,
        assumptions,
        supporting_evidence,
        contradicting_evidence,
        conviction
    ):

        return {
            "Investment Thesis":
                thesis,

            "Assumptions":
                assumptions,

            "Supporting Evidence":
                supporting_evidence,

            "Contradicting Evidence":
                contradicting_evidence,

            "Conviction":
                conviction,

            "Overall Rating":
                conviction["Rating"],

            "Overall Score":
                conviction["Conviction Score"],

            "Confidence":
                conviction["Confidence"]
        }