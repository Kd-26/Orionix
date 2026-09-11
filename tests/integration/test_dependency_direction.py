"""Lightweight import and manifest checks enforce the package layering."""

import ast
import tomllib
from collections.abc import Iterable
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]

ALLOWED_INTERNAL_IMPORTS = {
    "llmopt_common": set(),
    "llmopt_domain": {"llmopt_common"},
    "llmopt_schemas": {"llmopt_common", "llmopt_domain"},
    "llmopt_config": {"llmopt_common"},
    "llmopt_discovery": {"llmopt_schemas"},
    "llmopt_workload": {"llmopt_schemas"},
    "llmopt_benchmark": {"llmopt_common", "llmopt_schemas"},
    "llmopt_optimizer": {"llmopt_schemas"},
    "llmopt_quality": {"llmopt_schemas"},
    "llmopt_capsule": {"llmopt_common", "llmopt_domain", "llmopt_schemas"},
    "llmopt_telemetry": set(),
    "llmopt_deployment": {"llmopt_schemas"},
    "llmopt_integrations": {"llmopt_schemas"},
}


def _internal_imports(path: Path) -> set[str]:
    imported: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        module = node.module if isinstance(node, ast.ImportFrom) else None
        names: Iterable[str]
        if isinstance(node, ast.Import):
            names = (alias.name for alias in node.names)
        elif module is not None:
            names = (module,)
        else:
            continue
        imported.update(
            name.split(".", maxsplit=1)[0] for name in names if name.startswith("llmopt_")
        )
    return imported


@pytest.mark.integration
def test_stable_package_import_direction() -> None:
    for package, allowed in ALLOWED_INTERNAL_IMPORTS.items():
        package_root = next(ROOT.glob(f"**/src/{package}"))
        actual = set().union(*(_internal_imports(path) for path in package_root.rglob("*.py")))
        actual.discard(package)
        assert actual <= allowed, f"{package} imports prohibited packages: {actual - allowed}"


@pytest.mark.integration
def test_workspace_dependency_graph_is_acyclic() -> None:
    graph: dict[str, set[str]] = {}
    for manifest in ROOT.glob("**/pyproject.toml"):
        if ".venv" in manifest.parts or manifest == ROOT / "pyproject.toml":
            continue
        project = tomllib.loads(manifest.read_text(encoding="utf-8"))["project"]
        graph[project["name"]] = {
            dependency.split("=", maxsplit=1)[0]
            for dependency in project.get("dependencies", ())
            if dependency.startswith("llmopt-")
        }

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(package: str) -> None:
        if package in visiting:
            raise AssertionError(f"dependency cycle includes {package}")
        if package in visited:
            return
        visiting.add(package)
        for dependency in graph.get(package, set()):
            visit(dependency)
        visiting.remove(package)
        visited.add(package)

    for package in graph:
        visit(package)
