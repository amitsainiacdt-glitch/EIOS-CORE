from enum import Enum

from modules.research.company_research import CompanyResearch


class ResearchStage(Enum):
    BUSINESS_QUALITY = "Business Quality"
    MANAGEMENT = "Management"
    FINANCIALS = "Financial Quality"
    VALUATION = "Valuation"
    RISK = "Risk Analysis"


class StageEngine:

    def __init__(self, researcher: CompanyResearch):
        self.researcher = researcher
        self.current_stage = ResearchStage.BUSINESS_QUALITY

    def run_current_stage(self):

        print(f"Running {self.current_stage.value}")

    def next_stage(self):

        stages = list(ResearchStage)

        index = stages.index(self.current_stage)

        if index < len(stages) - 1:
            self.current_stage = stages[index + 1]
            return self.current_stage

        return None

    def reset(self):

        self.current_stage = ResearchStage.BUSINESS_QUALITY