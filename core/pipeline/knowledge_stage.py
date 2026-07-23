"""
Knowledge Pipeline Stage

Converts validated Evidence into Knowledge.
"""

from modules.knowledge.knowledge_engine import KnowledgeEngine


class KnowledgeStage:
    """
    Pipeline stage responsible for creating Knowledge
    from validated Evidence.
    """

    def __init__(self):

        self.engine = KnowledgeEngine()

    def execute(self, context):

        if context.evidence is None:
            return context

        knowledge = self.engine.create_from_evidence(
            context.evidence
        )

        context.knowledge = knowledge

        return context