"""
EIOS Bootstrap
"""

from modules.kernel.service_container import ServiceContainer


class Bootstrap:

    def __init__(self):

        self.container = ServiceContainer()

    def initialize(self):

        print("=" * 60)
        print("BOOTSTRAPPING EIOS")
        print("=" * 60)

        return self.container
