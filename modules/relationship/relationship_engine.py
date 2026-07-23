"""
Relationship Engine

Creates and manages relationships inside EIOS.
"""

from .relationship import Relationship
from .relationship_registry import RelationshipRegistry


class RelationshipEngine:
    """
    Creates and manages relationships.
    """

    def __init__(self):

        self.registry = RelationshipRegistry()

    def create_relationship(
        self,
        source,
        relationship_type,
        target,
        confidence=100,
        description="",
        evidence=None
    ):

        relationship = Relationship(
            source=source,
            relationship_type=relationship_type,
            target=target,
            confidence=confidence,
            description=description
        )

        if evidence:

            if not isinstance(evidence, list):
                evidence = [evidence]

            for item in evidence:
                relationship.add_evidence(item)

        self.registry.add(relationship)

        return relationship

    def show_relationships(self):

        self.registry.show_relationships()

    def count(self):

        return self.registry.count()

    def all(self):

        return self.registry.all()