"""
Relationship Registry

Stores all relationships created by EIOS.
"""


class RelationshipRegistry:
    """
    Registry for all relationship objects.
    """

    def __init__(self):

        self._relationships = []

    def add(self, relationship):

        self._relationships.append(relationship)

    def all(self):

        return self._relationships

    def count(self):

        return len(self._relationships)

    def clear(self):

        self._relationships.clear()

    def show_relationships(self):

        print("=" * 60)
        print("RELATIONSHIPS")
        print("=" * 60)

        if not self._relationships:
            print("No relationships available.")
            return

        for relationship in self._relationships:
            print(relationship.summary())

        print()
        print(f"Total Relationships : {self.count()}")