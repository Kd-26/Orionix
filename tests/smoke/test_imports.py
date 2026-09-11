"""Every base workspace package imports without GPU dependencies."""

import importlib

import pytest

PACKAGES = (
    "llmopt_agent",
    "llmopt_benchmark",
    "llmopt_capsule",
    "llmopt_cli",
    "llmopt_common",
    "llmopt_config",
    "llmopt_control_plane",
    "llmopt_deployment",
    "llmopt_discovery",
    "llmopt_domain",
    "llmopt_integrations",
    "llmopt_optimizer",
    "llmopt_quality",
    "llmopt_schemas",
    "llmopt_telemetry",
    "llmopt_workload",
)


@pytest.mark.smoke
@pytest.mark.parametrize("package_name", PACKAGES)
def test_package_imports(package_name: str) -> None:
    assert importlib.import_module(package_name) is not None
