from .reasoning import Reasoning
from .reasoning_registry import ReasoningRegistry
from .reasoning_rules import REASONING_RULES


class ReasoningEngine:

    def __init__(self):
        self.registry = ReasoningRegistry()

    def initialize(self):
        print("Reasoning Engine Initialized")

    def reason(
        self,
        title: str,
        conclusion: str,
        evidence=None,
        assumptions=None,
        confidence="UNKNOWN",
        metadata=None,
    ):

        reasoning = Reasoning(
            title=title,
            conclusion=conclusion,
            evidence=evidence or [],
            assumptions=assumptions or [],
            confidence=confidence,
            metadata=metadata or {},
        )

        self.registry.register(reasoning)

        return reasoning

    def create_from_knowledge(self, knowledge):

        implications = []

        for keyword, rules in REASONING_RULES.items():

            if keyword.lower() in knowledge.title.lower():
                implications.extend(rules)

            elif keyword.lower() in knowledge.description.lower():
                implications.extend(rules)

        return self.reason(
            title=knowledge.title,
            conclusion=knowledge.description,
            evidence=knowledge.source_evidence,
            assumptions=implications,
            confidence=f"{knowledge.confidence:.0f}%",
            metadata={
                "category": knowledge.category,
                "tags": knowledge.tags,
                "generated_from": "Knowledge",
            },
        )

    def get(self, title):
        return self.registry.get(title)

    def all(self):
        return self.registry.all()

    def count(self):
        return self.registry.count()

    def clear(self):
        self.registry.clear()

    def show_reasoning(self):

        print("=" * 60)
        print("REASONING")
        print("=" * 60)

        if self.count() == 0:
            print("No reasoning available.")
            return

        for reasoning in self.all():

            print(f"Title       : {reasoning.title}")
            print(f"Conclusion  : {reasoning.conclusion}")
            print(f"Confidence  : {reasoning.confidence}")

            if reasoning.evidence:
                print("Evidence")
                for item in reasoning.evidence:
                    print(f"  - {item}")

            if reasoning.assumptions:
                print("Assumptions")
                for item in reasoning.assumptions:
                    print(f"  - {item}")

            print("-" * 60)