"""Every base workspace package imports without GPU dependencies."""

import importlib

import pytest

PACKAGES = (
    "llmopt_agent",
    "llmopt_benchmark",
    "llmopt_capsule",
    "llmopt_cli",
    "llmopt_common",
    "llmopt_control_plane",
    "llmopt_domain",
    "llmopt_integrations",
    "llmopt_optimization_worker",
    "llmopt_optimizer",
    "llmopt_schemas",
    "llmopt_telemetry",
)


@pytest.mark.smoke
@pytest.mark.parametrize("package_name", PACKAGES)
def test_package_imports(package_name: str) -> None:
    assert importlib.import_module(package_name) is not None
