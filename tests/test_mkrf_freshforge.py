from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from mkrf_freshforge import MkrfFreshForgeProvider, provider_factory

freshforge = pytest.importorskip("freshforge")

WORKFLOW_PATH = Path("workflows/freshforge/mkrf_model_build_workflow.yaml")
EXPECTED_MODEL_BUILD_ORDER = [
    "validate_case",
    "geospatial_preflight",
    "build_au_inputs",
    "select_aus",
    "build_managed_au_inputs",
    "build_managed_au_curves",
    "init_runtime_package",
    "patchworks_preflight",
    "matrix_build",
]


def _successful_runner(commands: list[tuple[str, ...]]):
    def _run(command: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(
            args=list(command),
            returncode=0,
            stdout="ok",
            stderr="",
        )

    return _run


def _registry_with_femic_and_mkrf():
    from femic.freshforge import provider_factory as femic_provider_factory
    from freshforge.providers import ProviderRegistry

    registry = ProviderRegistry()
    registry.register(femic_provider_factory())
    registry.register(provider_factory())
    return registry


def test_provider_metadata_serializes_deterministically() -> None:
    metadata = provider_factory().metadata()

    assert metadata.id == "mkrf"
    assert [node_type.id for node_type in metadata.node_types] == [
        "build_au_inputs",
        "select_aus",
        "build_managed_au_inputs",
        "build_managed_au_curves",
        "init_runtime_package",
    ]
    assert metadata.to_dict()["node_types"][0]["parameters"] == [
        "instance_root",
        "resultant_gdb",
    ]


def test_pyproject_declares_mkrf_freshforge_entry_point() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    entry_points = pyproject["project"]["entry-points"]["freshforge.providers"]
    assert entry_points["mkrf"] == "mkrf_freshforge:provider_factory"


def test_provider_execution_constructs_femic_command() -> None:
    from freshforge.records import ExecutionContext, WorkflowNode

    commands: list[tuple[str, ...]] = []
    provider = MkrfFreshForgeProvider(command_runner=_successful_runner(commands))
    node_type = next(
        item for item in provider.metadata().node_types if item.id == "build_au_inputs"
    )
    node = WorkflowNode(
        id="build_au_inputs",
        provider="mkrf.build_au_inputs",
        parameters={
            "instance_root": ".",
            "resultant_gdb": "data/source/03_MappingAnalysisData/Resultant.gdb",
        },
    )

    result = provider.execute_node(
        node,
        node_type,
        context=ExecutionContext(workflow_id="wf", run_id="run"),
    )

    assert result.diagnostics == ()
    assert commands == [
        (
            sys.executable,
            "-m",
            "femic",
            "instance",
            "mkrf-build-au-inputs",
            "--instance-root",
            ".",
            "--resultant-gdb",
            "data/source/03_MappingAnalysisData/Resultant.gdb",
        )
    ]


def test_workflow_validates_and_plans_with_mkrf_provider() -> None:
    from freshforge.loading import load_workflow
    from freshforge.planning import create_run_plan
    from freshforge.validation import validate_workflow_with_providers

    spec, load_diagnostics = load_workflow(WORKFLOW_PATH)
    assert spec is not None
    assert load_diagnostics == []

    registry = _registry_with_femic_and_mkrf()
    diagnostics = validate_workflow_with_providers(
        spec,
        registry=registry,
        structural_diagnostics=load_diagnostics,
    )
    assert diagnostics == []

    plan = create_run_plan(spec, diagnostics=diagnostics, registry=registry)
    assert not plan.has_errors
    assert [node.id for node in plan.nodes] == EXPECTED_MODEL_BUILD_ORDER
    assert {node.provider_id for node in plan.nodes} == {"femic", "mkrf"}


def test_workflow_dry_run_uses_mkrf_provider() -> None:
    from freshforge.execution import execute_workflow
    from freshforge.loading import load_workflow

    spec, load_diagnostics = load_workflow(WORKFLOW_PATH)
    assert spec is not None

    report = execute_workflow(
        spec,
        run_id="mkrf_freshforge_exec",
        diagnostics=load_diagnostics,
        registry=_registry_with_femic_and_mkrf(),
        dry_run=True,
    )

    assert not report.failed
    assert report.dry_run
    assert report.planned_order == tuple(EXPECTED_MODEL_BUILD_ORDER)
