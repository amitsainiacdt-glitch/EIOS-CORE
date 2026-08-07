"""
EIOS
Service Container

Central dependency container.
"""

from modules.company.company_registry import CompanyRegistry
from modules.decision.decision_office import DecisionOffice


class ServiceContainer:

    def __init__(self):

        self._registry = CompanyRegistry()
        self._decision_office = DecisionOffice()

    @property
    def registry(self):
        return self._registry

    @property
    def decision_office(self):
        return self._decision_office
