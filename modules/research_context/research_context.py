"""
EIOS
Research Context

Central shared runtime context for all analytical engines.

The ResearchContext acts as the single source of truth for
all shared research state during an analysis session.

Release 18.0
"""

from datetime import datetime


class ResearchContext:
    """
    Shared runtime context for the entire EIOS pipeline.
    """

    def __init__(self):

        # ----------------------------
        # Core Research Objects
        # ----------------------------

        self.master_dossier = None

        self.evidence_library = []

        self.knowledge_base = []

        self.observations = []

        self.assumptions = []

        # ----------------------------
        # External Intelligence
        # ----------------------------

        self.internet_cache = {}

        # ----------------------------
        # Runtime
        # ----------------------------

        self.runtime_state = {}

        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "release": "18.0",
            "version": "ResearchContext-1.0",
        }

    # -------------------------------------------------
    # Master Dossier
    # -------------------------------------------------

    def set_master_dossier(self, dossier):
        self.master_dossier = dossier

    def get_master_dossier(self):
        return self.master_dossier

    # -------------------------------------------------
    # Evidence
    # -------------------------------------------------

    def add_evidence(self, evidence):
        self.evidence_library.append(evidence)

    def get_evidence(self):
        return self.evidence_library

    # -------------------------------------------------
    # Observations
    # -------------------------------------------------

    def add_observation(self, observation):
        self.observations.append(observation)

    def get_observations(self):
        return self.observations

    # -------------------------------------------------
    # Assumptions
    # -------------------------------------------------

    def add_assumption(self, assumption):
        self.assumptions.append(assumption)

    def get_assumptions(self):
        return self.assumptions

    # -------------------------------------------------
    # Knowledge
    # -------------------------------------------------

    def add_knowledge(self, knowledge):
        self.knowledge_base.append(knowledge)

    def get_knowledge(self):
        return self.knowledge_base

    # -------------------------------------------------
    # Internet Cache
    # -------------------------------------------------

    def cache(self, key, value):
        self.internet_cache[key] = value

    def get_cache(self, key, default=None):
        return self.internet_cache.get(key, default)

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    def set_runtime(self, key, value):
        self.runtime_state[key] = value

    def get_runtime(self, key, default=None):
        return self.runtime_state.get(key, default)