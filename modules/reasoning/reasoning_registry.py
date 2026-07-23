from typing import Dict, List

from .reasoning import Reasoning


class ReasoningRegistry:

    def __init__(self):
        self._reasonings: Dict[str, Reasoning] = {}

    def register(self, reasoning: Reasoning):
        self._reasonings[reasoning.title] = reasoning

    def get(self, title: str):
        return self._reasonings.get(title)

    def all(self) -> List[Reasoning]:
        return list(self._reasonings.values())

    def exists(self, title: str) -> bool:
        return title in self._reasonings

    def remove(self, title: str):
        self._reasonings.pop(title, None)

    def clear(self):
        self._reasonings.clear()

    def count(self):
        return len(self._reasonings)