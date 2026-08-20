"""
EIOS
Everest Investment Operating System

Research Runtime
================

Production composition boundary for scheduled external research.

Responsibilities:
    - Construct the external research stack.
    - Load persistent observation state.
    - Connect Tavily to the existing orchestrator.
    - Connect ObservationRegistry to ObservationEngine.
    - Connect external observations to ResearchContext.
    - Execute one scheduled research cycle.
    - Persist observations after execution.
    - Record execution telemetry.
    - Optionally compare new observations with pre-cycle history.

Does NOT:
    - implement scheduling logic.
    - perform searches directly.
    - perform HTTP retrieval directly.
    - create Evidence.
    - create Signals.
    - score Opportunities.
    - perform investment analysis.
    - run infinite loops.
    - publish historical comparisons downstream.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from time import perf_counter

from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
)

from modules.external_intelligence.external_intelligence_adapter import (
    ExternalIntelligenceAdapter,
)

from modules.external_intelligence.research_execution_log import (
    ResearchExecutionLog,
)

from modules.external_intelligence.research_execution_logger import (
    ResearchExecutionLogger,
)

from modules.external_intelligence.research_execution_service import (
    ResearchExecutionService,
)

from modules.external_intelligence.research_job_registry import (
    ResearchJobRegistry,
)

from modules.external_intelligence.research_scheduler import (
    ResearchScheduler,
)

from modules.external_intelligence.research_runtime_controller import (
    ResearchRuntimeController,
)

from modules.external_intelligence.runtime_historical_comparison import (
    RuntimeHistoricalComparison,
)

from modules.external_intelligence.scheduled_research_runner import (
    ScheduledResearchRunner,
)

from modules.external_intelligence.tavily_search_provider import (
    TavilySearchProvider,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.observation.observation_persistence import (
    ObservationPersistence,
)

from modules.observation.observation_registry import (
    ObservationRegistry,
)

from modules.research_context.research_context import (
    ResearchContext,
)


class ResearchRuntime:
    """
    Composes the complete EIOS external research runtime.

    The runtime executes one cycle at a time.

    A future operating-system scheduler may invoke
    run_once() periodically.
    """

    def __init__(
        self,
        *,
        observation_path: str | Path = "data/observations.json",
        tavily_api_key: str | None = None,
        context: ResearchContext | None = None,
        enable_historical_comparison: bool = False,
    ) -> None:

        self.historical_comparison_enabled = bool(
            enable_historical_comparison
        )

        self._historical_comparison_results: list[
            RuntimeHistoricalComparison
        ] = []

        # ==================================================
        # RESEARCH CONTEXT
        # ==================================================

        self.context = (
            context
            if context is not None
            else ResearchContext()
        )

        # ==================================================
        # EXECUTION LOGGER
        # ==================================================

        self.execution_logger = (
            ResearchExecutionLogger()
        )

        # ==================================================
        # PERSISTENCE
        # ==================================================

        self.persistence = ObservationPersistence(
            observation_path
        )

        # ==================================================
        # OBSERVATION REGISTRY
        # ==================================================

        self.observation_registry = (
            ObservationRegistry()
        )

        # ==================================================
        # OBSERVATION ENGINE
        # ==================================================

        self.observation_engine = (
            ObservationEngine(
                registry=self.observation_registry,
                persistence=self.persistence,
            )
        )

        # ==================================================
        # EXTERNAL INTELLIGENCE ADAPTER
        # ==================================================

        self.external_intelligence_adapter = (
            ExternalIntelligenceAdapter(
                self.context
            )
        )

        # ==================================================
        # TAVILY PROVIDER
        # ==================================================

        self.provider = TavilySearchProvider(
            api_key=tavily_api_key
        )

        if not self.provider.configured:

            raise RuntimeError(
                "TAVILY_API_KEY is not configured"
            )

        # ==================================================
        # EXTERNAL RESEARCH ORCHESTRATOR
        # ==================================================

        self.orchestrator = (
            ExternalResearchOrchestrator(
                provider=self.provider,
                observation_engine=(
                    self.observation_engine
                ),
            )
        )

        # ==================================================
        # RESEARCH EXECUTION
        # ==================================================

        self.scheduler = ResearchScheduler()

        self.registry = ResearchJobRegistry()

        self.execution_service = (
            ResearchExecutionService(
                orchestrator=self.orchestrator,
                scheduler=self.scheduler,
            )
        )

        # ==================================================
        # SCHEDULED RUNNER
        # ==================================================

        self.runner = ScheduledResearchRunner(
            registry=self.registry,
            scheduler=self.scheduler,
            execution_service=self.execution_service,
        )

        # ==================================================
        # RUNTIME CONTROLLER
        # ==================================================

        self.controller = (
            ResearchRuntimeController(
                self.runner
            )
        )

    # ======================================================
    # REGISTER JOB
    # ======================================================

    def register_job(
        self,
        job,
    ) -> None:
        """
        Register one ResearchJob with both the job registry
        and scheduling registry.
        """

        self.registry.add(
            job
        )

        self.scheduler.register(
            job
        )

    # ======================================================
    # RUN ONCE
    # ======================================================

    def run_once(
        self,
        now: datetime,
    ):
        """
        Execute one complete scheduled research cycle.

        Execution telemetry is recorded for every cycle.

        Newly created external observations are published
        through the existing ResearchContext intelligence bus.

        Observations are persisted after execution.
        """

        start_time = perf_counter()

        observations_before = (
            self.observation_registry.count()
        )

        historical_observations = tuple(
            self.observation_registry.all()
        )

        failures = 0

        result = None

        status = "SUCCESS"

        try:

            # --------------------------------------------------
            # EXECUTE SCHEDULED RESEARCH
            # --------------------------------------------------

            result = self.controller.run_once(
                now
            )

            # --------------------------------------------------
            # EXTERNAL OBSERVATION → INTELLIGENCE
            # --------------------------------------------------
            #
            # The ResearchExecutionService returns execution
            # results from the ExternalResearchOrchestrator.
            #
            # ResearchRuntime is the composition boundary that
            # connects externally created Observations to the
            # existing ResearchContext / IntelligenceMesh.
            # --------------------------------------------------

            for execution_result in result.results:

                if execution_result is None:
                    continue

                observations = getattr(
                    execution_result,
                    "observations",
                    [],
                )

                for observation in observations:

                    if observation is None:
                        continue

                    if self.historical_comparison_enabled:
                        self._historical_comparison_results.append(
                            self._compare_with_history(
                                observation,
                                historical_observations,
                            )
                        )

                    self.external_intelligence_adapter.publish(
                        observation
                    )

                # --------------------------------------------------
                # EXECUTION FAILURE STATUS
                # --------------------------------------------------

                execution_status = getattr(
                    execution_result,
                    "status",
                    None,
                )

                if execution_status in (
                    "FAILED",
                    "FAILURE",
                    "PARTIAL_FAILURE",
                ):
                    failures += 1

            if failures > 0:

                status = "PARTIAL_FAILURE"

            # --------------------------------------------------
            # PERSIST OBSERVATION STATE
            # --------------------------------------------------

            self.persistence.save(
                self.observation_registry.all()
            )

        except Exception:

            failures += 1

            status = "PARTIAL_FAILURE"

            # Preserve normal exception semantics.

            raise

        finally:

            # --------------------------------------------------
            # EXECUTION TELEMETRY
            # --------------------------------------------------

            observations_after = (
                self.observation_registry.count()
            )

            # --------------------------------------------------
            # RESEARCH CONTEXT RUNTIME STATE
            # --------------------------------------------------
            #
            # Publish lightweight runtime telemetry through
            # the existing ResearchContext boundary.
            #
            # This is state/telemetry only.
            # It performs no analysis.
            # --------------------------------------------------

            self.context.set_runtime(
                "last_external_research_run",
                now,
            )

            self.context.set_runtime(
                "last_external_observations_after",
                observations_after,
            )

            observations_created = max(
                0,
                observations_after
                - observations_before,
            )

            duration_seconds = (
                perf_counter()
                - start_time
            )

            jobs_due = (
                len(result.due_jobs)
                if result is not None
                else 0
            )

            jobs_executed = (
                len(result.executed_jobs)
                if result is not None
                else 0
            )

            execution_log = ResearchExecutionLog(
                run_time=now,
                status=status,
                jobs_due=jobs_due,
                jobs_executed=jobs_executed,
                observations_before=(
                    observations_before
                ),
                observations_after=(
                    observations_after
                ),
                observations_created=(
                    observations_created
                ),
                failures=failures,
                duration_seconds=(
                    duration_seconds
                ),
            )

            self.execution_logger.record(
                execution_log
            )

        # ------------------------------------------------------
        # PRESERVE RUNTIME RESULT CONTRACT
        # ------------------------------------------------------

        return result

    # ======================================================
    # HISTORICAL COMPARISON
    # ======================================================

    def _compare_with_history(
        self,
        current_observation,
        historical_observations,
    ) -> RuntimeHistoricalComparison:
        """
        Select and compare against the pre-cycle history snapshot.
        """

        selection = (
            self.observation_engine
            .historical_observation_selector
            .select(
                current_observation=current_observation,
                observations=historical_observations,
            )
        )

        comparison = None

        if selection.selected_observation is not None:
            comparison = self.observation_engine.compare_historical(
                current_observation=current_observation,
                historical_observation=(
                    selection.selected_observation
                ),
            )

        return RuntimeHistoricalComparison(
            current_observation=current_observation,
            selection=selection,
            comparison=comparison,
        )

    def historical_comparisons(
        self,
    ) -> list[RuntimeHistoricalComparison]:
        """
        Return a copy of all opt-in runtime comparison results.
        """

        return list(
            self._historical_comparison_results
        )

    def historical_comparison_count(
        self,
    ) -> int:
        """Return the number of preserved runtime comparison results."""

        return len(
            self._historical_comparison_results
        )

    # ======================================================
    # OBSERVATIONS
    # ======================================================

    def observations(
        self,
    ):

        return (
            self.observation_registry.all()
        )

    def observation_count(
        self,
    ) -> int:

        return (
            self.observation_registry.count()
        )

    # ======================================================
    # INTELLIGENCE
    # ======================================================

    def intelligence(
        self,
    ):

        return (
            self.context
            .get_intelligence_mesh()
            .get_all()
        )

    def intelligence_count(
        self,
    ) -> int:

        return (
            self.context
            .get_intelligence_mesh()
            .count()
        )

    # ======================================================
    # EXECUTION LOGGING
    # ======================================================

    def execution_logs(
        self,
    ) -> list[ResearchExecutionLog]:
        """
        Return all runtime execution logs.

        A copy is returned so callers cannot mutate the
        logger's internal collection.
        """

        return (
            self.execution_logger.all()
        )

    def execution_log_count(
        self,
    ) -> int:
        """
        Return the number of recorded runtime executions.
        """

        return (
            self.execution_logger.count()
        )

    def latest_execution_log(
        self,
    ) -> ResearchExecutionLog | None:
        """
        Return the latest execution log.
        """

        return (
            self.execution_logger.latest()
        )


__all__ = [
    "ResearchRuntime",
]
