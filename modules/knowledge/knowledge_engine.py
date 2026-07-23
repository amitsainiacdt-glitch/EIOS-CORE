"""
Knowledge Engine

Creates structured knowledge from validated evidence.
"""

from .knowledge import Knowledge
from .knowledge_registry import KnowledgeRegistry


class KnowledgeEngine:
    """
    Converts Evidence into Knowledge.
    """

    def __init__(self):

        self.registry = KnowledgeRegistry()

    def create_knowledge(
        self,
        title,
       category,
        description,
        confidence=100,
        evidence=None,
        tags=None
    ):

        knowledge = Knowledge(
            title=title,
            category=category,
            description=description,
            confidence=confidence
        )

        if evidence:

            if not isinstance(evidence, list):
                evidence = [evidence]

            for item in evidence:
                knowledge.add_evidence(item)

        if tags:
            for tag in tags:
                knowledge.add_tag(tag)

        self.registry.add(knowledge)

        return knowledge

    def create_from_evidence(self, evidence):
        """
        Automatically create Knowledge from Evidence.
        """

        knowledge = Knowledge(
            title=evidence.title,
            category=evidence.category,
            description=evidence.description,
            confidence=evidence.confidence
        )

        knowledge.add_evidence(evidence)

        self.registry.add(knowledge)

        return knowledge

    def show_knowledge(self):

        self.registry.show_knowledge()

    def count(self):

        return self.registry.count()

    def all(self):

        return self.registry.all()