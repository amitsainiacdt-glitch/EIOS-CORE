from modules.research.kill_switch import KillSwitchEngine
from modules.research.question_engine import QuestionEngine


class ResearchPipeline:

    def __init__(self):

        self.kill_switch = KillSwitchEngine()

        self.question_engine = QuestionEngine()

    def execute(self):

        print("\n")
        print("=" * 60)
        print("RESEARCH PIPELINE")
        print("=" * 60)

        result = self.kill_switch.evaluate(
            tam=True,
            moat=True,
            management=True,
            financial_quality=True,
            customer_concentration=True
        )

        if not result.passed:

            print("\nResearch Stopped")
            print(result.failed_checks)

            return False

        print("Kill Switch : PASS")

        self.question_engine.add(
            "Is the business easy to understand?",
            10
        )

        self.question_engine.add(
            "Does it have pricing power?",
            15
        )

        self.question_engine.add(
            "Does it have a durable moat?",
            20
        )

        self.question_engine.show()

        print()

        print(
            f"Business Quality Weight : {self.question_engine.total_weight()}"
        )

        return True