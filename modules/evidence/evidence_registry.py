"""
Evidence Registry

Stores all evidence collected by EIOS.
"""

from .evidence import Evidence


class EvidenceRegistry:

    def __init__(self):

        self._evidence = []

    def add(self, evidence: Evidence):

        self._evidence.append(evidence)

    def all(self):

        return self._evidence

    def count(self):

        return len(self._evidence)

    def latest(self):

        if self._evidence:
            return self._evidence[-1]
        return None

    def clear(self):

        self._evidence.clear()