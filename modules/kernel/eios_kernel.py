"""
EIOS
Everest Investment Operating System

Kernel

Central execution kernel for EIOS.

Responsible for:
- Bootstrapping services
- Holding the service container
- Building application instances
"""

from modules.kernel.bootstrap import Bootstrap
from modules.kernel.application_builder import ApplicationBuilder


class EIOSKernel:
    """
    Central execution kernel.
    """

    def __init__(self):

        self.bootstrap = Bootstrap()
        self.container = None
        self.builder = ApplicationBuilder()

    # ==========================================================
    # Initialize
    # ==========================================================

    def initialize(self):

        self.container = self.bootstrap.initialize()

        return self

    # ==========================================================
    # Build Application
    # ==========================================================

    def build(self, company):

        return self.builder.build(company)

    # ==========================================================
    # Shared Services
    # ==========================================================

    @property
    def registry(self):

        return self.container.registry

    @property
    def decision_office(self):

        return self.container.decision_office