"""
EIOS
Everest Investment Operating System

Valuation Registry

Purpose:
Central registry for all valuation engines.

Every valuation engine registers itself here.
The Valuation Engine executes the registry rather than
hardcoding valuation methods.
"""


class ValuationRegistry:
    """
    Registry of valuation engines.
    """

    def __init__(self):
        self._engines = []

    def register(self, engine):
        """
        Register a valuation engine.

        Duplicate engine classes are ignored.
        """

        for existing in self._engines:
            if type(existing) is type(engine):
                return

        self._engines.append(engine)

    def unregister(self, engine_type):
        """
        Remove a valuation engine by class.
        """

        self._engines = [
            engine
            for engine in self._engines
            if not isinstance(engine, engine_type)
        ]

    def clear(self):
        """
        Remove all registered engines.
        """

        self._engines.clear()

    def get_engines(self):
        """
        Return registered valuation engines.
        """

        return list(self._engines)

    def __iter__(self):
        """
        Allow:

            for engine in registry
        """

        return iter(self._engines)

    def __len__(self):
        return len(self._engines)