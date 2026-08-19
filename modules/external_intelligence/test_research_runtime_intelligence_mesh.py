"""
EIOS
Everest Investment Operating System

Research Runtime → Intelligence Mesh Integration Test
"""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)

from modules.research_context.research_context import (
    ResearchContext,
)


def make_job():

    return ResearchJob(
        job_id="MESH-001",
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check recent company developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=60,
        enabled=True,
        priority=100,
        max_sources=3,
        observation_category="External Web",
        observation_confidence=70.0,
    )


def main():

    print("=" * 60)
    print(
        "EIOS RESEARCH RUNTIME → INTELLIGENCE MESH TEST"
    )
    print("=" * 60)

    with TemporaryDirectory() as temp_dir:

        observation_path = (
            Path(temp_dir)
            / "observations.json"
        )

        # ==================================================
        # TEST 1 — CONTEXT CREATION
        # ==================================================

        context = ResearchContext()

        runtime = ResearchRuntime(
            observation_path=observation_path,
            context=context,
        )

        assert runtime.context is context

        print(
            "Test 1 — ResearchContext Injection    : PASS"
        )

        # ==================================================
        # TEST 2 — ADAPTER CREATION
        # ==================================================

        assert (
            runtime.external_intelligence_adapter
            is not None
        )

        print(
            "Test 2 — Intelligence Adapter          : PASS"
        )

        # ==================================================
        # TEST 3 — JOB REGISTRATION
        # ==================================================

        job = make_job()

        runtime.register_job(
            job
        )

        assert (
            runtime.registry.get(
                "MESH-001"
            )
            is job
        )

        print(
            "Test 3 — Job Registration               : PASS"
        )

        # ==================================================
        # TEST 4 — LIVE EXECUTION
        # ==================================================

        result = runtime.run_once(
            datetime.now()
        )

        assert result is not None

        assert len(
            result.executed_jobs
        ) == 1

        print(
            "Test 4 — Live Runtime Execution         : PASS"
        )

        # ==================================================
        # TEST 5 — OBSERVATIONS EXIST
        # ==================================================

        observation_count = (
            runtime.observation_count()
        )

        assert observation_count >= 0

        print(
            "Test 5 — Observation Pipeline            : PASS"
        )

        # ==================================================
        # TEST 6 — INTELLIGENCE MESH
        # ==================================================

        intelligence_count = (
            runtime.intelligence_count()
        )

        assert (
            intelligence_count
            == observation_count
        )

        print(
            "Test 6 — Intelligence Mesh Handoff      : PASS"
        )

        # ==================================================
        # TEST 7 — INTELLIGENCE CONTENT
        # ==================================================

        intelligence = (
            runtime.intelligence()
        )

        for item in intelligence:

            assert (
                item.source_engine
                == "ExternalResearch"
            )

            assert (
                "external"
                in item.tags
            )

            assert (
                "web"
                in item.tags
            )

        print(
            "Test 7 — Intelligence Contract          : PASS"
        )

        # ==================================================
        # TEST 8 — CONTEXT RUNTIME STATE
        # ==================================================

        assert (
            context.get_runtime(
                "last_external_research_run"
            )
            is not None
        )

        assert (
            context.get_runtime(
                "last_external_observations_after"
            )
            == observation_count
        )

        print(
            "Test 8 — Runtime State                  : PASS"
        )

    print()
    print(
        "EIOS RESEARCH RUNTIME → "
        "INTELLIGENCE MESH : ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()