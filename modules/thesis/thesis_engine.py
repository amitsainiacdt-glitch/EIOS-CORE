from modules.thesis.investment_thesis import InvestmentThesis
from modules.thesis.assumptions import Assumptions
from modules.thesis.supporting_evidence import SupportingEvidence
from modules.thesis.contradicting_evidence import ContradictingEvidence
from modules.thesis.kill_conditions import KillConditions
from modules.thesis.conviction_engine import ConvictionEngine
from modules.thesis.thesis_scorecard import ThesisScorecard


class ThesisEngine:

    def __init__(self, research):

        self.research = research

        self.investment_thesis = InvestmentThesis()
        self.assumptions = Assumptions()
        self.supporting_evidence = SupportingEvidence()
        self.contradicting_evidence = ContradictingEvidence()
        self.kill_conditions = KillConditions()
        self.conviction_engine = ConvictionEngine()
        self.scorecard = ThesisScorecard()

    def analyze(self):

        print("\nStarting Thesis Analysis...")

        dossier = self.research.dossier

        thesis = self.investment_thesis.build(dossier)

        assumptions = self.assumptions.build(dossier)

        supporting = self.supporting_evidence.build(dossier)

        contradicting = self.contradicting_evidence.build(dossier)

        kill_conditions = self.kill_conditions.build(dossier)

        conviction = self.conviction_engine.calculate(
            thesis,
            assumptions,
            supporting,
            contradicting,
            kill_conditions
        )

        thesis_summary = self.scorecard.build(
            thesis,
            assumptions,
            supporting,
            contradicting,
            conviction
        )

        self.research.update_thesis(thesis_summary)

        print("Thesis Analysis Completed")