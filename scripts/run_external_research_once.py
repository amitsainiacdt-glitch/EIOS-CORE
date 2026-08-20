"""Validate or explicitly execute one external-research runtime cycle."""

from __future__ import annotations

import argparse

from modules.external_intelligence.research_runtime_bootstrap import (
    ResearchRuntimeBootstrap,
    ResearchRuntimeBootstrapConfig,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate EIOS external-research configuration. "
            "Use --execute to perform one live cycle."
        )
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform one live external-research cycle.",
    )
    return parser


def main(
    argv=None,
    *,
    bootstrap_factory=ResearchRuntimeBootstrap,
    config_factory=(
        ResearchRuntimeBootstrapConfig.from_environment
    ),
) -> int:
    args = build_parser().parse_args(argv)
    config = config_factory()
    bootstrap = bootstrap_factory(config)
    validation = bootstrap.validate()

    print("EIOS EXTERNAL RESEARCH RUNTIME")
    print(f"Ready: {validation.ready}")
    print(f"Jobs: {validation.job_count}")
    print(f"Observation path: {validation.observation_path}")
    print(
        "Historical comparison: "
        f"{validation.historical_comparison_enabled}"
    )
    print(
        "Historical comparison audit: "
        f"{validation.historical_comparison_audit_enabled}"
    )
    if validation.historical_comparison_audit_path is not None:
        print(
            "Historical comparison audit path: "
            f"{validation.historical_comparison_audit_path}"
        )

    if validation.errors:
        for error in validation.errors:
            print(f"Configuration error: {error}")
        return 1

    if not args.execute:
        print("Validation only. No external API calls were made.")
        return 0

    runtime, result = bootstrap.run_once()

    print(
        "Executed jobs: "
        f"{len(result.executed_jobs)}"
    )
    print(
        "Observations stored: "
        f"{runtime.observation_count()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
