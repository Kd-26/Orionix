"""Every base workspace package imports without GPU dependencies."""

import importlib
import importlib.resources
import sys

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

INTEGRATION_NAMESPACES = (
    "llmopt_integrations.artifacts.foundry",
    "llmopt_integrations.cache.lmcache",
    "llmopt_integrations.engines.sglang",
    "llmopt_integrations.engines.tensorrt_llm",
    "llmopt_integrations.engines.vllm",
    "llmopt_integrations.execution.docker_host",
    "llmopt_integrations.execution.jarvislabs",
    "llmopt_integrations.execution.local_host",
    "llmopt_integrations.execution.modal",
    "llmopt_integrations.execution.runpod",
)

OPTIONAL_RUNTIME_MODULES = {
    "fastapi",
    "jarvislabs",
    "kubernetes",
    "modal",
    "optuna",
    "pynvml",
    "ray",
    "runpod",
    "sglang",
    "tensorrt_llm",
    "torch",
    "vllm",
}


@pytest.mark.smoke
@pytest.mark.parametrize("package_name", PACKAGES)
def test_package_imports(package_name: str) -> None:
    assert importlib.import_module(package_name) is not None


@pytest.mark.smoke
@pytest.mark.parametrize("package_name", PACKAGES)
def test_typed_package_marker_is_visible(package_name: str) -> None:
    package_root = importlib.resources.files(package_name)

    assert package_root.joinpath("py.typed").is_file()


@pytest.mark.smoke
@pytest.mark.parametrize("namespace", INTEGRATION_NAMESPACES)
def test_integration_namespace_imports_without_optional_sdks(namespace: str) -> None:
    modules_before = set(sys.modules)

    assert importlib.import_module(namespace) is not None

    newly_loaded_roots = {name.partition(".")[0] for name in set(sys.modules) - modules_before}
    assert newly_loaded_roots.isdisjoint(OPTIONAL_RUNTIME_MODULES)
